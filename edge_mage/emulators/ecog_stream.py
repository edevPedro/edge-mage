"""Synthetic ECoG grid stream (educational)."""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class EcogConfig:
    fs_hz: int = 1000
    grid_rows: int = 4
    grid_cols: int = 4
    n_ch: int = 16
    spatial_blur: float = 0.4  # 0-1
    noise_std_uv: float = 1.0
    seed: int = 42


class EcogStream:
    def __init__(self, cfg: EcogConfig | None = None) -> None:
        self.cfg = cfg or EcogConfig()
        self.rng = random.Random(self.cfg.seed)
        self._t_ms: float = 0.0
        self._step = 1000.0 / self.cfg.fs_hz if self.cfg.fs_hz > 0 else 1.0

    def generate_window_ms(self, duration_ms: float, intention: float = 0.5) -> Dict:
        n = max(1, int(math.ceil(duration_ms / self._step)))
        chs = min(self.cfg.n_ch, self.cfg.grid_rows * self.cfg.grid_cols)
        data = [[0.0] * n for _ in range(chs)]
        mod = max(0.0, min(1.0, intention))
        for i in range(n):
            t = i * self._step / 1000.0
            base_mu = 3.0 * math.sin(2 * math.pi * 10.0 * t) * (0.9 + mod * 0.3)
            base_hf = 1.2 * math.sin(2 * math.pi * 70.0 * t + mod * math.pi) * 0.25
            for c in range(chs):
                r = c // self.cfg.grid_cols if self.cfg.grid_cols > 0 else 0
                k = c % self.cfg.grid_cols if self.cfg.grid_cols > 0 else 0
                ctr = (self.cfg.grid_rows - 1) / 2.0, (self.cfg.grid_cols - 1) / 2.0
                dr = abs(r - ctr[0]); dc = abs(k - ctr[1])
                spatial = 1.0 / (1.0 + (dr + dc) * self.cfg.spatial_blur)
                data[c][i] = (base_mu + base_hf) * spatial + self.rng.gauss(0.0, self.cfg.noise_std_uv)
        self._t_ms += duration_ms
        return {
            "fs_hz": self.cfg.fs_hz,
            "duration_ms": duration_ms,
            "n_ch": chs,
            "grid": (self.cfg.grid_rows, self.cfg.grid_cols),
            "ecog_uv": data,
            "intention": round(mod, 3),
        }
