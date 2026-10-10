"""NEURON CLI simulation stub (educational) - simulates minimal CLI output."""
from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class NeuronSimConfig:
    dt_ms: float = 0.025
    tstop_ms: float = 100.0
    seed: int = 123


class NeuronCLIStub:
    def __init__(self, cfg: NeuronSimConfig | None = None) -> None:
        self.cfg = cfg or NeuronSimConfig()
        self.rng = random.Random(self.cfg.seed)

    def run_hh_sim(self, stim_amp_nA: float = 0.1, stim_dur_ms: float = 10.0) -> Dict:
        steps = int(self.cfg.tstop_ms / self.cfg.dt_ms)
        v = -65.0
        m = 0.05; h = 0.6; n = 0.32
        gna = 120; gk = 36; gl = 0.3
        ena = 50; ek = -77; el = -54.4
        cm = 1.0
        vm = []
        tms = []
        for i in range(steps):
            t = i * self.cfg.dt_ms
            stim = stim_amp_nA if t >= 5.0 and t <= 5.0 + stim_dur_ms else 0.0
            am = 0.1 * (v + 40) / (1 - math.exp(-(v + 40) / 10)) if abs(v + 40) > 1e-6 else 1.0
            bm = 4.0 * math.exp(-(v + 65) / 18)
            ah = 0.07 * math.exp(-(v + 65) / 20)
            bh = 1.0 / (1 + math.exp(-(v + 35) / 10))
            an = 0.01 * (v + 55) / (1 - math.exp(-(v + 55) / 10)) if abs(v + 55) > 1e-6 else 0.1
            bn = 0.125 * math.exp(-(v + 65) / 80)
            m += (am * (1 - m) - bm * m) * self.cfg.dt_ms
            h += (ah * (1 - h) - bh * h) * self.cfg.dt_ms
            n += (an * (1 - n) - bn * n) * self.cfg.dt_ms
            ina = gna * m ** 3 * h * (v - ena)
            ik = gk * n ** 4 * (v - ek)
            il = gl * (v - el)
            dv = (stim - ina - ik - il) / cm
            v += dv * self.cfg.dt_ms
            if i % int(0.5 / self.cfg.dt_ms) == 0 or i == steps - 1:
                vm.append(round(v, 2))
                tms.append(round(t, 2))
        spikes = sum(1 for i in range(1, len(vm)) if vm[i] > 0 and vm[i-1] <= 0)
        return {
            "command": "nrniv -python hh_sim.py (simulated)",
            "tstop_ms": self.cfg.tstop_ms,
            "dt_ms": self.cfg.dt_ms,
            "stim_amp_nA": stim_amp_nA,
            "vm_uv": vm[-50:] if len(vm) > 50 else vm,
            "t_ms": tms[-50:] if len(tms) > 50 else tms,
            "spike_count": spikes,
            "educational_note": "NEURON CLI output simulated for critical interpretation (no local NEURON install required).",
        }

    def run_passive_cable(self, length_um: float = 1000.0) -> Dict:
        return {
            "command": "nrniv -python cable.hoc (simulated)",
            "length_um": length_um,
            "tau_ms": round(20.0 * (length_um / 1000.0) ** 0.5, 3),
            "lambda_um": round(1000.0 * math.sqrt(0.5), 1),
            "notes": "Space/length constant intuition; interpret attenuation, not derive full cable eq.",
            "educational_note": "Simulated for figure/simulation interpretation.",
        }
