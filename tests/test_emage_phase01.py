"""Phase 0–1: launcher, path migration, global ranks, courses, sync stub."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from edge_mage.app import EdgeMageApp
from edge_mage.auth import start_github_device_flow
from edge_mage.content import load_tracks_for_course
from edge_mage.courses import COURSE_EDGE, COURSE_FUNDAMENTALS, COURSE_SYSTEMS
from edge_mage.paths import mage_home, packs_dir, progress_path
from edge_mage.progress import ProgressStore
from edge_mage.ranks import global_rank_from_flags
from edge_mage.screens.launcher import LauncherScreen
from edge_mage.sync import progress_to_api_payload, pull_catalog


def test_path_migration(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    # force paths to use HOME (no MAGE_HOME)
    monkeypatch.delenv("MAGE_HOME", raising=False)

    legacy = home / ".edge-mage"
    legacy.mkdir()
    (legacy / "progress.json").write_text('{"xp": 42, "version": 3}\n', encoding="utf-8")

    # re-import path helpers under new HOME
    from edge_mage import paths as paths_mod

    mh = paths_mod.mage_home()
    assert mh == home / ".mage"
    assert (mh / "progress.json").exists()
    data = json.loads((mh / "progress.json").read_text(encoding="utf-8"))
    assert data["xp"] == 42


def test_progress_shared_room_credit(tmp_path: Path) -> None:
    store = ProgressStore(tmp_path / "p.json")
    store.mark_room_id("vectors")
    store.save()
    assert store.is_room_done("systems", "vectors")
    assert store.is_room_done("fundamentals", "vectors")


def test_fundamentals_and_systems_load() -> None:
    fund = load_tracks_for_course(COURSE_FUNDAMENTALS)
    assert fund and fund[0].rooms
    ids = {r.id for r in fund[0].rooms}
    assert {"vectors", "bits", "intro-asm", "fundamentals-clear"} <= ids

    sys_tracks = load_tracks_for_course(COURSE_SYSTEMS)
    assert sys_tracks and sys_tracks[0].rooms
    sys_ids = {r.id for r in sys_tracks[0].rooms}
    assert "flag-hello" in sys_ids or "systems-boss-craft" in sys_ids
    assert "vectors" in sys_ids  # shared core merged

    edge = load_tracks_for_course(COURSE_EDGE)
    assert len(edge) >= 8


def test_global_ranks() -> None:
    assert global_rank_from_flags(has_mago_base=False).id == "none"
    assert global_rank_from_flags(has_mago_base=True).id == "mago_base"
    assert global_rank_from_flags(
        has_mago_base=True, any_advanced_progress=True
    ).id == "intermediate"
    assert (
        global_rank_from_flags(
            has_mago_base=True,
            has_systems_boss=True,
            has_edge_on_device=True,
            has_evidence=True,
        ).id
        == "mago_supremo"
    )


def test_auth_and_sync_stubs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MAGE_HOME", str(tmp_path / "mage"))
    monkeypatch.delenv("MAGE_GITHUB_CLIENT_ID", raising=False)
    flow = start_github_device_flow()
    assert flow.stub
    assert (tmp_path / "mage" / "auth.json").exists()

    result = pull_catalog(course="systems")
    assert result.ok
    assert (tmp_path / "mage" / "packs" / "systems.json").exists()

    payload = progress_to_api_payload(
        {
            "xp": 10,
            "completed_rooms_by_id": {"vectors": True},
            "completed_rooms": {"fundamentos/trigonometria": True},
            "last_active": "2026-10-01",
        }
    )
    assert "vectors" in payload["readAt"]
    assert "trigonometria" in payload["readAt"]
    assert "tui" in payload


@pytest.mark.asyncio
async def test_launcher_opens_first() -> None:
    app = EdgeMageApp(show_launcher=True)
    async with app.run_test() as pilot:
        assert isinstance(app.screen, LauncherScreen)
        lst = app.screen._option_list()
        assert lst is not None
        assert lst.option_count >= 4
