"""Painel semanal (§8): metas fechadas, evidências, horas por bloco, dispersão.

As horas vêm do estimador por eventos (Passo 3): intervalos entre evidências,
commits no work dir do desafio e commits no próprio repo do e-mage.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from edge_mage.roadmap import daily as daily_mod
from edge_mage.roadmap import evidence as evidence_mod
from edge_mage.roadmap.errors import RoadmapError
from edge_mage.roadmap.loader import load_roadmap
from edge_mage.roadmap.timeusage import weekly_time


@dataclass
class WeekSummary:
    start: date
    end: date
    days_active: int = 0
    goals_closed: int = 0
    evidence_pass: int = 0
    evidence_total: int = 0
    per_challenge: dict = field(default_factory=dict)
    platform_minutes: float = 0.0
    challenge_minutes: float = 0.0
    dispersion_pct: float = 0.0
    streak: int = 0


def _iso_week_bounds(when: date) -> tuple[date, date]:
    start = when - timedelta(days=when.weekday())
    return start, start + timedelta(days=6)


def build_summary(when: date | None = None, *, roadmap=None, state=None, records=None) -> WeekSummary:
    from edge_mage.paths import practice_dir

    d = when or date.today()
    start, end = _iso_week_bounds(d)
    roadmap = roadmap if roadmap is not None else load_roadmap()
    state = state if state is not None else daily_mod.load_state()
    records = records if records is not None else evidence_mod.iter_all()

    summary = WeekSummary(start=start, end=end)
    days: set[str] = set()
    for rec in records:
        if not rec.timestamp:
            continue
        try:
            rd = datetime.fromisoformat(rec.timestamp).date()
        except ValueError:
            continue
        if start <= rd <= end:
            summary.evidence_total += 1
            if rec.is_pass:
                summary.evidence_pass += 1
                days.add(rd.isoformat())
                summary.per_challenge[rec.challenge_id] = summary.per_challenge.get(rec.challenge_id, 0) + 1
    summary.days_active = len(days)
    for iso, entry in state.days.items():
        try:
            ed = date.fromisoformat(iso)
        except ValueError:
            continue
        if start <= ed <= end and entry.get("status") == "closed":
            summary.goals_closed += 1
    summary.streak = daily_mod.streak(records, today=d)

    try:
        tu = weekly_time(start, end, roadmap=roadmap, work_root=practice_dir())
        summary.platform_minutes = tu.platform_minutes
        summary.challenge_minutes = tu.challenge_minutes
        total = tu.platform_minutes + tu.challenge_minutes
        if total > 0:
            summary.dispersion_pct = 100.0 * tu.platform_minutes / total
    except Exception:  # noqa: BLE001 - painel nunca deve quebrar
        pass
    return summary


def render(summary: WeekSummary, *, rules=None) -> str:
    disp_alert = rules.dispersion_alert_pct if rules else 10.0
    lines: list[str] = []
    lines.append("─" * 60)
    lines.append(f"SEMANA {summary.start.isoformat()} → {summary.end.isoformat()}")
    lines.append("─" * 60)
    lines.append(f"dias ativos: {summary.days_active} · streak: {summary.streak} dia(s)")
    lines.append(
        f"evidências PASS: {summary.evidence_pass}/{summary.evidence_total} · "
        f"metas fechadas: {summary.goals_closed}"
    )
    if summary.per_challenge:
        lines.append("por desafio:")
        for cid, n in sorted(summary.per_challenge.items(), key=lambda kv: -kv[1]):
            lines.append(f"  {cid:20s} {n} evidência(s)")
    if summary.platform_minutes or summary.challenge_minutes:
        lines.append("")
        lines.append("tempo (ESTIMATIVA por eventos):")
        lines.append(f"  tronco/desafio: {summary.challenge_minutes/60:.1f} h")
        lines.append(f"  plataforma:     {summary.platform_minutes/60:.1f} h "
                     f"({summary.dispersion_pct:.0f}%)")
        if summary.dispersion_pct > disp_alert:
            lines.append(
                f"  ALERTA de dispersão: plataforma > {disp_alert:.0f}% — "
                "bloqueie novas metas de feature (§8/§12)."
            )
    return "\n".join(lines)


def cmd_week(argv: list[str]) -> int:
    try:
        roadmap = load_roadmap()
        state = daily_mod.load_state()
        records = evidence_mod.iter_all()
    except RoadmapError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1
    summary = build_summary(roadmap=roadmap, state=state, records=records)
    print(render(summary, rules=roadmap.rules))
    return 0
