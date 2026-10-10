"""Runner de labs verificáveis: compila, testa, mede e emite evidência."""

from __future__ import annotations

import json
import operator
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from edge_mage.labs import bench as bench_mod
from edge_mage.labs import evidence as evidence_mod
from edge_mage.labs.errors import LabError, ToolchainError
from edge_mage.labs.sandbox import Limits, clean_env, run_process
from edge_mage.labs.spec import LabSpec, load_spec
from edge_mage.labs.toolchain import find_cpp_compiler
from edge_mage.paths import labs_work_dir

BENCH_MARKER = "__MAGE_BENCH__"
MIN_VALID_RUNS = 2
MIN_REPS = 3


@dataclass
class LabResult:
    lab_id: str
    ok: bool
    stage: str
    message: str
    tests_ok: bool = False
    bench_ok: bool = False
    noisy: bool = False
    noisy_metrics: list[str] = field(default_factory=list)
    metrics: dict[str, dict] = field(default_factory=dict)
    requirements: list[dict] = field(default_factory=list)
    evidence_path: Path | None = None
    code_hash: str = ""
    compiler: str = ""
    detail: str = ""


def init_lab(lab_id: str, *, work_dir: Path | None = None, root: Path | None = None,
             force: bool = False) -> tuple[Path, list[str]]:
    """Semeia o diretório de trabalho do aluno a partir de <lab>/src/."""
    spec = load_spec(lab_id, root=root)
    work = work_dir or labs_work_dir(spec.id)
    work.mkdir(parents=True, exist_ok=True)
    src = spec.dir / "src"
    copied: list[str] = []
    if src.exists():
        for item in sorted(src.rglob("*")):
            if not item.is_file():
                continue
            rel = item.relative_to(src)
            dest = work / rel
            if dest.exists() and not force:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)
            copied.append(rel.as_posix())
    return work, copied


def _build_limits(spec: LabSpec) -> Limits:
    """Compilação pode usar mais memória que a execução."""
    return Limits(
        cpu_seconds=int(spec.timeout_build_s) + 5,
        memory_mb=0,  # sem teto de AS no build
        file_mb=max(spec.limits.file_mb, 256),
        open_files=max(spec.limits.open_files, 512),
    )


def _compile(
    compiler,
    *,
    std: str,
    flags: list[str],
    include_dirs: list[Path],
    sources: list[Path],
    out_bin: Path,
    build_dir: Path,
    timeout_s: float,
    limits: Limits,
):
    argv = [compiler.path, f"-std={std}", *flags]
    for inc in include_dirs:
        argv += ["-I", str(inc)]
    argv += [str(s) for s in sources]
    argv += ["-o", str(out_bin), "-lm"]
    env = clean_env(build_dir)
    return run_process(argv, cwd=build_dir, env=env, limits=limits, timeout_s=timeout_s)


def _parse_bench_line(stdout: str) -> dict | None:
    payload = None
    for line in stdout.splitlines():
        if line.startswith(BENCH_MARKER):
            raw = line[len(BENCH_MARKER):].strip()
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                continue
    return payload if isinstance(payload, dict) else None


def _check_requirements(spec: LabSpec, agg: bench_mod.Aggregate):
    results: list[dict] = []
    ok = True

    if spec.requires_zero_allocs:
        allocs = agg.metrics.get("allocs")
        actual = allocs.median if allocs else None
        passed = actual is not None and actual == 0
        results.append(
            {"metric": "allocs", "op": "==", "value": 0, "actual": actual, "ok": passed}
        )
        ok = ok and passed

    ops = {
        "<=": operator.le,
        "<": operator.lt,
        ">=": operator.ge,
        ">": operator.gt,
        "==": operator.eq,
    }
    for req in spec.requirements:
        metric = str(req.get("metric", ""))
        op = str(req.get("op", "<="))
        value = float(req.get("value", 0))
        summary = agg.metrics.get(metric)
        actual = summary.median if summary else None
        func = ops.get(op)
        passed = actual is not None and func is not None and func(actual, value)
        results.append(
            {"metric": metric, "op": op, "value": value, "actual": actual, "ok": passed}
        )
        ok = ok and passed
    return ok, results


def run_lab(
    lab_id: str,
    *,
    work_dir: Path | None = None,
    root: Path | None = None,
    evidence_root: Path | None = None,
) -> LabResult:
    """Compila, roda testes/benchmark, agrega métricas e grava evidência."""
    try:
        spec = load_spec(lab_id, root=root)
    except LabError as exc:
        return LabResult(lab_id=lab_id, ok=False, stage="spec", message=str(exc))

    work = work_dir or labs_work_dir(spec.id)
    seeded = work.exists() and any(work.rglob("*"))
    if not work.exists() or (work_dir is None and not seeded):
        return LabResult(
            lab_id=lab_id,
            ok=False,
            stage="workdir",
            message=f"diretório de trabalho vazio: rode `mage lab init {lab_id}`",
        )

    try:
        compiler = find_cpp_compiler()
    except ToolchainError as exc:
        return LabResult(lab_id=lab_id, ok=False, stage="toolchain", message=str(exc))

    if spec.bench_reps < MIN_REPS:
        return LabResult(
            lab_id=lab_id,
            ok=False,
            stage="spec",
            message=f"bench_reps={spec.bench_reps} < {MIN_REPS}: nunca conte uma única execução.",
        )

    code_hash_value = evidence_mod.code_hash(work)
    build_dir = Path(tempfile.mkdtemp(prefix=f"mage-lab-{spec.id}-"))
    include_dirs = spec.resolved_include_dirs(work)
    solution = spec.solution_files(work)
    tests_ok = True
    bench_ok = False
    detail = ""
    agg = bench_mod.Aggregate()
    req_results: list[dict] = []
    req_ok = True
    stage = "ok"
    message = "tudo passou"
    ok = True

    try:
        # ---- testes -------------------------------------------------------
        test_files = spec.test_files()
        if test_files:
            missing = [str(t) for t in test_files if not t.exists()]
            if missing:
                return LabResult(
                    lab_id=lab_id,
                    ok=False,
                    stage="spec",
                    message=f"test_sources ausentes: {', '.join(missing)}",
                )
            tests_bin = build_dir / "tests_bin"
            comp = _compile(
                compiler,
                std=spec.std,
                flags=spec.flags,
                include_dirs=include_dirs,
                sources=solution + test_files,
                out_bin=tests_bin,
                build_dir=build_dir,
                timeout_s=spec.timeout_build_s,
                limits=_build_limits(spec),
            )
            if not comp.ok:
                return _finish(
                    lab_id, spec, compiler, code_hash_value, evidence_root,
                    ok=False, stage="build", message="falha ao compilar os testes",
                    tests_ok=False, detail=comp.tail(10),
                )
            run = run_process(
                [str(tests_bin)],
                cwd=build_dir,
                env=clean_env(work),
                limits=spec.limits,
                timeout_s=spec.timeout_run_s,
            )
            if run.timed_out:
                return _finish(
                    lab_id, spec, compiler, code_hash_value, evidence_root,
                    ok=False, stage="tests", message="timeout ao rodar os testes",
                    tests_ok=False, detail=run.tail(6),
                )
            if not run.ok:
                return _finish(
                    lab_id, spec, compiler, code_hash_value, evidence_root,
                    ok=False, stage="tests", message="testes falharam",
                    tests_ok=False, detail=run.tail(10),
                )

        # ---- benchmark ----------------------------------------------------
        bench_file = spec.bench_file()
        if bench_file and bench_file.exists():
            bench_bin = build_dir / "bench_bin"
            comp = _compile(
                compiler,
                std=spec.std,
                flags=spec.flags,
                include_dirs=include_dirs,
                sources=solution + [bench_file],
                out_bin=bench_bin,
                build_dir=build_dir,
                timeout_s=spec.timeout_build_s,
                limits=_build_limits(spec),
            )
            if not comp.ok:
                return _finish(
                    lab_id, spec, compiler, code_hash_value, evidence_root,
                    ok=False, stage="build", message="falha ao compilar o benchmark",
                    tests_ok=tests_ok, detail=comp.tail(10),
                )
            env = clean_env(work)
            for _ in range(max(0, spec.bench_warmup)):
                run_process(
                    [str(bench_bin)], cwd=build_dir, env=env,
                    limits=spec.limits, timeout_s=spec.timeout_run_s,
                )
            runs: list[dict] = []
            for _ in range(spec.bench_reps):
                run = run_process(
                    [str(bench_bin)], cwd=build_dir, env=env,
                    limits=spec.limits, timeout_s=spec.timeout_run_s,
                )
                parsed = _parse_bench_line(run.stdout)
                if run.ok and parsed is not None:
                    runs.append(parsed)
            if len(runs) < MIN_VALID_RUNS:
                return _finish(
                    lab_id, spec, compiler, code_hash_value, evidence_root,
                    ok=False, stage="bench",
                    message=f"benchmark inválido ({len(runs)}/{spec.bench_reps} runs válidos)",
                    tests_ok=tests_ok, detail="sem linha __MAGE_BENCH__ ou crash/timeout",
                )
            agg = bench_mod.aggregate_runs(runs, noise_cv=spec.noise_cv)
            bench_ok = len(agg.metrics) > 0
            req_ok, req_results = _check_requirements(spec, agg)

            if agg.noisy:
                stage = "noise"
                message = (
                    "variância alta detectada em: "
                    + ", ".join(agg.noisy_metrics[:4])
                    + " — rode novamente (máquina ocupada?)"
                )
                ok = False
            elif not req_ok:
                stage = "requirements"
                failed = [r["metric"] for r in req_results if not r["ok"]]
                message = f"requisitos não atendidos: {', '.join(failed)}"
                ok = False
            else:
                ok = tests_ok
        else:
            ok = tests_ok

    finally:
        shutil.rmtree(build_dir, ignore_errors=True)

    return _finish(
        lab_id, spec, compiler, code_hash_value, evidence_root,
        ok=ok, stage=stage, message=message,
        tests_ok=tests_ok, bench_ok=bench_ok, agg=agg,
        req_results=req_results, req_ok=req_ok, detail=detail,
    )


def _finish(
    lab_id: str,
    spec: LabSpec,
    compiler,
    code_hash_value: str,
    evidence_root: Path | None,
    *,
    ok: bool,
    stage: str,
    message: str,
    tests_ok: bool = False,
    bench_ok: bool = False,
    agg: bench_mod.Aggregate | None = None,
    req_results: list[dict] | None = None,
    req_ok: bool = True,
    detail: str = "",
) -> LabResult:
    agg = agg or bench_mod.Aggregate()
    metrics = {name: m.to_dict() for name, m in agg.metrics.items()}
    record = evidence_mod.build_record(
        lab_id=spec.id,
        status="PASS" if ok else "FAIL",
        code_hash_value=code_hash_value,
        compiler=compiler,
        std=spec.std,
        flags=spec.flags,
        metrics=metrics,
        tests_ok=tests_ok,
        noisy=agg.noisy,
        noisy_metrics=agg.noisy_metrics,
        valid_runs=agg.valid_runs,
        detail=detail,
        requirements=req_results or [],
        requirements_ok=req_ok,
    )
    path = evidence_mod.write_evidence(spec.id, record, root=evidence_root)
    return LabResult(
        lab_id=spec.id,
        ok=ok,
        stage=stage,
        message=message,
        tests_ok=tests_ok,
        bench_ok=bench_ok,
        noisy=agg.noisy,
        noisy_metrics=list(agg.noisy_metrics),
        metrics=metrics,
        requirements=req_results or [],
        evidence_path=path,
        code_hash=code_hash_value,
        compiler=compiler.version or compiler.kind,
        detail=detail,
    )


def format_result(result: LabResult) -> str:
    lines: list[str] = []
    head = "PASS" if result.ok else "FAIL"
    lines.append(f"[{head}] {result.lab_id} · stage={result.stage} · {result.message}")
    if result.code_hash:
        lines.append(f"code_hash: {result.code_hash[:12]} · compilador: {result.compiler}")
    if result.metrics:
        lines.append("métricas (mediana entre runs):")
        for name in sorted(result.metrics):
            m = result.metrics[name]
            lines.append(
                f"  {name:24s} med={m['median']:.3g}  p99={m['p99']:.3g}  "
                f"cv={m['cv']:.2%}  n={m['samples']}"
            )
    for req in result.requirements:
        mark = "ok" if req.get("ok") else "X"
        lines.append(f"  [{mark}] {req.get('metric')} {req.get('op')} {req.get('value')}")
    if result.detail:
        lines.append("detalhe:")
        lines.append("  " + result.detail.replace("\n", "\n  "))
    if result.evidence_path:
        lines.append(f"evidência: {result.evidence_path}")
    return "\n".join(lines)
