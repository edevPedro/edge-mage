"""Tests for signal_viz: ASCII EEG waveforms, PSD spectrum, and bandpower."""

from __future__ import annotations

import math
from edge_mage.emulators.signal_viz import (
    compute_bandpowers,
    compute_simple_psd,
    render_ascii_spectrogram,
    render_ascii_spectrum,
    render_ascii_wave,
    render_bandpower_bars,
    render_multichannel_waves,
)


def test_render_ascii_wave_basic() -> None:
    # 1 second of 10 Hz sine at 250 Hz
    t = [i / 250.0 for i in range(250)]
    sine = [10.0 * math.sin(2.0 * math.pi * 10.0 * ti) for ti in t]

    plot = render_ascii_wave(sine, width=50, height=7, title="10 Hz Sine", unit="µV")
    assert "10 Hz Sine" in plot
    assert "µV" in plot
    assert "0 ms" in plot
    assert "1000 ms" in plot
    assert "●" in plot
    lines = plot.splitlines()
    assert len(lines) >= 8


def test_render_ascii_wave_empty() -> None:
    plot = render_ascii_wave([])
    assert "vazio" in plot.lower()


def test_render_multichannel_waves() -> None:
    ch1 = [math.sin(i * 0.1) for i in range(100)]
    ch2 = [math.cos(i * 0.1) for i in range(100)]
    channels = {"C3": ch1, "Cz": ch2}

    res = render_multichannel_waves(channels, width=40, height_per_ch=3)
    assert "C3" in res
    assert "Cz" in res
    assert "2 canais" in res
    assert "ms" in res


def test_compute_simple_psd_detects_peak() -> None:
    # 250 Hz sample rate, 2 seconds
    fs = 250.0
    n = 500
    # 10 Hz pure sine wave
    sig = [20.0 * math.sin(2.0 * math.pi * 10.0 * (i / fs)) for i in range(n)]

    freqs, psd_db = compute_simple_psd(sig, fs=fs, n_fft=128)
    assert len(freqs) == len(psd_db)
    assert len(freqs) == 65  # 128 / 2 + 1

    # Find peak frequency
    max_idx = max(range(len(psd_db)), key=lambda i: psd_db[i])
    peak_f = freqs[max_idx]
    # Peak should be around 10 Hz (within resolution of ~1.95 Hz)
    assert abs(peak_f - 10.0) < 2.0


def test_compute_bandpowers_identifies_alpha_peak() -> None:
    fs = 250.0
    sig = [15.0 * math.sin(2.0 * math.pi * 10.0 * (i / fs)) for i in range(500)]
    freqs, psd_db = compute_simple_psd(sig, fs=fs, n_fft=128)
    bands = compute_bandpowers(freqs, psd_db)

    assert "alpha" in bands
    assert "delta" in bands
    assert "beta" in bands
    # Alpha power should be significantly higher than gamma and delta
    assert bands["alpha"] > bands["gamma"]
    assert bands["alpha"] > bands["delta"]


def test_render_ascii_spectrum() -> None:
    freqs = [float(i) for i in range(50)]
    psd_db = [-30.0 + (20.0 if 9 <= i <= 11 else 0.0) for i in range(50)]

    plot = render_ascii_spectrum(freqs, psd_db, width=40, height=6, max_freq_hz=45.0)
    assert "PSD" in plot or "Espectral" in plot
    assert "dB" in plot
    assert "Hz" in plot
    assert "█" in plot


def test_render_bandpower_bars() -> None:
    powers = {"delta": -30.0, "theta": -20.0, "alpha": -5.0, "beta": -25.0, "gamma": -45.0}
    bars = render_bandpower_bars(powers, width=20)
    assert "α/µ" in bars
    assert "★" in bars  # star on maximum (alpha)
    assert "dB" in bars


def test_render_ascii_spectrogram() -> None:
    # 5 frequency rows, 10 time columns
    matrix = [[float(r * c) for c in range(10)] for r in range(5)]
    res = render_ascii_spectrogram(matrix, freqs=[5.0, 10.0, 15.0, 20.0, 25.0], width=30, height=5)
    assert "Espectrograma" in res
    assert "t=0" in res
    assert "Hz" in res
