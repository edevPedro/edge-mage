"""
ARM Cortex-M *class* firmware/edge pipeline stub for Neurotech F5 labs.

Python host stub only — not QEMU, not a CMSIS runtime. Teaches acquisition →
ring buffer → filter → packet → latency budget under MCU-like constraints
(fixed buffer, no heap thrash). Point to Edge `cmsis-nn` for real kernels.
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass, field


@dataclass
class CortexMPipelineStub:
    """
    Tiny MCU-flavored DSP stub on the Python host (mental model: Cortex-M).

    Stages (sense → decide → act):
      ADC sample → ring buffer → moving-average / FIR stub → UART-like packet

    Latency splits **window_ms** (time to fill the sense window — usually
    dominates) vs **compute_ms** (filter + pack). Closed-loop deadlines ~40 ms
    often miss when the window alone is longer than the deadline.
    """

    fs: float = 250.0
    buffer_len: int = 64
    deadline_ms: float = 40.0
    adc_us_per_sample: float = 40.0
    filter_us_per_sample: float = 8.0
    packet_us: float = 120.0
    _buf: list[float] = field(default_factory=list, init=False, repr=False)
    _write: int = field(default=0, init=False, repr=False)
    _count: int = field(default=0, init=False, repr=False)
    packets_sent: int = field(default=0, init=False)
    last_latency_ms: float = field(default=0.0, init=False)
    last_window_ms: float = field(default=0.0, init=False)
    last_compute_ms: float = field(default=0.0, init=False)
    deadline_misses: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        self._buf = [0.0] * self.buffer_len
        self._write = 0
        self._count = 0

    def reset(self) -> None:
        self._buf = [0.0] * self.buffer_len
        self._write = 0
        self._count = 0
        self.packets_sent = 0
        self.last_latency_ms = 0.0
        self.last_window_ms = 0.0
        self.last_compute_ms = 0.0
        self.deadline_misses = 0

    def push_sample(self, x: float) -> None:
        """ADC ISR mental model: write one sample into ring buffer."""
        self._buf[self._write] = x
        self._write = (self._write + 1) % self.buffer_len
        self._count = min(self.buffer_len, self._count + 1)

    def snapshot(self) -> list[float]:
        """Oldest→newest view of occupied buffer (for labs)."""
        if self._count == 0:
            return []
        start = (self._write - self._count) % self.buffer_len
        out: list[float] = []
        for i in range(self._count):
            out.append(self._buf[(start + i) % self.buffer_len])
        return out

    def fir_ma(self, taps: int = 5) -> float:
        """Crude moving-average FIR stub on latest `taps` samples."""
        data = self.snapshot()
        if not data:
            return 0.0
        window = data[-min(taps, len(data)) :]
        return sum(window) / len(window)

    def pack_uart(self, value: float) -> bytes:
        """Stub 'packet': magic + int16 µV-ish + checksum nibble."""
        q = max(-32768, min(32767, int(value * 100)))
        hi, lo = (q >> 8) & 0xFF, q & 0xFF
        chk = (0xA5 + hi + lo) & 0xFF
        return bytes([0xA5, hi, lo, chk])

    def process_window(self, samples: list[float], *, taps: int = 5) -> dict:
        """
        Run sense→filter→packet for a window; estimate latency vs deadline.

        - window_ms: causal sense duration = n_samples / fs  (usually dominates)
        - compute_ms: ADC conversion overhead + FIR + pack (host-modeled µs)
        - latency_ms: window_ms + compute_ms
        """
        t0 = time.perf_counter()
        for x in samples:
            self.push_sample(x)
        filt = self.fir_ma(taps=taps)
        pkt = self.pack_uart(filt)
        self.packets_sent += 1

        n = max(1, len(samples))
        window_ms = 1000.0 * n / self.fs
        compute_us = (
            n * self.adc_us_per_sample
            + n * self.filter_us_per_sample
            + self.packet_us
        )
        compute_ms = compute_us / 1000.0
        latency_ms = window_ms + compute_ms
        self.last_window_ms = window_ms
        self.last_compute_ms = compute_ms
        self.last_latency_ms = latency_ms
        miss = latency_ms > self.deadline_ms
        if miss:
            self.deadline_misses += 1

        wall_ms = (time.perf_counter() - t0) * 1000.0
        return {
            "filtered": filt,
            "packet_hex": pkt.hex(),
            "window_ms": window_ms,
            "compute_ms": compute_ms,
            "latency_ms": latency_ms,
            "deadline_ms": self.deadline_ms,
            "miss": miss,
            "wall_ms": wall_ms,
            "buffer_fill": self._count,
            "arch": "python-host-cortex-m-stub",
            "runtime_note": "Python host stub — not QEMU / not CMSIS runtime",
        }

    def budget_report(self) -> str:
        return (
            f"Cortex-M host stub  fs={self.fs}  buf={self.buffer_len}  "
            f"deadline={self.deadline_ms}ms  packets={self.packets_sent}  "
            f"misses={self.deadline_misses}  "
            f"window={self.last_window_ms:.2f}ms  compute={self.last_compute_ms:.2f}ms  "
            f"total={self.last_latency_ms:.2f}ms"
        )


def _demo() -> None:
    from edge_mage.emulators.synth_eeg import SynthEEGStream

    mcu = CortexMPipelineStub(fs=250.0, buffer_len=64, deadline_ms=40.0)
    stream = SynthEEGStream(n_channels=1, fs=250.0, seed=11)
    # 32 samples @ 250 Hz → window 128 ms >> 40 ms deadline → miss (window-dominated)
    block = stream.generate(32)
    ch0 = [row[0] for row in block]
    result = mcu.process_window(ch0, taps=5)
    print("cortex_m_stub demo (Python host — not QEMU / not CMSIS runtime)")
    print(f"  {mcu.budget_report()}")
    print(
        f"  filtered={result['filtered']:.3f}  pkt={result['packet_hex']}  "
        f"window={result['window_ms']:.2f}ms  compute={result['compute_ms']:.2f}ms  "
        f"latency={result['latency_ms']:.2f}ms  miss={result['miss']}"
    )
    if not result["miss"]:
        raise SystemExit("demo expected miss at 40ms deadline with 32-sample window")


def main(argv: list[str] | None = None) -> None:
    argparse.ArgumentParser(
        description="Cortex-M class pipeline stub (Python host)"
    ).parse_args(argv)
    _demo()


if __name__ == "__main__":
    main()
