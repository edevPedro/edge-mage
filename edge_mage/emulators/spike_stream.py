"""Synthetic spike + LFP + MUA stream (educational, nonclinical)."""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class SpikeEvent:
    neuron_id: int
    time_ms: float
    amplitude_uv: float = 30.0


@dataclass
class SpikeStreamConfig:
    fs_hz: int = 1000
    n_neurons: int = 20
    n_ch_lfp: int = 8
    mean_rate_hz: float = 15.0
    noise_std_uv: float = 1.0
    intention_modulation: float = 0.4  # 0-1
    seed: int = 12345


class SpikeStream:
    def __init__(self, cfg: SpikeStreamConfig | None = None) -> None:
        self.cfg = cfg or SpikeStreamConfig()
        self.rng = random.Random(self.cfg.seed)
        self._time_ms: float = 0.0
        self._step_ms: float = 1000.0 / self.cfg.fs_hz if self.cfg.fs_hz > 0 else 1.0

    def generate_window_ms(self, duration_ms: float, intention: float = 0.5) -> Dict:
        n_samples = max(1, int(math.ceil(duration_ms / self._step_ms)))
        lfp = [[0.0] * n_samples for _ in range(self.cfg.n_ch_lfp)]
        spikes: List[SpikeEvent] = []
        mod = max(0.0, min(1.0, intention * (1.0 + self.cfg.intention_modulation) - self.cfg.intention_modulation / 2.0))
        base = self.cfg.mean_rate_hz
        for ni in range(self.cfg.n_neurons):
            rate = base * (0.7 + mod * 0.6 + self.rng.uniform(-0.1, 0.1))
            rate = max(0.1, rate)
            isi_ms = 1000.0 / rate if rate > 0 else 1000.0
            t = self.rng.uniform(0, isi_ms)
            while t < duration_ms:
                spikes.append(SpikeEvent(neuron_id=ni, time_ms=self._time_ms + t, amplitude_uv=self.rng.gauss(40.0, 10.0)))
                t += self.rng.gauss(isi_ms, isi_ms * 0.1)
                if t < 0:
                    t = isi_ms
        for ch in range(self.cfg.n_ch_lfp):
            phase = self.rng.random() * 2 * math.pi
            for i in range(n_samples):
                tms = i * self._step_ms
                mu = 2.0 * math.sin(2 * math.pi * 10.0 * tms / 1000.0 + phase) * (0.8 + mod * 0.4)
                beta = 1.0 * math.sin(2 * math.pi * 20.0 * tms / 1000.0 + phase / 2) * 0.3
                noise = self.rng.gauss(0.0, self.cfg.noise_std_uv)
                lfp[ch][i] = mu + beta + noise
        self._time_ms += duration_ms
        return {
            "fs_hz": self.cfg.fs_hz,
            "duration_ms": duration_ms,
            "lfp_uv": lfp,
            "spikes": [{"n": e.neuron_id, "t": round(e.time_ms, 3), "a": round(e.amplitude_uv, 2)} for e in spikes],
            "mua_count": len(spikes),
            "intention": round(mod, 3),
        }
