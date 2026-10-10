"""Bridge helpers for correlated spikes+LFP (educational)."""
from __future__ import annotations

from typing import Dict

from .spike_stream import SpikeStream, SpikeStreamConfig


def synth_spike_lfp_correlated(duration_ms: float = 500.0, intention: float = 0.6) -> Dict:
    s = SpikeStream(SpikeStreamConfig(seed=999, n_neurons=30, n_ch_lfp=8))
    return s.generate_window_ms(duration_ms, intention=intention)
