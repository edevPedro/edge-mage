"""Verificador genérico (§6): roda um comando que devolve JSON no stdout.

Nunca conta uma única execução: o comando é invocado `runs` vezes e as métricas
são agregadas entre invocações, com detecção de ruído por coeficiente de variação.

Contrato de saída (JSON, uma linha `__MAGE_VERIFY__ {...}` ou o stdout inteiro)::

    {
      "ok": true, "stage": "ok", "message": "...",
      "metrics": {"p99_ns": {"median": 120.0, "p50": 90.0, "p99": 250.0,
                             "p999": 400.0, "min": 80.0, "max": 500.0,
                             "samples": 7, "cv": 0.02}},
      "runs": 7, "warmup": 3,
      "degraded": false, "degraded_reason": "",
      "detail": "..."
    }
"""

from __future__ import annotations

import json
import re
import shlex
import statistics
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

from edge_mage.roadmap.models import Challenge, DailyGoal, VerifyConfig

VERIFY_MARKER = "__MAGE_VERIFY__"
MIN_RUNS = 2
_JSON_OBJ = re.compile(r"\{.*\}", re.DOTALL)


@dataclass
class VerifyOutcome:
    ok: bool
    status: str
    stage: str
    message: str
    cmd: str = ""
    metrics: dict = field(default_factory=dict)
    noisy: bool = False
    noisy_metrics: list[str] = field(default_factory=list)
    runs: int = 0
    warmup: int = 0
    degraded: bool = False
    degraded_reason: str = ""
    detail: str = ""
    invocations: int = 0
    duration_s: float = 0.0


def parse_json_stdout(stdout: str) -> dict | None:
    marker_payload: dict | None = None
    for line in stdout.splitlines():
        if line.startswith(VERIFY_MARKER):
            raw = line[len(VERIFY_MARKER):].strip()
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                marker_payload = parsed
    if marker_payload is not None:
        return marker_payload
    text = stdout.strip()
    if not text:
        return None
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    matches = _JSON_OBJ.findall(text)
    for candidate in reversed(matches):
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


def _run_once(cmd: str, work_dir: Path, timeout_s: float) -> tuple[bool, str, str, float, bool]:
    start = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            cwd=str(work_dir),
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired as exc:
        dur = time.monotonic() - start
        out = exc.stdout or ""
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        return False, out, "timeout", dur, True
    except OSError as exc:
        dur = time.monotonic() - start
        return False, "", str(exc), dur, False
    dur = time.monotonic() - start
    return proc.returncode == 0, proc.stdout, proc.stderr, dur, False


def _metric_median(values: list[float]) -> float:
    return round(statistics.median(values), 6)


def _aggregate_metrics(run_metrics: list[dict], noise_cv: float) -> tuple[dict, bool, list[str]]:
    names: set[str] = set()
    for rm in run_metrics:
        names.update(rm.keys())
    out: dict = {}
    noisy: list[str] = []
    for name in sorted(names):
        stats_per_run = [rm[name] for rm in run_metrics if isinstance(rm.get(name), dict)]
        if not stats_per_run:
            continue
        keys: set[str] = set()
        for s in stats_per_run:
            keys.update(s.keys())
        merged: dict = {}
        for key in sorted(keys):
            vals = [float(s[key]) for s in stats_per_run if isinstance(s.get(key), (int, float))]
            if not vals:
                continue
            if key == "samples":
                merged[key] = int(sum(vals))
            else:
                merged[key] = _metric_median(vals)
        medians = [float(s["median"]) for s in stats_per_run if isinstance(s.get("median"), (int, float))]
        if len(medians) >= MIN_RUNS and statistics.mean(medians) > 0:
            cv = statistics.pstdev(medians) / statistics.mean(medians)
            merged["cv"] = round(cv, 6)
            if cv > noise_cv:
                noisy.append(name)
        out[name] = merged
    return out, bool(noisy), noisy


def run_verifier(
    challenge: Challenge,
    goal: DailyGoal | None,
    work_dir: Path,
    *,
    config: VerifyConfig | None = None,
    runs: int | None = None,
) -> VerifyOutcome:
    cfg = config or challenge.verify
    cmd = challenge.verify_command(goal)
    if not cmd.strip():
        return VerifyOutcome(
            ok=False, status="FAIL", stage="config",
            message=f"desafio {challenge.id} sem comando de verificação",
        )
    if not work_dir.exists():
        return VerifyOutcome(
            ok=False, status="FAIL", stage="workdir",
            message=f"diretório de trabalho ausente: {work_dir}",
            cmd=cmd,
        )
    n = runs if runs is not None else max(MIN_RUNS, cfg.runs)
    total_runs = 0
    warmup = 0
    run_metrics: list[dict] = []
    all_ok = True
    stage = "ok"
    message = "verificado"
    detail = ""
    degraded = False
    degraded_reason = ""
    total_duration = 0.0
    timed_out = False

    for i in range(n):
        ok, stdout, stderr, dur, to = _run_once(cmd, work_dir, cfg.timeout_s)
        total_duration += dur
        if to:
            timed_out = True
            all_ok = False
            stage = "timeout"
            message = f"timeout após {cfg.timeout_s:.0f}s"
            detail = stdout[-2000:]
            break
        parsed = parse_json_stdout(stdout)
        run_ok = ok
        if parsed is not None:
            run_ok = bool(parsed.get("ok", ok)) and ok
            m = parsed.get("metrics")
            if isinstance(m, dict):
                run_metrics.append(m)
            total_runs += int(parsed.get("runs") or 0)
            warmup = max(warmup, int(parsed.get("warmup") or 0))
            if parsed.get("degraded"):
                degraded = True
                degraded_reason = str(parsed.get("degraded_reason") or degraded_reason)
            if not run_ok:
                stage = str(parsed.get("stage") or "verify")
                message = str(parsed.get("message") or message)
                detail = str(parsed.get("detail") or "")[-2000:]
        else:
            total_runs += 1
            if not ok:
                stage = "verify"
                message = (stderr.strip().splitlines() or ["comando falhou"])[-1][:200]
                detail = (stdout + "\n" + stderr)[-2000:]
        if not run_ok:
            all_ok = False
            if i == n - 1:
                break

    metrics, noisy, noisy_metrics = _aggregate_metrics(run_metrics, cfg.noise_cv)
    if run_metrics and total_runs < MIN_RUNS:
        noisy = True
        message = f"poucas execuções ({total_runs}) — rode novamente"
    ok_final = all_ok and not noisy and not timed_out
    if noisy and stage == "ok":
        stage = "noise"
        message = "variância alta em: " + ", ".join(noisy_metrics[:4]) + " — rode novamente"
    status = "PASS" if ok_final else ("NOISE" if noisy else "FAIL")
    return VerifyOutcome(
        ok=ok_final,
        status=status,
        stage=stage,
        message=message,
        cmd=cmd,
        metrics=metrics,
        noisy=noisy,
        noisy_metrics=noisy_metrics,
        runs=total_runs,
        warmup=warmup,
        degraded=degraded,
        degraded_reason=degraded_reason,
        detail=detail,
        invocations=n,
        duration_s=round(total_duration, 3),
    )


def shell_argv(cmd: str) -> list[str]:
    """Utilitário para inspeção/testes."""
    return shlex.split(cmd)
