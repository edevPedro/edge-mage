"""Testes de painéis Ctrl+w, grimório e story/concept."""

from __future__ import annotations

from pathlib import Path

import pytest

from edge_mage.app import EdgeMageApp
from edge_mage.content import load_all_tracks
from edge_mage.grimoire import load_skills, skills_for_room
from edge_mage.nav import NavMode
from edge_mage.progress import ProgressStore
from edge_mage.screens.grimoire import GrimoireScreen
from edge_mage.screens.room import RoomScreen
from edge_mage.widgets.statusline import StatusLine


def test_all_rooms_have_story_and_concept() -> None:
    tracks = load_all_tracks()
    for t in tracks:
        for r in t.rooms:
            assert r.story_md.strip(), f"sem história: {t.id}/{r.id}"
            assert r.concept_md.strip(), f"sem conceito: {t.id}/{r.id}"
            assert r.lesson_md.strip(), f"sem lição: {t.id}/{r.id}"


def test_skills_yaml_covers_rooms() -> None:
    skills = load_skills()
    assert len(skills) >= 20
    tracks = load_all_tracks()
    room_ids = {r.id for t in tracks for r in t.rooms}
    skill_rooms = {s.unlock_room for s in skills}
    missing = room_ids - skill_rooms
    assert not missing, f"salas sem skill: {missing}"


def test_grimoire_unlock_on_room_complete(tmp_path: Path) -> None:
    store = ProgressStore(tmp_path / "p.json")
    tracks = load_all_tracks()
    skills = load_skills()
    fund = next(t for t in tracks if t.id == "fundamentos")
    room = next(r for r in fund.rooms if r.id == "trigonometria")
    from edge_mage.validators import validate_task

    for task in room.tasks:
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
        res = store.mark_task(fund.id, room.id, task.id, task.xp, room)
        if res.get("room_completed"):
            granted = skills_for_room(skills, track_id=fund.id, room_id=room.id)
            newly = store.unlock_skills([s.id for s in granted])
            store.save()
            assert newly
            assert store.is_skill_unlocked("trig-arcana")
    assert store.is_room_done(fund.id, room.id)
    assert store.is_skill_unlocked("trig-arcana")


@pytest.mark.asyncio
async def test_ctrl_w_cycles_panes() -> None:
    app = EdgeMageApp()
    async with app.run_test() as pilot:
        fund = next(t for t in app.tracks if t.id == "fundamentos")
        room = next(r for r in fund.rooms if r.id == "trigonometria")
        app.push_screen(RoomScreen(fund, room))
        await pilot.pause()

        screen = app.screen
        assert isinstance(screen, RoomScreen)
        assert screen.focused_pane == "story"
        assert "story" in screen.pane_ids
        assert "concept" in screen.pane_ids
        assert "tasks" in screen.pane_ids

        # Ctrl+w → WINDOW, then w cycles
        await pilot.press("ctrl+w")
        assert app.nav_mode == NavMode.WINDOW
        await pilot.press("w")
        assert app.nav_mode == NavMode.NORMAL
        assert screen.focused_pane == "concept"

        await pilot.press("ctrl+w")
        await pilot.press("l")
        assert screen.focused_pane == "desafio"

        sl = screen.query_one(StatusLine)
        ctx = str(sl.query_one("#sl-ctx").render())
        assert "DESAFIO" in ctx or "desafio" in ctx.lower() or "CONCEITO" in ctx or "HISTÓRIA" in ctx or "DESAFIO" in ctx


@pytest.mark.asyncio
async def test_grimoire_screen_opens() -> None:
    app = EdgeMageApp()
    async with app.run_test() as pilot:
        await pilot.press("g", "r")
        assert isinstance(app.screen, GrimoireScreen)
        assert app.nav_mode == NavMode.NORMAL
