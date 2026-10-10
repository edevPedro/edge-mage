"""Stimulus safety stub (educational) — charge balance & basic checks."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Pulse:
    phase_dur_us: int
    amp_ma: float
    polarity: int  # +1/-1
    interphase_us: int = 100


@dataclass
class StimConfig:
    biphasic: bool = True
    charge_balance_tol_percent: float = 5.0
    max_duty_cycle_percent: float = 20.0
    max_charge_per_phase_uc: float = 10.0  # µC (educational bounds)


class StimSafetyStub:
    def __init__(self, cfg: StimConfig | None = None) -> None:
        self.cfg = cfg or StimConfig()

    def analyze(self, pulses: List[Pulse], rate_hz: float, total_ms: float = 1000.0) -> Dict:
        warnings: List[str] = []
        charge_ua_s = 0.0  # sum Q
        phases = []
        for p in pulses:
            q_uc = abs(p.amp_ma) * (p.phase_dur_us / 1_000_000.0) * 1000.0  # mA*us -> µC approx? better: mA*s = µC (mA*ms)? mA*us = 1e-6 mA-s = 1e-3 µA-s? simpler: Q(µC)=I(mA)*t(ms); or I(A)*t(s)=C
            q_uc = abs(p.amp_ma) * (p.phase_dur_us / 1000.0)  # mA * ms? phase_dur_us in us, so ms = us/1000 -> mA*ms = µC
            phases.append({"pol": p.polarity, "q_uc": round(q_uc, 4), "dur_us": p.phase_dur_us})
            charge_ua_s += q_uc
        pos = sum(ph["q_uc"] for ph in phases if ph["pol"] > 0)
        neg = sum(ph["q_uc"] for ph in phases if ph["pol"] < 0)
        bal_err_pct = 0.0
        denom = max(pos, neg, 1e-6)
        if pos > 0 or neg > 0:
            bal_err_pct = abs(pos - neg) / denom * 100.0
        if bal_err_pct > self.cfg.charge_balance_tol_percent:
            warnings.append(f"Charge imbalance > {self.cfg.charge_balance_tol_percent}% ({bal_err_pct:.2f}%)")
        duty = 0.0
        if rate_hz > 0:
            per_pulse_ms = sum(p.phase_dur_us for p in pulses) / 1000.0 + sum(getattr(p, "interphase_us", 0) for p in pulses) / 1000.0
            duty = min(100.0, (per_pulse_ms * rate_hz))
        if duty > self.cfg.max_duty_cycle_percent:
            warnings.append(f"Duty cycle high ({duty:.2f}% > {self.cfg.max_duty_cycle_percent}%)")
        for ph in phases:
            if ph["q_uc"] > self.cfg.max_charge_per_phase_uc:
                warnings.append(f"Phase charge large ({ph['q_uc']:.3f} µC)")
        return {
            "biphasic": self.cfg.biphasic,
            "pos_uc": round(pos, 4),
            "neg_uc": round(neg, 4),
            "imbalance_pct": round(bal_err_pct, 2),
            "duty_cycle_pct": round(duty, 2),
            "phases": phases,
            "ok": len(warnings) == 0,
            "warnings": warnings,
            "educational_note": "Nonclinical safety literacy only; not for clinical use.",
        }
