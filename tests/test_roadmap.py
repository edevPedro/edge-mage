"""Testes do motor da plataforma (Passo 1): loader, verifier, evidence, daily."""

from __future__ import annotations

import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

from edge_mage.roadmap import daily as daily_mod
from edge_mage.roadmap import evidence as evidence_mod
from edge_mage.roadmap.loader import load_roadmap
from edge_mage.roadmap.runner import verify_goal
from edge_mage.roadmap.verifier import parse_json_stdout, run_verifier

VERIFY_SCRIPT = """#!/bin/sh
printf '%%s\\n' '__MAGE_VERIFY__ {"ok": true, "stage": "ok", "message": "ok", "metrics": {"p99_ns": {"median": %s, "p50": %s, "p99": %s, "samples": 7}}, "runs": 7, "warmup": 2}'
"""


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture()
def platform(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    home = tmp_path / "mage-home"
    monkeypatch.setenv("MAGE_HOME", str(home))
    roadmap_root = tmp_path / "roadmap"
    challenges_root = tmp_path / "challenges"
    work_root = tmp_path / "work"
    monkeypatch.setenv("MAGE_ROADMAP_ROOT", str(roadmap_root))
    monkeypatch.setenv("MAGE_CHALLENGES_ROOT", str(challenges_root))
    monkeypatch.setenv("MAGE_WORK_ROOT", str(work_root))

    _write(
        roadmap_root / "roadmap.yaml",
        "version: 1\n"
        "daily_minutes: 60\ntrunk_track: A\n"
        "trunk_order: [c01-demo, c02-demo]\n"
        "rules: {trunk_min_pct: 65, branches_max_pct: 35, max_active_branches: 2, rollover_max: 1}\n",
    )
    _write(
        roadmap_root / "branches.yaml",
        "branches:\n"
        "  - {id: leetcode, title: LeetCode, opens_when: {week: 1}, weekly_cap_pct: 15}\n"
        "  - {id: mem, title: Memória, opens_when: {challenge: c01-demo}, weekly_cap_pct: 10}\n",
    )

    work = work_root / "c01-demo"
    work.mkdir(parents=True, exist_ok=True)
    _write(work / "verify.sh", VERIFY_SCRIPT % ("100", "90", "250"))
    (work / "verify.sh").chmod(0o755)

    _write(
        challenges_root / "c01-demo" / "challenge.yaml",
        "id: c01-demo\ntrack: A\ntitle: Demo\n"
        "timebox_days: 21\n"
        "exit_criteria: {metric: p99_ns, target: '< 200'}\n"
        "sources:\n"
        "  - {name: cppreference, url: 'https://x', section: memory_order, why: ordenação}\n"
        "  - {name: Drepper, section: caches, why: false sharing}\n"
        "daily_goals:\n"
        "  - {id: g1, goal: 'push/pop corretos', verify: 'sh verify.sh'}\n"
        "  - {id: g2, goal: 'medir p99', verify: 'sh verify.sh'}\n"
        "verify: {cmd: 'sh verify.sh', timeout_s: 20, runs: 3}\n"
        "artifact: {readme_sections: ['O que medi', 'O que me surpreendeu', 'O que faria depois']}\n",
    )
    _write(
        challenges_root / "c02-demo" / "challenge.yaml",
        "id: c02-demo\ntrack: A\ntitle: Demo 2\ndaily_goals:\n"
        "  - {id: g1, goal: 'x', verify: 'sh verify.sh'}\n"
        "verify: {cmd: 'sh verify.sh', timeout_s: 20, runs: 3}\n",
    )
    return {"home": home, "roadmap": roadmap_root, "challenges": challenges_root, "work": work_root}


def test_loader_reads_roadmap_and_challenge(platform) -> None:
    rm = load_roadmap()
    assert rm.daily_minutes == 60
    assert rm.trunk_order == ["c01-demo", "c02-demo"]
    assert set(rm.challenges) == {"c01-demo", "c02-demo"}
    ch = rm.challenge("c01-demo")
    assert ch is not None
    assert [g.id for g in ch.daily_goals] == ["g1", "g2"]
    assert ch.sources[0].section == "memory_order"
    assert len(rm.branches) == 2
    assert rm.branch("leetcode").opens_when.week == 1


def test_parse_json_stdout_variants() -> None:
    assert parse_json_stdout('__MAGE_VERIFY__ {"ok": true}') == {"ok": True}
    assert parse_json_stdout('{"ok": false, "stage": "tests"}') == {"ok": False, "stage": "tests"}
    assert parse_json_stdout('log line\n{"ok": true}\ntrailing') == {"ok": True}
    assert parse_json_stdout("no json here") is None


def test_run_verifier_aggregates_and_flags(platform) -> None:
    rm = load_roadmap()
    ch = rm.challenge("c01-demo")
    goal = ch.goal("g1")
    wd = platform["work"] / "c01-demo"
    out = run_verifier(ch, goal, wd, runs=3)
    assert out.ok
    assert out.invocations == 3
    assert out.runs == 21  # 7 * 3
    assert "p99_ns" in out.metrics
    assert out.metrics["p99_ns"]["median"] == pytest.approx(100.0)


def test_run_verifier_missing_workdir(platform) -> None:
    rm = load_roadmap()
    ch = rm.challenge("c01-demo")
    out = run_verifier(ch, ch.goal("g1"), platform["work"] / "nope")
    assert not out.ok
    assert out.stage == "workdir"


def test_verify_goal_writes_evidence(platform) -> None:
    rm = load_roadmap()
    ch = rm.challenge("c01-demo")
    wd = platform["work"] / "c01-demo"
    run = verify_goal(ch, ch.goal("g1"), wd)
    assert run.outcome.ok
    assert run.evidence_path.exists()
    assert run.evidence_path.parent.name == "c01-demo"
    rec = evidence_mod.read_latest("c01-demo")
    assert rec is not None
    assert rec.schema_version == evidence_mod.SCHEMA_VERSION
    assert rec.goal_id == "g1"
    assert rec.runs == 21
    assert rec.code_hash
    assert rec.os_kernel


def test_evidence_append_only_and_explanation(platform) -> None:
    rm = load_roadmap()
    ch = rm.challenge("c01-demo")
    wd = platform["work"] / "c01-demo"
    verify_goal(ch, ch.goal("g1"), wd)
    verify_goal(ch, ch.goal("g1"), wd)
    recs = evidence_mod.iter_namespace("c01-demo")
    assert len(recs) == 2
    from edge_mage.roadmap.evidence import attach_explanation

    path = attach_explanation("c01-demo", "g1", "medi; surpreendeu; próximo")
    assert path is not None
    latest = evidence_mod.read_latest("c01-demo")
    assert latest.explanation == "medi; surpreendeu; próximo"


def test_legacy_evidence_detected(platform, tmp_path) -> None:
    root = platform["home"] / "evidence"
    d = root / "old"
    _write(d / "latest.json", json.dumps({"lab_id": "old", "status": "PASS"}))
    rec = evidence_mod.read_latest("old", root=root)
    assert rec is not None
    assert rec.legacy is True


def test_today_selects_first_goal_and_rolls(platform) -> None:
    rm = load_roadmap()
    state = daily_mod.DailyState()
    records: list = []
    d0 = date(2026, 10, 5)
    ctx = daily_mod.today_context(rm, state, records, today=d0)
    assert ctx is not None
    assert ctx.challenge.id == "c01-demo"
    assert ctx.goal.id == "g1"
    assert ctx.source.section == "memory_order"
    # mesmo dia não rola
    ctx2 = daily_mod.today_context(rm, state, records, today=d0)
    assert ctx2.rollovers == 0
    # dia seguinte sem concluir → rola 1x
    ctx3 = daily_mod.today_context(rm, state, records, today=d0 + timedelta(days=1))
    assert ctx3.rollovers == 1
    # segunda rolagem → quebra
    ctx4 = daily_mod.today_context(rm, state, records, today=d0 + timedelta(days=2))
    assert ctx4.rollovers == 2
    assert ctx4.needs_breakup


def test_streak_counts_pass_days(platform) -> None:
    now = datetime.now(timezone.utc)
    recs = [
        evidence_mod.Evidence(challenge_id="c", goal_id="g", timestamp=now.isoformat(), ok=True, status="PASS"),
        evidence_mod.Evidence(
            challenge_id="c", goal_id="g2",
            timestamp=(now - timedelta(days=1)).isoformat(), ok=True, status="PASS",
        ),
        evidence_mod.Evidence(
            challenge_id="c", goal_id="g3",
            timestamp=(now - timedelta(days=3)).isoformat(), ok=True, status="PASS",
        ),
    ]
    assert daily_mod.streak(recs, today=now.date()) == 2
