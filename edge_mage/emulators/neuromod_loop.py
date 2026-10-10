"""Adaptive neuromodulation closed-loop stub (educational)."""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class NMLConfig:
    fs_hz: int = 250
    beta_thresh: float = 1.8  # normalized
    ramp_rate: float = 0.1
    hysteresis: float = 0.15
    seed: int = 7


class NeuromodLoop:
    def __init__(self, cfg: NMLConfig | None = None) -> None:
        self.cfg = cfg or NMLConfig()
        self.rng = random.Random(self.cfg.seed)
        self._amp: float = 0.0  # 0-1
        self._on: bool = False

    def step(self, lfp_bandpower_beta: float) -> Dict:
        beta_n = lfp_bandpower_beta
        if self._on:
            if beta_n < self.cfg.beta_thresh - self.cfg.hysteresis:
                self._amp = max(0.0, self._amp - self.cfg.ramp_rate)
                if self._amp < 1e-3:
                    self._on = False
            else:
                self._amp = min(1.0, self._amp + self.cfg.ramp_rate * 0.3)
        else:
            if beta_n > self.cfg.beta_thresh + self.cfg.hysteresis:
                self._on = True
                self._amp = min(1.0, self.cfg.ramp_rate * 2.0)
        return {
            "biomarker_beta_n": round(beta_n, 3),
            "stim_on": self._on,
            "stim_amp_norm": round(self._amp, 3),
            "rule": "gated_by_beta_with_hysteresis",
            "educational_note": "Biomarker-driven gating only; not clinical aDBS",
        }

    def simulate_window(self, n_steps: int = 50) -> List[Dict]:
        out = []
        for i in range(n_steps):
            beta = 1.0 + math.sin(i / 5.0) * 0.8 + self.rng.gauss(0.0, 0.1)
            out.append(self.step(max(0.0, beta)))
        return out
