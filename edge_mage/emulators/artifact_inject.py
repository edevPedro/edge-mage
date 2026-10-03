"""Artifact overlays for synthetic EEG (blink / EMG / line noise)."""

from __future__ import annotations

import argparse
import math
import random
from typing import Literal

ArtifactKind = Literal["blink", "emg", "line"]


def inject_artifacts(
    block: list[list[float]],
    *,
    fs: float = 250.0,
    kind: ArtifactKind = "blink",
    channel: int = 0,
    start_sample: int = 0,
    duration_samples: int | None = None,
    amplitude: float = 8.0,
    line_hz: float = 60.0,
    seed: int = 1,
) -> list[list[float]]:
    """
    Return a copy of `block` with an educational artifact overlay.

    - blink: slow high-amplitude pulse (EOG-ish)
    - emg: high-frequency burst
    - line: 50/60 Hz sinusoid
    """
    if not block:
        return []
    n = len(block)
    n_ch = len(block[0])
    if channel < 0 or channel >= n_ch:
        raise ValueError("channel out of range")
    out = [list(row) for row in block]
    rng = random.Random(seed)
    dur = duration_samples if duration_samples is not None else max(1, int(0.25 * fs))
    end = min(n, start_sample + dur)

    for i in range(max(0, start_sample), end):
        local = i - start_sample
        if kind == "blink":
            # raised-cosine pulse
            env = 0.5 * (1.0 - math.cos(2 * math.pi * local / max(1, dur)))
            out[i][channel] += amplitude * env
        elif kind == "emg":
            out[i][channel] += amplitude * 0.35 * rng.gauss(0.0, 1.0)
            out[i][channel] += amplitude * 0.15 * math.sin(2 * math.pi * 80.0 * i / fs)
        elif kind == "line":
            out[i][channel] += amplitude * 0.4 * math.sin(2 * math.pi * line_hz * i / fs)
        else:
            raise ValueError(f"unknown artifact kind: {kind}")
    return out


def detect_line_power(block: list[list[float]], channel: int, fs: float, line_hz: float) -> float:
    """Goertzel-ish power at line frequency — student can compare clean vs contaminated."""
    if not block:
        return 0.0
    re = im = 0.0
    n = len(block)
    for i, row in enumerate(block):
        ang = 2 * math.pi * line_hz * i / fs
        x = row[channel]
        re += x * math.cos(ang)
        im += x * math.sin(ang)
    return (re * re + im * im) / max(1, n)


def _demo() -> None:
    from edge_mage.emulators.synth_eeg import SynthEEGStream

    stream = SynthEEGStream(n_channels=2, fs=250.0, seed=3)
    clean = stream.generate(250)
    dirty = inject_artifacts(clean, fs=250.0, kind="line", channel=0, amplitude=6.0, line_hz=60.0)
    p_clean = detect_line_power(clean, 0, 250.0, 60.0)
    p_dirty = detect_line_power(dirty, 0, 250.0, 60.0)
    print("artifact_inject demo (line 60 Hz)")
    print(f"  line_power clean={p_clean:.3f}  dirty={p_dirty:.3f}")
    print(f"  ratio dirty/clean ≈ {p_dirty / max(1e-9, p_clean):.1f}×")


def main(argv: list[str] | None = None) -> None:
    argparse.ArgumentParser(description="Artifact inject demo").parse_args(argv)
    _demo()


if __name__ == "__main__":
    main()
