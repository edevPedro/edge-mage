"""Neurotech course load, emulators, animations."""

from __future__ import annotations

from edge_mage.animations.math import animation_for_room, render_frame
from edge_mage.content import load_tracks_for_course
from edge_mage.courses import COURSE_EDGE, COURSE_NEUROTECH, COURSES
from edge_mage.emulators import CortexMPipelineStub, SynthEEGStream, inject_artifacts
from edge_mage.emulators.artifact_inject import detect_line_power
from edge_mage.validators import validate_task
from edge_mage.models import Task


def test_neurotech_in_catalog() -> None:
    assert any(c.id == COURSE_NEUROTECH for c in COURSES)


def test_neurotech_track_loads_22_rooms() -> None:
    tracks = load_tracks_for_course(COURSE_NEUROTECH)
    assert len(tracks) == 1
    assert tracks[0].id == "neurotech"
    ids = [r.id for r in tracks[0].rooms]
    assert len(ids) == 22
    assert ids[0] == "nt-portal"
    assert ids[-1] == "nt-neuro-mage"
    assert "nt-filter-bank" in ids
    assert "nt-stream-buffer" in ids


def test_edge_excludes_neurotech_track() -> None:
    edge = load_tracks_for_course(COURSE_EDGE)
    assert all(t.id != "neurotech" for t in edge)
    assert all(t.course != COURSE_NEUROTECH for t in edge)


def test_synth_eeg_and_artifacts() -> None:
    stream = SynthEEGStream(n_channels=2, fs=250.0, seed=1)
    stream.schedule_mu_burst(
        start_sample=10, duration_samples=50, channel=0, amplitude=4.0, freq_hz=10.0
    )
    block = stream.generate(200)
    assert len(block) == 200
    assert len(block[0]) == 2
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


def test_neuro_animations_render() -> None:
    for kind in (
        "rhythm_bands",
        "filter_freq_response",
        "dipole_field",
        "spike_to_lfp",
        "mi_erds",
        "closed_loop_timeline",
        "volume_blur",
    ):
        assert animation_for_room("nt-x", kind) == kind
        frame = render_frame(kind, 0.25)
        assert len(frame) > 20


def test_filter_bank_code_task() -> None:
    tracks = load_tracks_for_course(COURSE_NEUROTECH)
    room = next(r for t in tracks for r in t.rooms if r.id == "nt-filter-bank")
    task = next(t for t in room.tasks if t.id == "band-mask")
    code = "def band_mask(freqs, lo, hi):\n    return [lo <= f < hi for f in freqs]\n"
    ok, msg = validate_task(task, code)
    assert ok, msg


def test_ring_buffer_code_task() -> None:
    tracks = load_tracks_for_course(COURSE_NEUROTECH)
    room = next(r for t in tracks for r in t.rooms if r.id == "nt-stream-buffer")
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
