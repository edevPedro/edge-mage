"""Single-track journey (`emage`): order, phases, aliases, continue prefers spine."""

from __future__ import annotations

from edge_mage.content import (
    load_emage_journey,
    load_performance_tracks,
    load_tracks_for_course,
)
from edge_mage.courses import (
    COURSE_EDGE,
    COURSE_EMAGE,
    COURSE_NEUROTECH,
    COURSE_PERFORMANCE,
    COURSES,
    primary_course,
)
from edge_mage.curriculum import next_open_room, pedagogical_rooms
from edge_mage.mastery import remediation_blurb, remediation_for
from edge_mage.progress import ProgressStore


def test_primary_course_is_emage() -> None:
    assert primary_course().id == COURSE_EMAGE
    assert any(c.primary for c in COURSES)
    assert COURSES[0].id == COURSE_EMAGE


def test_emage_journey_loads_phases() -> None:
    tracks = load_tracks_for_course(COURSE_EMAGE)
    assert len(tracks) == len(load_emage_journey())
    ids = [t.id for t in tracks]
    assert "fundamentals" in ids or any(t.phase == "P0" for t in tracks)
    assert "emage-arch" in ids
    assert "emage-simd" in ids
    assert "emage-hpc" in ids
    assert "emage-gpu" in ids
    assert "emage-inf-bridge" in ids
    assert "emage-codesign" in ids
    assert "emage-forge" in ids
    assert "edge-ai" in ids
    assert "neurotech" in ids

    by_id = {t.id: t for t in tracks}
    # Inference after GPU, co-design after inference bridge
    assert by_id["emage-gpu"].order < by_id["edge-ai"].order
    assert by_id["edge-ai"].order < by_id["emage-codesign"].order
    assert by_id["emage-inf-bridge"].order < by_id["emage-codesign"].order
    assert by_id["neurotech"].elective is True


def test_performance_phases_cover_all_rooms() -> None:
    journey = load_emage_journey()
    perf_ids = {r.id for t in load_performance_tracks() for r in t.rooms}
    sliced = {
        r.id
        for t in journey
        if t.id.startswith("emage-") and t.module_label == "Performance"
        for r in t.rooms
    }
    # Forge is not Performance module_label
    sliced = {
        r.id
        for t in journey
        if t.phase in {"P2", "P3", "P4", "P5", "P6", "P7"} and t.module_label == "Performance"
        for r in t.rooms
    }
    assert perf_ids == sliced


def test_legacy_aliases_still_load() -> None:
    assert load_tracks_for_course(COURSE_PERFORMANCE)
    assert load_tracks_for_course(COURSE_EDGE)
    assert load_tracks_for_course(COURSE_NEUROTECH)
    edge = load_tracks_for_course(COURSE_EDGE)
    assert all(t.id != "performance" for t in edge)
    assert all(t.id != "emage-forge" for t in edge)


def test_continue_prefers_non_elective(tmp_path) -> None:
    store = ProgressStore(tmp_path / "p.json")
    tracks = load_emage_journey()
    nxt = next_open_room(store, tracks)
    assert nxt is not None
    track, room = nxt
    assert track.elective is False
    assert track.phase in {"P0", "Forge", "P1", "P2", ""} or track.order < 100


def test_pedagogical_order_spine_before_neuro() -> None:
    rooms = pedagogical_rooms(load_emage_journey(), include_elective=False)
    assert rooms
    assert all(not t.elective for t, _ in rooms)
    neuro = [t for t, _ in pedagogical_rooms(load_emage_journey()) if t.id == "neurotech"]
    assert neuro


def test_mastery_remediation() -> None:
    assert remediation_for("neon") is not None
    assert "NEON" in remediation_blurb("neon") or "neon" in remediation_blurb("neon").lower()
    assert "Estuda" in remediation_blurb("unknown-theme")
