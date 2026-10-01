"""Systems Mage pack load + room-count sanity."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from edge_mage.content import load_tracks_for_course
from edge_mage.courses import COURSE_SYSTEMS
from edge_mage.packs import (
    MIN_SYSTEMS_FLAG_ROOMS,
    bundled_systems_pack_path,
    load_systems_pack_data,
    pack_room_count,
    seed_systems_pack,
    write_systems_pack,
)
from edge_mage.validators import validate_task
from edge_mage.models import Task


def test_bundled_systems_pack_exists_and_is_full() -> None:
    path = bundled_systems_pack_path()
    assert path.exists(), "content/packs/systems.json missing — run edevs export script"
    data = json.loads(path.read_text(encoding="utf-8"))
    rooms = data.get("rooms") or []
    assert data.get("course") == "systems"
    assert data.get("version") == 1
    assert set(data.get("sourceTracks") or []) == {"systems", "llvm", "math"}
    assert len(rooms) >= MIN_SYSTEMS_FLAG_ROOMS
    assert data.get("roomCount") == len(rooms)
    # Every FLAG room should be playable (fill task or pattern)
    with_tasks = [r for r in rooms if r.get("tasks")]
    assert len(with_tasks) >= MIN_SYSTEMS_FLAG_ROOMS
    sample = next(r for r in rooms if r["id"] == "sys-memory")
    assert sample["tasks"][0]["type"] == "fill"
    assert "FLAG" in str(sample["tasks"][0].get("answer") or "")


def test_load_systems_course_has_many_rooms(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MAGE_HOME", str(tmp_path / "mage"))
    tracks = load_tracks_for_course(COURSE_SYSTEMS)
    assert len(tracks) >= 3  # systems, llvm, math (+ craft)
    ids = {t.id for t in tracks}
    assert {"systems", "llvm", "math"} <= ids
    total = sum(len(t.rooms) for t in tracks)
    # shared cores + 82 FLAG + craft rooms
    assert total >= MIN_SYSTEMS_FLAG_ROOMS
    all_ids = {r.id for t in tracks for r in t.rooms}
    assert "sys-memory" in all_ids
    assert "llvm-langref" in all_ids or "llvm-overview" in all_ids
    assert "math-vectors" in all_ids
    assert "systems-boss-craft" in all_ids
    assert "shared-math-evidence" in all_ids
    assert "flag-hello" not in all_ids  # stub superseded by full pack


def test_seed_and_write_pack(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MAGE_HOME", str(tmp_path / "mage"))
    dest = seed_systems_pack(force=True)
    assert dest is not None and dest.exists()
    assert pack_room_count() >= MIN_SYSTEMS_FLAG_ROOMS

    # Catalog envelope → flat pack
    envelope = {
        "version": 1,
        "systemsMagePack": json.loads(bundled_systems_pack_path().read_text(encoding="utf-8")),
    }
    written = write_systems_pack(envelope)
    data = json.loads(written.read_text(encoding="utf-8"))
    assert len(data["rooms"]) >= MIN_SYSTEMS_FLAG_ROOMS


def test_flag_fill_and_regex_tasks() -> None:
    exact = Task(
        id="flag",
        type="fill",
        prompt="FLAG?",
        answer="FLAG{heap:malloc}",
    )
    ok, _ = validate_task(exact, "FLAG{heap:malloc}")
    assert ok
    ok, _ = validate_task(exact, "flag{heap:malloc}")
    assert ok

    regex = Task(
        id="flag",
        type="fill",
        prompt="FLAG?",
        answer_pattern=r"^FLAG\{(aarch64:x0|x86_64:rax)\}$",
    )
    ok, _ = validate_task(regex, "FLAG{aarch64:x0}")
    assert ok
    ok, _ = validate_task(regex, "FLAG{nope}")
    assert not ok


def test_load_systems_pack_data_reads_bundle(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MAGE_HOME", str(tmp_path / "mage"))
    data, path = load_systems_pack_data()
    assert path.exists()
    assert len(data.get("rooms") or []) >= MIN_SYSTEMS_FLAG_ROOMS
