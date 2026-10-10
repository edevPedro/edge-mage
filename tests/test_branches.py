"""Testes do ciclo de vida dos ramos (§3/§5) e dos gráficos SVG (§11)."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from edge_mage.roadmap import branches as branches_mod
from edge_mage.roadmap import charts as charts_mod
from edge_mage.roadmap import daily as daily_mod
from edge_mage.roadmap import evidence as evidence_mod
from edge_mage.roadmap.models import (
    Branch,
    Challenge,
    DailyGoal,
    OpenWhen,
    Roadmap,
    RoadmapRules,
)

TODAY = date(2026, 10, 12)


def _challenge(cid: str, goals: int = 2) -> Challenge:
    return Challenge(
        id=cid,
        track="A",
        title=cid,
        dir=Path("/tmp") / cid,
        daily_goals=[DailyGoal(id=f"g{i}", goal="x") for i in range(1, goals + 1)],
    )


def _roadmap() -> Roadmap:
    return Roadmap(
        trunk_order=["c01"],
        rules=RoadmapRules(trunk_min_pct=65, branches_max_pct=35, max_active_branches=2, stagnation_weeks=2),
        branches=[
            Branch(id="cal", title="Calendário", opens_when=OpenWhen(week=2)),
            Branch(id="evid", title="Evidência", opens_when=OpenWhen(challenge="c01")),
            Branch(id="late", title="Tarde", opens_when=OpenWhen(week=9)),
        ],
        challenges={"c01": _challenge("c01")},
    )


def _state(*, started: date = date(2026, 10, 5)) -> daily_mod.DailyState:
    st = daily_mod.DailyState()
    st.started_at = started.isoformat()
    return st


def test_program_week() -> None:
    rm = _roadmap()
    st = _state(started=date(2026, 10, 5))
    assert branches_mod.program_week(rm, st, today=date(2026, 10, 5)) == 1
    assert branches_mod.program_week(rm, st, today=date(2026, 10, 12)) == 2


def test_branch_opens_by_calendar_and_evidence() -> None:
    rm = _roadmap()
    st = _state(started=date(2026, 10, 5))
    # semana 1: nada abre por calendário; evidência também não (c01 incompleto)
    statuses = {s.branch.id: s for s in branches_mod.statuses(rm, st, today=date(2026, 10, 5))}
    assert statuses["cal"].open is False
    assert statuses["evid"].open is False
    # semana 2: 'cal' abre
    statuses = {s.branch.id: s for s in branches_mod.statuses(rm, st, today=TODAY)}
    assert statuses["cal"].open is True
    # concluir c01 abre 'evid'
    daily_mod.mark_goal_done(st, "c01", "g1")
    daily_mod.mark_goal_done(st, "c01", "g2")
    statuses = {s.branch.id: s for s in branches_mod.statuses(rm, st, today=TODAY)}
    assert statuses["evid"].open is True


def test_activate_respects_cap_and_openness() -> None:
    rm = _roadmap()
    st = _state()
    ok, msg = branches_mod.activate(rm, st, "late", today=TODAY)
    assert not ok and "não abre" in msg
    ok, _ = branches_mod.activate(rm, st, "cal", today=TODAY)
    assert ok
    daily_mod.mark_goal_done(st, "c01", "g1")
    daily_mod.mark_goal_done(st, "c01", "g2")
    ok, _ = branches_mod.activate(rm, st, "evid", today=TODAY)
    assert ok
    assert st.branches_active == ["cal", "evid"]
    # terceiro ramo excede o teto de 2 ativos
    st2 = _state()
    st2.branches_active = ["cal", "evid"]
    ok, msg = branches_mod.activate(rm, st2, "cal", today=TODAY)
    assert ok and msg == "já ativo"


def test_deactivate() -> None:
    rm = _roadmap()
    st = _state()
    branches_mod.activate(rm, st, "cal", today=TODAY)
    assert branches_mod.deactivate(st, "cal")
    assert st.branches_active == []
    assert not branches_mod.deactivate(st, "cal")


def test_trunk_share() -> None:
    rm = _roadmap()
    ts = f"{TODAY.isoformat()}T12:00:00+00:00"
    recs = [
        evidence_mod.Evidence(challenge_id="c01", goal_id="g1", timestamp=ts, ok=True, status="PASS"),
        evidence_mod.Evidence(challenge_id="c01", goal_id="g2", timestamp=ts, ok=True, status="PASS"),
        evidence_mod.Evidence(challenge_id="c01", goal_id="g3", timestamp=ts, ok=True, status="PASS"),
        evidence_mod.Evidence(challenge_id="branch-x", goal_id="b1", timestamp=ts, ok=True, status="PASS"),
    ]
    pct, tn, tot = branches_mod.trunk_share(recs, rm, days=7, today=TODAY)
    assert (tn, tot) == (3, 4)
    assert pct == 75.0
    # record antigo (fora da janela) é ignorado
    old = f"{(TODAY - timedelta(days=30)).isoformat()}T12:00:00+00:00"
    recs.append(evidence_mod.Evidence(challenge_id="c01", goal_id="g4", timestamp=old, ok=True, status="PASS"))
    pct2, tn2, tot2 = branches_mod.trunk_share(recs, rm, days=7, today=TODAY)
    assert (tn2, tot2) == (3, 4)


def test_stagnation_warning() -> None:
    rm = _roadmap()
    st = _state(started=date(2026, 9, 1))
    stale = f"{(TODAY - timedelta(days=20)).isoformat()}T12:00:00+00:00"
    recs = [evidence_mod.Evidence(challenge_id="c01", goal_id="g1", timestamp=stale, ok=True, status="PASS")]
    warn = branches_mod.stagnation_warning(rm, st, recs, today=TODAY)
    assert warn is not None and "estagnado" in warn
    fresh = f"{(TODAY - timedelta(days=1)).isoformat()}T12:00:00+00:00"
    recs.append(evidence_mod.Evidence(challenge_id="c01", goal_id="g2", timestamp=fresh, ok=True, status="PASS"))
    assert branches_mod.stagnation_warning(rm, st, recs, today=TODAY) is None


def test_charts_bar_svg() -> None:
    svg = charts_mod.bar_chart_svg(["Seg", "Ter", "Qua"], [0, 2, 1])
    assert svg.startswith("<svg")
    assert svg.endswith("</svg>")
    assert "Seg" in svg
    assert svg.count("<rect") >= 3


def test_charts_line_svg_and_missing() -> None:
    empty = charts_mod.line_chart_svg([])
    assert "sem dados" in empty
    svg = charts_mod.line_chart_svg([("2026-10-01", 250.0), ("2026-10-05", 180.0)])
    assert svg.startswith("<svg") and "polyline" in svg


def test_metric_series_extracts_p99() -> None:
    recs = [
        evidence_mod.Evidence(
            challenge_id="c01", goal_id="g1", timestamp="2026-10-01T10:00:00+00:00",
            ok=True, status="PASS", metrics={"spsc_p99_ns": {"median": 300.0, "p99": 400.0}},
        ),
        evidence_mod.Evidence(
            challenge_id="c01", goal_id="g2", timestamp="2026-10-03T10:00:00+00:00",
            ok=True, status="PASS", metrics={"spsc_p99_ns": {"median": 200.0, "p99": 250.0}},
        ),
        evidence_mod.Evidence(
            challenge_id="c02", goal_id="g1", timestamp="2026-10-03T10:00:00+00:00",
            ok=True, status="PASS", metrics={"spsc_p99_ns": {"median": 9.0, "p99": 9.0}},
        ),
    ]
    pts = charts_mod.metric_series(recs, challenge_id="c01", stat="p99")
    assert pts == [("2026-10-01", 400.0), ("2026-10-03", 250.0)]


def test_markdown_table() -> None:
    md = charts_mod.markdown_table(["a", "b"], [[1, 2], [3, 4]])
    assert "| a | b |" in md
    assert "| --- | --- |" in md
    assert "| 1 | 2 |" in md
