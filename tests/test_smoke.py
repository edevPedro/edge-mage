"""Smoke tests sem TUI."""

from __future__ import annotations

from pathlib import Path

from edge_mage.content import load_all_tracks
from edge_mage.models import Room, Task
from edge_mage.progress import ProgressStore
from edge_mage.ranks import level_from_xp, rank_from_xp
from edge_mage.validators import validate_task


def test_tracks_load() -> None:
    tracks = load_all_tracks()
    assert len(tracks) >= 8
    playable = [t for t in tracks if not t.scaffold and len(t.rooms) >= 3]
    assert len(playable) >= 3
    for t in tracks:
        assert t.rooms, f"trilha vazia: {t.id}"
        for r in t.rooms:
            assert r.tasks, f"sala sem tasks: {t.id}/{r.id}"
            assert r.lesson_md.strip(), f"lição vazia: {t.id}/{r.id}"


def test_validators_and_xp(tmp_path: Path) -> None:
    store = ProgressStore(tmp_path / "progress.json")
    tracks = load_all_tracks()
    fund = next(t for t in tracks if t.id == "fundamentos")
    room = next(r for r in fund.rooms if r.id == "trigonometria")

    # numeric
    t = next(x for x in room.tasks if x.id == "sin-pi6")
    ok, _ = validate_task(t, "0.5")
    assert ok
    res = store.mark_task(fund.id, room.id, t.id, t.xp, room)
    assert res["gained"] == t.xp
    assert store.state.xp == t.xp

    # mcq
    t2 = next(x for x in room.tasks if x.id == "identity")
    ok, _ = validate_task(t2, "A")
    assert ok

    assert level_from_xp(0) == 1
    assert rank_from_xp(0).id == "novico"
    assert rank_from_xp(2900).id == "edge_mage"


def test_code_task() -> None:
    task = Task(
        id="c",
        type="code",
        prompt="x",
        expected_stdout="5.0",
        code_template="",
    )
    code = "import math\nprint(math.sqrt(9)+2)\n"
    # wait sqrt(9)+2 = 5.0
    ok, msg = validate_task(task, code)
    assert ok, msg


def _solve_known(task: Task) -> str:
    if task.type == "numeric":
        return str(task.answer)
    if task.type == "mcq":
        return "1" if isinstance(task.answer, int) and task.answer == 0 else str(
            (task.answer if isinstance(task.answer, int) else 0) + 1
            if isinstance(task.answer, int)
            else "A"
        )
    if task.type == "fill":
        return (task.answers or [str(task.answer)])[0]
    if task.type == "code":
        # only used for special cases in full solve below
        return ""
    return ""


def test_fundamentos_end_to_end(tmp_path: Path) -> None:
    """Resolve a primeira sala completa e verifica XP."""
    store = ProgressStore(tmp_path / "p.json")
    tracks = load_all_tracks()
    fund = next(t for t in tracks if t.id == "fundamentos")
    room = fund.rooms[0]
    for task in room.tasks:
        if task.type == "mcq":
            # answer 0-based index → send letter
            from edge_mage.validators import _resolve_mcq_answer

            idx = _resolve_mcq_answer(task)
            ans = chr(ord("A") + idx)
        elif task.type == "numeric":
            ans = str(task.answer)
        elif task.type == "fill":
            ans = task.answers[0]
        else:
            continue
        ok, msg = validate_task(task, ans)
        assert ok, msg
        store.mark_task(fund.id, room.id, task.id, task.xp, room)
    assert store.is_room_done(fund.id, room.id)
    assert store.state.xp >= sum(t.xp for t in room.tasks) + room.xp_reward
