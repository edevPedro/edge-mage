"""Testes de modos NORMAL/INSERT e navegação vim (sem mouse)."""

from __future__ import annotations

import pytest

from edge_mage.app import EdgeMageApp
from edge_mage.nav import NavMode, is_insert_like, mode_label
from edge_mage.screens.home import HomeScreen
from edge_mage.screens.task import TaskScreen
from edge_mage.screens.tracks import TracksScreen
from edge_mage.widgets.statusline import StatusLine


def test_nav_mode_helpers() -> None:
    assert mode_label(NavMode.NORMAL) == "NORMAL"
    assert mode_label(NavMode.INSERT) == "INSERT"
    assert is_insert_like(NavMode.INSERT)
    assert is_insert_like(NavMode.COMMAND)
    assert not is_insert_like(NavMode.NORMAL)


@pytest.mark.asyncio
async def test_home_jk_and_enter_without_mouse() -> None:
    app = EdgeMageApp()
    async with app.run_test() as pilot:
        assert isinstance(app.screen, HomeScreen)
        assert app.nav_mode == NavMode.NORMAL
        home = app.screen
        lst = home._option_list()
        assert lst is not None
        assert lst.highlighted == 0

        await pilot.press("j")
        assert lst.highlighted == 1
        await pilot.press("k")
        assert lst.highlighted == 0
        await pilot.press("G")
        assert lst.highlighted == lst.option_count - 1
        await pilot.press("g", "g")
        assert lst.highlighted == 0

        # Enter abre trilhas
        await pilot.press("enter")
        assert isinstance(app.screen, TracksScreen)
        tracks = app.screen
        tlist = tracks._option_list()
        assert tlist is not None
        assert tlist.has_focus or tlist.highlighted is not None

        await pilot.press("j")
        assert tlist.highlighted == 1
        await pilot.press("h")  # voltar
        assert isinstance(app.screen, HomeScreen)


@pytest.mark.asyncio
async def test_task_insert_escape_cycle() -> None:
    app = EdgeMageApp()
    async with app.run_test() as pilot:
        # abre fundamentos → primeira sala → primeira task via comandos internos
        fund = next(t for t in app.tracks if t.id == "fundamentos")
        room = next(r for r in fund.rooms if r.id == "trigonometria")
        task = room.tasks[0]
        app.push_screen(TaskScreen(fund, room, task))
        await pilot.pause()

        assert isinstance(app.screen, TaskScreen)
        assert app.nav_mode == NavMode.NORMAL

        await pilot.press("i")
        assert app.nav_mode == NavMode.INSERT
        assert app.screen.is_typing()

        # digitar não deve sair do INSERT / deve ir para o Input
        await pilot.press("1", ".", "5")
        from textual.widgets import Input

        inp = app.screen.query_one("#answer", Input)
        assert "1.5" in inp.value

        await pilot.press("escape")
        assert app.nav_mode == NavMode.NORMAL
        assert not app.screen.is_typing()

        # j/k no menu de ações
        lst = app.screen._option_list()
        assert lst is not None
        start = lst.highlighted or 0
        await pilot.press("j")
        assert lst.highlighted == start + 1


@pytest.mark.asyncio
async def test_statusline_shows_mode() -> None:
    app = EdgeMageApp()
    async with app.run_test() as pilot:
        sl = app.screen.query_one(StatusLine)
        mode_w = sl.query_one("#sl-mode")
        assert "NORMAL" in str(mode_w.render())
        app.enter_insert()
        await pilot.pause()
        assert "INSERT" in str(mode_w.render())
        app.enter_normal()
        await pilot.pause()
        assert "NORMAL" in str(mode_w.render())


@pytest.mark.asyncio
async def test_leader_gt_tracks() -> None:
    app = EdgeMageApp()
    async with app.run_test() as pilot:
        await pilot.press("g", "t")
        assert isinstance(app.screen, TracksScreen)
        assert app.nav_mode == NavMode.NORMAL
