"""Testes da tela HOJE (TUI) ligada ao motor do roadmap."""

from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import OptionList

from edge_mage.app import EdgeMageApp
from edge_mage.screens.today import TodayScreen
from edge_mage.widgets.wave import MetricStrip, SparklineBlock, WaveBlock


@pytest.fixture()
def isolated_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    home = tmp_path / "mage-home"
    monkeypatch.setenv("MAGE_HOME", str(home))
    work = tmp_path / "work"
    monkeypatch.setenv("MAGE_WORK_ROOT", str(work))
    return home


@pytest.mark.asyncio
async def test_today_screen_shows_active_challenge(isolated_home: Path) -> None:
    app = EdgeMageApp(course="edge", show_launcher=False)
    async with app.run_test() as pilot:
        app.push_screen(TodayScreen())
        await pilot.pause()
        assert isinstance(app.screen, TodayScreen)
        screen = app.screen
        assert screen._ctx is not None
        # primeiro desafio do tronco
        assert screen._ctx.challenge.id == "c01-spsc-ring"
        goal = screen.query_one("#today-goal", WaveBlock)
        assert "c01-spsc-ring" in goal.plain_text
        assert isinstance(screen.query_one("#today-metrics", MetricStrip), MetricStrip)
        assert isinstance(screen.query_one("#today-spark", SparklineBlock), SparklineBlock)
        lst = screen.query_one("#today-actions", OptionList)
        assert lst.option_count >= 4


@pytest.mark.asyncio
async def test_leader_g_o_opens_today(isolated_home: Path) -> None:
    app = EdgeMageApp(course="edge", show_launcher=False)
    async with app.run_test() as pilot:
        await pilot.press("g", "o")
        await pilot.pause()
        assert isinstance(app.screen, TodayScreen)


@pytest.mark.asyncio
async def test_colon_today_opens_screen(isolated_home: Path) -> None:
    app = EdgeMageApp(course="edge", show_launcher=False)
    async with app.run_test() as pilot:
        app.dispatch_colon(":today")
        await pilot.pause()
        assert isinstance(app.screen, TodayScreen)


@pytest.mark.asyncio
async def test_close_without_evidence_warns(isolated_home: Path) -> None:
    app = EdgeMageApp(course="edge", show_launcher=False)
    async with app.run_test() as pilot:
        app.push_screen(TodayScreen())
        await pilot.pause()
        screen = app.screen
        # sem evidência PASS, fechar não conclui
        inp = screen.query_one("#today-explain")
        inp.value = "a; b; c"
        screen.on_input_submitted(  # type: ignore[attr-defined]
            type("E", (), {"input": inp, "value": "a; b; c"})()
        )
        await pilot.pause()
        assert not screen._state.days
