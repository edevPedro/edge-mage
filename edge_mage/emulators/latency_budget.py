"""
latency_budget — thin wrapper over CortexMPipelineStub.

Maps closed-loop stages to host-stub quantities:
  sense  ≈ window_ms  (time to fill the analysis window)
  decide ≈ compute_ms (filter / feature / classify stub)
  act    ≈ act_ms     (feedback / packet / actuator — separate from sense)

Not a second physics engine: same Python host model as cortex_m_stub.
"""

from __future__ import annotations

from edge_mage.emulators.cortex_m_stub import CortexMPipelineStub


def stage_budget(
    sense_ms: float,
    decide_ms: float,
    act_ms: float,
    *,
    deadline_ms: float = 40.0,
) -> dict:
    """Sum sense→decide→act and compare to deadline (didactic accounting)."""
    total = float(sense_ms) + float(decide_ms) + float(act_ms)
    return {
        "sense_ms": float(sense_ms),
        "decide_ms": float(decide_ms),
        "act_ms": float(act_ms),
        "total_ms": total,
        "deadline_ms": float(deadline_ms),
        "miss": total > float(deadline_ms),
        "map": {
            "sense": "window_ms (fill causal window)",
            "decide": "compute_ms (filter/feature/classify stub)",
            "act": "act_ms (feedback / UART packet / actuator)",
        },
        "backend": "cortex_m_stub Python host — not QEMU / not CMSIS runtime",
        "disclaimer": (
            "MI feedback loops often tolerate 100–300 ms; a hard 40 ms RT deadline "
            "is a stress case — window_ms alone often dominates."
        ),
    }


def from_cortex_window(
    samples: list[float],
    *,
    act_ms: float = 5.0,
    deadline_ms: float = 40.0,
    taps: int = 5,
) -> dict:
    """Run Cortex stub then expose sense/decide/act mapping."""
    mcu = CortexMPipelineStub(deadline_ms=deadline_ms)
    result = mcu.process_window(samples, taps=taps)
    stages = stage_budget(
        result["window_ms"],
        result["compute_ms"],
        act_ms,
        deadline_ms=deadline_ms,
    )
    stages["cortex"] = {
        "packet_hex": result["packet_hex"],
        "filtered": result["filtered"],
        "runtime_note": result["runtime_note"],
    }
    return stages


def _demo() -> None:
    from edge_mage.emulators.synth_eeg import SynthEEGStream

    stream = SynthEEGStream(n_channels=1, fs=250.0, seed=3)
    samples = [row[0] for row in stream.generate(32)]
    report = from_cortex_window(samples, act_ms=5.0, deadline_ms=40.0)
    print("latency_budget demo (wrapper → cortex_m_stub)")
    print(
        f"  sense={report['sense_ms']:.2f}  decide={report['decide_ms']:.2f}  "
        f"act={report['act_ms']:.2f}  total={report['total_ms']:.2f}  "
        f"deadline={report['deadline_ms']}  miss={report['miss']}"
    )
    print(f"  {report['disclaimer']}")


if __name__ == "__main__":
    _demo()
