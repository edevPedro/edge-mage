"""Testes do loop quiz → spell → ritual."""

from __future__ import annotations

from pathlib import Path

import pytest

from edge_mage.content import load_all_tracks
from edge_mage.curriculum import next_open_room
from edge_mage.daily import build_daily_run
from edge_mage.juice import numeric_near_miss, xp_banner
from edge_mage.progress import ProgressStore
from edge_mage.ranks import effective_rank, rank_from_xp
from edge_mage.rituals import parse_on_device_checklist, write_artifact
from edge_mage.validators import validate_task


def test_edge_mage_requires_ritual() -> None:
    assert rank_from_xp(2900).id == "edge_mage"
    assert effective_rank(2900, False).id == "arquimago"
    assert effective_rank(2900, True).id == "edge_mage"


def test_numeric_near_miss_hint() -> None:
    msg = numeric_near_miss(1.55, 1.5708)
    assert "Off by" in msg or "Perto" in msg
    assert "1.5708" not in msg or "≈" in msg  # não spoil completo cru se near
    assert xp_banner(12).count("+") >= 1


def test_critical_path_has_code() -> None:
    tracks = load_all_tracks()
    need = {
        "fundamentos",
        "otimizacao",
        "ml-math",
        "edge-ai",
    }
    for t in tracks:
        if t.id not in need:
            continue
        for r in t.rooms:
            if r.boss and r.id != "on-device":
                continue
            codes = [x for x in r.tasks if x.type in {"code", "ritual"}]
            assert codes, f"sala sem code/ritual: {t.id}/{r.id}"


def test_code_tests_harness() -> None:
    tracks = load_all_tracks()
    fund = next(t for t in tracks if t.id == "fundamentos")
    vet = next(r for r in fund.rooms if r.id == "vetores")
    code = next(t for t in vet.tasks if t.type == "code")
    assert code.code_tests.strip()
    ok, msg = validate_task(
        code,
        "def dot(a, b):\n    return sum(x*y for x,y in zip(a,b))\n",
    )
    assert ok, msg


def test_streak_mana_and_combo(tmp_path: Path) -> None:
    store = ProgressStore(tmp_path / "p.json")
    store.state.streak_days = 3
    assert store.xp_multiplier() == 1.25
    store.state.streak_days = 1
    assert store.xp_multiplier() == 1.0
    c = store.bump_daily_combo()
    assert c == 1
    assert store.bump_daily_combo() == 2


def test_daily_run_persists(tmp_path: Path) -> None:
    store = ProgressStore(tmp_path / "p.json")
    tracks = load_all_tracks()
    # mark trigonometria done so review exists after we complete it lightly
    fund = next(t for t in tracks if t.id == "fundamentos")
    room = next(r for r in fund.rooms if r.id == "trigonometria")
    for task in room.tasks:
        if task.type == "code":
            continue
        if task.type == "mcq":
            from edge_mage.validators import _resolve_mcq_answer

            ans = chr(ord("A") + _resolve_mcq_answer(task))
        elif task.type == "numeric":
            ans = str(task.answer)
        elif task.type == "fill":
            ans = task.answers[0]
        else:
            continue
        ok, _ = validate_task(task, ans)
        assert ok
        store.mark_task(fund.id, room.id, task.id, task.xp, room)
    # room may still miss code task — force room done for daily review
    store.state.completed_rooms[store.state.room_key(fund.id, room.id)] = True
    store.save()
    d1 = build_daily_run(store, tracks, day="2099-01-01")
    d2 = build_daily_run(store, tracks, day="2099-01-01")
    assert d1["date"] == d2["date"] == "2099-01-01"
    assert d1.get("new")


def test_continue_picks_open_room(tmp_path: Path) -> None:
    store = ProgressStore(tmp_path / "p.json")
    tracks = load_all_tracks()
    nxt = next_open_room(store, tracks)
    assert nxt is not None
    assert nxt[1].id == "trigonometria"


def test_on_device_checklist(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "study-log" / "artifacts").mkdir(parents=True)
    body = """
- latency_ms: 12.5
- ram_mb: 64
- model: mobilenet-int8
- device: rpi5
"""
    write_artifact("on-device", body, repo_root=tmp_path)
    ok, msg, fields = parse_on_device_checklist(body)
    assert ok, msg
    assert fields["model"] == "mobilenet-int8"


def test_boss_rooms_exist() -> None:
    tracks = load_all_tracks()
    rit = next(t for t in tracks if t.id == "rituais")
    ids = {r.id for r in rit.rooms}
    assert {"codex-matricial", "softmax-estavel", "quant-lab"} <= ids
    edge = next(t for t in tracks if t.id == "edge-ai")
    assert edge.requires_ritual == "softmax-estavel"
