"""Testes das animações matemáticas."""

from __future__ import annotations

from edge_mage.animations.math import (
    animation_for_room,
    available_animations,
    frame_matrix,
    frame_sine_wave,
    frame_unit_circle,
    frame_vector,
    render_frame,
)
from edge_mage.content import load_all_tracks


def test_animation_frames_nonempty() -> None:
    for fn in (frame_unit_circle, frame_sine_wave, frame_vector, frame_matrix):
        out = fn(0.25)
        assert isinstance(out, str)
        assert len(out) > 40
        assert "\n" in out


def test_render_and_kinds() -> None:
    kinds = available_animations()
    assert "unit_circle" in kinds
    assert "vector" in kinds
    for k in kinds:
        assert "θ" in render_frame(k, 0.0) or "v=" in render_frame(k, 0.0) or "A =" in render_frame(
            k, 0.0
        ) or "sin" in render_frame(k, 0.0)


def test_room_animation_mapping() -> None:
    assert animation_for_room("trigonometria", "unit_circle") == "unit_circle"
    assert animation_for_room("vetores") == "vector"
    assert animation_for_room("algebra-linear") == "matrix"
    assert animation_for_room("foo-bar") == "none"

    tracks = load_all_tracks()
    fund = next(t for t in tracks if t.id == "fundamentos")
    trig = next(r for r in fund.rooms if r.id == "trigonometria")
    assert trig.animation == "unit_circle"
    vet = next(r for r in fund.rooms if r.id == "vetores")
    assert vet.animation == "vector"
