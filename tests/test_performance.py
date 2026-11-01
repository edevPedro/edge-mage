"""Performance Mage course wiring + pedagogical order."""

from __future__ import annotations

from edge_mage.content import (
    load_all_tracks,
    load_performance_tracks,
    load_tracks_for_course,
)
from edge_mage.courses import COURSE_EDGE, COURSE_PERFORMANCE, COURSES

PEDAGOGICAL_IDS = [
    "pf-portal",
    "pf-pipeline",
    "pf-cache-vm",
    "pf-aarch64-perf",
    "pf-neon-intro",
    "pf-simd-tiling",
    "pf-counters",
    "pf-boss-arm-math",
    "pf-nla-ieee",
    "pf-roofline",
    "pf-gemm-jacobi",
    "pf-boss-physics",
    "pf-metal-intro",
    "pf-gpu-kernels",
    "pf-cuda-elective",
    "pf-boss-metal",
    "pf-inference-bridge",
    "pf-rtl-intro",
    "pf-hls-lite",
    "pf-boss-accelerator",
]

BOSS_IDS = {
    "pf-boss-arm-math",
    "pf-boss-physics",
    "pf-boss-metal",
    "pf-boss-accelerator",
}

PILLAR_FIRST_ROOMS = {
    "architecture": "pf-pipeline",
    "neon": "pf-neon-intro",
    "numerical": "pf-nla-ieee",
    "gpu": "pf-metal-intro",
    "codesign": "pf-rtl-intro",
}


def _perf_track():
    tracks = load_performance_tracks()
    assert len(tracks) == 1
    assert tracks[0].id == "performance"
    assert tracks[0].course == COURSE_PERFORMANCE
    return tracks[0]


def test_performance_in_catalog() -> None:
    assert any(c.id == COURSE_PERFORMANCE for c in COURSES)
    info = next(c for c in COURSES if c.id == COURSE_PERFORMANCE)
    assert info.requires_mago_base is True
    assert "soft" in info.blurb.lower() or "Edge" in info.blurb


def test_performance_track_loads_and_order() -> None:
    track = _perf_track()
    ids = [r.id for r in track.rooms]
    assert ids == PEDAGOGICAL_IDS
    assert [r.order for r in track.rooms] == list(range(1, 21))
    assert len(track.rooms) == 20


def test_performance_bosses_and_pillars() -> None:
    track = _perf_track()
    by_id = {r.id: r for r in track.rooms}
    for bid in BOSS_IDS:
        assert by_id[bid].boss is True
        assert by_id[bid].concept_md.strip()
        assert by_id[bid].lesson_md.strip()
        assert len(by_id[bid].tasks) >= 2
        blob = (by_id[bid].concept_md + by_id[bid].lesson_md).lower()
        assert "golden" in blob or "correção" in blob or "correcao" in blob or "tolerância" in blob or "tolerancia" in blob
    for pillar, rid in PILLAR_FIRST_ROOMS.items():
        room = by_id[rid]
        assert room.concept_md.strip(), f"{rid} missing concept"
        assert room.story_md.strip(), f"{rid} missing story"
        assert len(room.concept_md) > 400, f"{rid} Estuda too thin for pillar {pillar}"


def test_requires_rooms_chain() -> None:
    track = _perf_track()
    by_id = {r.id: r for r in track.rooms}
    assert by_id["pf-pipeline"].requires_rooms == ["pf-portal"]
    assert by_id["pf-boss-arm-math"].requires_rooms == ["pf-counters"]
    assert by_id["pf-inference-bridge"].requires_rooms == ["pf-boss-metal"]
    # CUDA elective does not block Metal boss
    assert "pf-cuda-elective" not in by_id["pf-boss-metal"].requires_rooms


def test_edge_excludes_performance_track() -> None:
    edge = load_tracks_for_course(COURSE_EDGE)
    assert all(t.id != "performance" for t in edge)
    assert all(t.course != COURSE_PERFORMANCE for t in edge)
    all_default = load_all_tracks()
    assert all(t.id != "performance" for t in all_default)


def test_load_tracks_for_course_performance() -> None:
    tracks = load_tracks_for_course(COURSE_PERFORMANCE)
    assert len(tracks) == 1
    assert tracks[0].rooms[0].id == "pf-portal"
    # Soft modular note: inference bridge exists but course is separate from edge
    ids = {r.id for r in tracks[0].rooms}
    assert "pf-inference-bridge" in ids
