"""
Simulated online BCI loop stub: sliding window → bandpower → toy label → latency log.

Educational end-to-end sketch on synthetic EEG — not a clinical decoder.
"""

from __future__ import annotations

from edge_mage.emulators.synth_eeg import SynthEEGStream


def run_online_stub(
    *,
    fs: float = 250.0,
    window_samples: int = 25,
    hop_samples: int = 10,
    n_windows: int = 8,
    seed: int = 7,
    decide_ms: float = 4.0,
    act_ms: float = 3.0,
    deadline_ms: float = 150.0,
) -> dict:
    """
    Process n_windows of synth EEG with a crude left/right toy rule on µ-band proxy.

    Label rule (didactic): channel 0 µ-bandpower > channel 1 → "right", else "left".
    """
    stream = SynthEEGStream(n_channels=2, fs=fs, seed=seed)
    # Mild class-ish imbalance via suppression on ch0 for half the run
    stream.schedule_mu_suppression(
        start_sample=window_samples,
        duration_samples=window_samples * 3,
        channel=0,
        factor=0.35,
    )
    total = window_samples + hop_samples * (n_windows - 1)
    block = stream.generate(total)
    log: list[dict] = []
    for i in range(n_windows):
        start = i * hop_samples
        end = start + window_samples
        win = block[start:end]
        bp0 = stream.bandpower_proxy(win, 0, 8.0, 12.0)
        bp1 = stream.bandpower_proxy(win, 1, 8.0, 12.0)
        label = "right" if bp0 > bp1 else "left"
        window_ms = 1000.0 * window_samples / fs
        total_ms = window_ms + decide_ms + act_ms
        log.append(
            {
                "i": i,
                "start": start,
                "label": label,
                "bp0": bp0,
                "bp1": bp1,
                "window_ms": window_ms,
                "decide_ms": decide_ms,
                "act_ms": act_ms,
                "total_ms": total_ms,
                "miss": total_ms > deadline_ms,
            }
        )
    misses = sum(1 for row in log if row["miss"])
    return {
        "fs": fs,
        "window_samples": window_samples,
        "hop_samples": hop_samples,
        "deadline_ms": deadline_ms,
        "n_windows": n_windows,
        "misses": misses,
        "log": log,
        "note": (
            "Simulated online loop on synth EEG — toy µ-bandpower rule, "
            "not a trained MI classifier / not real-time hardware."
        ),
    }


def _demo() -> None:
    out = run_online_stub()
    print("online_loop stub demo")
    print(f"  windows={out['n_windows']}  misses={out['misses']}  deadline={out['deadline_ms']}ms")
    for row in out["log"][:3]:
        print(
            f"  [{row['i']}] {row['label']}  bp0={row['bp0']:.2f} bp1={row['bp1']:.2f}  "
            f"total={row['total_ms']:.1f}ms miss={row['miss']}"
        )
    print(f"  {out['note']}")


if __name__ == "__main__":
    _demo()
