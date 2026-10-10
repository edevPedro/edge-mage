"""Executa o verificador de uma meta e grava a evidência (§6/§7)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from edge_mage.paths import evidence_dir
from edge_mage.roadmap import evidence as evidence_mod
from edge_mage.roadmap.models import Challenge, DailyGoal
from edge_mage.roadmap.verifier import VerifyOutcome, run_verifier


@dataclass
class VerifyRun:
    outcome: VerifyOutcome
    record: evidence_mod.Evidence
    evidence_path: Path
    work_dir: Path


def verify_goal(
    challenge: Challenge,
    goal: DailyGoal | None,
    work_dir: Path,
    *,
    root: Path | None = None,
    runs: int | None = None,
) -> VerifyRun:
    outcome = run_verifier(challenge, goal, work_dir, runs=runs)
    record = evidence_mod.Evidence(
        schema_version=evidence_mod.SCHEMA_VERSION,
        challenge_id=challenge.id,
        goal_id=(goal.id if goal else ""),
        timestamp=__import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        status=outcome.status,
        ok=outcome.ok,
        stage=outcome.stage,
        git_commit=evidence_mod.git_commit(work_dir),
        code_hash=evidence_mod.code_hash(work_dir),
        cpu_model=evidence_mod.cpu_model(),
        os_kernel=evidence_mod.os_kernel(),
        runs=outcome.runs,
        warmup=outcome.warmup,
        metrics=outcome.metrics,
        noise_flag=outcome.noisy,
        noisy_metrics=list(outcome.noisy_metrics),
        degraded=outcome.degraded,
        degraded_reason=outcome.degraded_reason,
        detail=outcome.detail,
        verification_cmd=outcome.cmd,
        invocations=outcome.invocations,
        duration_s=outcome.duration_s,
    )
    if challenge.verify.cmd:
        record.compiler = ""  # preenchido pelo comando de verificação quando aplicável
    path = evidence_mod.write(record, root=root or evidence_dir())
    return VerifyRun(outcome=outcome, record=record, evidence_path=path, work_dir=work_dir)


def format_outcome(outcome: VerifyOutcome, *, record: evidence_mod.Evidence | None = None) -> str:
    head = "PASS" if outcome.ok else outcome.status
    lines = [f"[{head}] stage={outcome.stage} · {outcome.message}"]
    if outcome.cmd:
        lines.append(f"cmd: {outcome.cmd}")
    if outcome.invocations:
        lines.append(
            f"invocações: {outcome.invocations} · runs: {outcome.runs} · warmup: {outcome.warmup}"
        )
    if outcome.metrics:
        lines.append("métricas (mediana entre invocações):")
        for name in sorted(outcome.metrics):
            m = outcome.metrics[name]
            med = m.get("median")
            p99 = m.get("p99")
            cv = m.get("cv")
            bits = [f"med={_fmt(med)}"]
            if p99 is not None:
                bits.append(f"p99={_fmt(p99)}")
            if cv is not None:
                bits.append(f"cv={cv:.2%}")
            if m.get("samples") is not None:
                bits.append(f"n={m['samples']}")
            lines.append(f"  {name:24s} " + "  ".join(bits))
    if outcome.degraded:
        lines.append(f"AVISO degraded: {outcome.degraded_reason or 'recurso indisponível'}")
    if outcome.detail:
        lines.append("detalhe:")
        lines.append("  " + outcome.detail.replace("\n", "\n  "))
    if record and record.code_hash:
        lines.append(f"evidência: {record.code_hash[:12]} · kernel {record.os_kernel}")
    return "\n".join(lines)


def _fmt(x) -> str:
    if isinstance(x, float):
        return f"{x:.4g}"
    return str(x)
