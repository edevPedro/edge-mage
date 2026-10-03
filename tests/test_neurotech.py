"""Neurotech course load, pedagogical path, emulators, animations."""

from __future__ import annotations

from edge_mage.animations.math import animation_for_room, render_frame
from edge_mage.content import load_tracks_for_course
from edge_mage.courses import COURSE_EDGE, COURSE_NEUROTECH, COURSES
from edge_mage.emulators import (
    CortexMPipelineStub,
    SynthEEGStream,
    inject_artifacts,
    run_online_stub,
    stage_budget,
)
from edge_mage.emulators.artifact_inject import detect_line_power
from edge_mage.models import Task, Track
from edge_mage.progress import ProgressStore
from edge_mage.validators import validate_task

# Locked pedagogical chain (F2 acquisition + decode + F6 gates).
PEDAGOGICAL_IDS = [
    "nt-portal",
    "nt-ethics-consent",
    "nt-dipole-scalp",
    "nt-spike-lfp",
    "nt-volume-blur",
    "nt-electrode-snr",
    "nt-ground-ref",
    "nt-adc-bio",
    "nt-rhythms",
    "nt-filter-bank",
    "nt-mi-paradigm",
    "nt-artifacts",
    "nt-features-bandpower",
    "nt-decode-mvp",
    "nt-riemann-primer",
    "nt-metrics-offline",
    "nt-stream-buffer",
    "nt-mcu-filter",
    "nt-latency-budget",
    "nt-online-stub",
    "nt-checkpoint-paper",
    "nt-checkpoint-project",
    "nt-neuro-mage",
]


def _neuro_track() -> Track:
    tracks = load_tracks_for_course(COURSE_NEUROTECH)
    assert len(tracks) == 1
    return tracks[0]


def test_neurotech_in_catalog() -> None:
    assert any(c.id == COURSE_NEUROTECH for c in COURSES)


def test_neurotech_pedagogical_order_locked() -> None:
    track = _neuro_track()
    ids = [r.id for r in track.rooms]
    assert ids == PEDAGOGICAL_IDS
    assert [r.order for r in track.rooms] == list(range(1, 24))


def test_f2_requires_rooms_chain() -> None:
    track = _neuro_track()
    by_id = {r.id: r for r in track.rooms}
    assert by_id["nt-ground-ref"].requires_rooms == ["nt-electrode-snr"]
    assert by_id["nt-adc-bio"].requires_rooms == ["nt-ground-ref"]
    assert by_id["nt-rhythms"].requires_rooms == ["nt-adc-bio"]
    assert set(by_id["nt-filter-bank"].requires_rooms) == {
        "nt-rhythms",
        "nt-adc-bio",
    }
    assert "nt-filter-bank" in by_id["nt-mi-paradigm"].requires_rooms


def test_f6_gates_online_xor_boss() -> None:
    track = _neuro_track()
    by_id = {r.id: r for r in track.rooms}
    assert by_id["nt-checkpoint-paper"].requires_rooms == ["nt-online-stub"]
    assert by_id["nt-checkpoint-project"].requires_rooms == ["nt-online-stub"]
    boss = by_id["nt-neuro-mage"]
    assert boss.requires_rooms == ["nt-online-stub"]
    assert set(boss.requires_rooms_any) == {
        "nt-checkpoint-paper",
        "nt-checkpoint-project",
    }


def test_requires_rooms_enforced_in_unlock(tmp_path) -> None:
    track = _neuro_track()
    store = ProgressStore(tmp_path / "neuro-progress.json")
    # Fresh store: only portal (no requires) should unlock among early rooms
    portal = next(r for r in track.rooms if r.id == "nt-portal")
    ethics = next(r for r in track.rooms if r.id == "nt-ethics-consent")
    ground = next(r for r in track.rooms if r.id == "nt-ground-ref")
    assert store.is_room_unlocked(track, portal)
    assert not store.is_room_unlocked(track, ethics)
    store.state.completed_rooms_by_id["nt-portal"] = True
    assert store.is_room_unlocked(track, ethics)
    assert not store.is_room_unlocked(track, ground)

    # Boss needs online + (paper OR project)
    boss = next(r for r in track.rooms if r.id == "nt-neuro-mage")
    store.state.completed_rooms_by_id["nt-online-stub"] = True
    assert not store.is_room_unlocked(track, boss)
    store.state.completed_rooms_by_id["nt-checkpoint-paper"] = True
    assert store.is_room_unlocked(track, boss)


def test_edge_excludes_neurotech_track() -> None:
    edge = load_tracks_for_course(COURSE_EDGE)
    assert all(t.id != "neurotech" for t in edge)
    assert all(t.course != COURSE_NEUROTECH for t in edge)


def test_synth_eeg_and_artifacts() -> None:
    stream = SynthEEGStream(n_channels=2, fs=250.0, seed=1)
    stream.schedule_mu_burst(
        start_sample=10, duration_samples=50, channel=0, amplitude=15.0, freq_hz=10.0
    )
    stream.schedule_mu_suppression(
        start_sample=80, duration_samples=40, channel=0, factor=0.2
    )
    block = stream.generate(200)
    assert len(block) == 200
    assert len(block[0]) == 2
    assert max(abs(row[0]) for row in block) > 2.0
    bp = stream.bandpower_proxy(block, 0, 8.0, 12.0)
    assert bp > 0

    dirty = inject_artifacts(block, fs=250.0, kind="line", channel=0, amplitude=8.0)
    assert detect_line_power(dirty, 0, 250.0, 60.0) > detect_line_power(
        block, 0, 250.0, 60.0
    )


def test_cortex_m_stub_pipeline() -> None:
    mcu = CortexMPipelineStub(deadline_ms=40.0)
    result = mcu.process_window([0.1 * i for i in range(32)], taps=5)
    assert "packet_hex" in result
    assert result["buffer_fill"] == 32
    assert mcu.packets_sent == 1
    assert result["window_ms"] == 128.0
    assert result["compute_ms"] < result["window_ms"]
    assert result["latency_ms"] == result["window_ms"] + result["compute_ms"]
    assert result["miss"] is True
    assert "not QEMU" in result["runtime_note"]


def test_latency_budget_and_online_loop() -> None:
    report = stage_budget(128.0, 3.0, 5.0, deadline_ms=40.0)
    assert report["miss"] is True
    assert report["sense_ms"] == 128.0
    out = run_online_stub(n_windows=4, deadline_ms=150.0)
    assert out["n_windows"] == 4
    assert len(out["log"]) == 4
    assert out["log"][0]["label"] in {"left", "right"}


def test_neuro_animations_render() -> None:
    for kind in (
        "rhythm_bands",
        "filter_freq_response",
        "dipole_field",
        "spike_to_lfp",
        "mi_erds",
        "closed_loop_timeline",
        "volume_blur",
        "artifact_trace",
    ):
        assert animation_for_room("nt-x", kind) == kind
        frame = render_frame(kind, 0.25)
        assert len(frame) > 20
    # ERS rebound claim must match animation content
    assert "ERS↑" in render_frame("mi_erds", 0.1)
    assert "acima" in render_frame("mi_erds", 0.1)
    assert "FEM" in render_frame("volume_blur", 0.1)
    assert "ritmos" in render_frame("artifact_trace", 0.1).lower() or "artefato" in render_frame(
        "artifact_trace", 0.1
    ).lower()


def test_filter_bank_code_task() -> None:
    room = next(r for r in _neuro_track().rooms if r.id == "nt-filter-bank")
    task = next(t for t in room.tasks if t.id == "band-mask")
    code = "def band_mask(freqs, lo, hi):\n    return [lo <= f < hi for f in freqs]\n"
    ok, msg = validate_task(task, code)
    assert ok, msg


def test_decode_mvp_lda_code_task() -> None:
    room = next(r for r in _neuro_track().rooms if r.id == "nt-decode-mvp")
    task = next(t for t in room.tasks if t.id == "lda-code")
    code = (
        "def predict_lda(x, w, b):\n"
        "    s = sum(a * b_ for a, b_ in zip(x, w)) + b\n"
        "    return 1 if s >= 0 else 0\n"
    )
    ok, msg = validate_task(task, code)
    assert ok, msg


def test_ring_buffer_code_task() -> None:
    room = next(r for r in _neuro_track().rooms if r.id == "nt-stream-buffer")
    task = next(t for t in room.tasks if t.id == "ring-code")
    code = """
class RingBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = []
    def push(self, x):
        self.data.append(x)
        if len(self.data) > self.capacity:
            self.data = self.data[-self.capacity:]
    def latest(self, n):
        return self.data[-n:] if n < len(self.data) else list(self.data)
"""
    ok, msg = validate_task(Task(**{**task.__dict__}), code) if False else validate_task(task, code)
    assert ok, msg


def test_substantive_rooms_have_http_resources() -> None:
    """Every room from F1 onward should cite at least one real http(s) URL."""
    track = _neuro_track()
    for room in track.rooms:
        if room.order < 3:
            continue
        assert room.resources, f"{room.id} missing resources"
        assert any(r.url.startswith("http") for r in room.resources), room.id
