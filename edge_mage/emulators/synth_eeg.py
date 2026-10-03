"""Synthetic multichannel EEG stream for Neurotech labs (offline + online tick)."""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass, field


@dataclass
class SynthEEGStream:
    """
    Colored-noise-ish EEG toy + optional band-limited µ bursts.

    Mode: offline replay (generate once) or online tick (chunk per call).
    No real human data — educational only.
    """

    n_channels: int = 8
    fs: float = 250.0
    seed: int = 0
    noise_std: float = 1.0
    _rng: random.Random = field(init=False, repr=False)
    _t: int = field(default=0, init=False, repr=False)
    # (start, end, channel, amplitude, freq_hz)
    _mu_bursts: list[tuple[int, int, int, float, float]] = field(
        default_factory=list, init=False, repr=False
    )

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)
        self._t = 0
        self._mu_bursts = []

    def reset(self, seed: int | None = None) -> None:
        if seed is not None:
            self.seed = seed
        self._rng = random.Random(self.seed)
        self._t = 0
        self._mu_bursts = []

    def schedule_mu_burst(
        self,
        *,
        start_sample: int,
        duration_samples: int,
        channel: int = 0,
        amplitude: float = 2.5,
        freq_hz: float = 10.0,
    ) -> None:
        """Inject a band-limited 'µ' sinusoid burst (toy motor-rhythm stand-in)."""
        if not (0 <= channel < self.n_channels):
            raise ValueError("channel out of range")
        end = start_sample + max(1, duration_samples)
        self._mu_bursts.append((start_sample, end, channel, amplitude, freq_hz))

    def _sample_at(self, i: int) -> list[float]:
        # simple AR(1)-ish colored noise per channel
        row: list[float] = []
        for ch in range(self.n_channels):
            # mix of white + slow drift + mid-band tone
            white = self._rng.gauss(0.0, self.noise_std)
            slow = 0.3 * math.sin(2 * math.pi * 0.5 * i / self.fs + ch)
            mid = 0.2 * math.sin(2 * math.pi * 12.0 * i / self.fs + 0.3 * ch)
            v = white + slow + mid
            for start, end, bch, amp, freq in self._mu_bursts:
                if bch == ch and start <= i < end:
                    phase = 2 * math.pi * freq * (i - start) / self.fs
                    envelope = 0.5 * (
                        1.0 - math.cos(2 * math.pi * (i - start) / max(1, end - start))
                    )
                    v += amp * envelope * math.sin(phase)
            row.append(v)
        return row

    def generate(self, n_samples: int) -> list[list[float]]:
        """Offline: return [sample][channel] block starting at current _t."""
        out: list[list[float]] = []
        for _ in range(n_samples):
            out.append(self._sample_at(self._t))
            self._t += 1
        return out

    def tick(self, chunk: int = 25) -> list[list[float]]:
        """Online: one chunk (~chunk/fs seconds at fs)."""
        return self.generate(chunk)

    def bandpower_proxy(
        self,
        block: list[list[float]],
        channel: int,
        lo_hz: float,
        hi_hz: float,
    ) -> float:
        """
        Tiny Goertzel-ish power proxy for teaching (not a production PSD).
        Sums squared correlation with sine/cosine at band mid frequency.
        """
        if not block or channel < 0 or channel >= self.n_channels:
            return 0.0
        mid = 0.5 * (lo_hz + hi_hz)
        n = len(block)
        re = im = 0.0
        for i, row in enumerate(block):
            ang = 2 * math.pi * mid * i / self.fs
            x = row[channel]
            re += x * math.cos(ang)
            im += x * math.sin(ang)
        return (re * re + im * im) / max(1, n)


def _demo(seconds: float = 1.0, with_mu: bool = True) -> None:
    stream = SynthEEGStream(n_channels=4, fs=250.0, seed=7)
    n = int(seconds * stream.fs)
    if with_mu:
        stream.schedule_mu_burst(
            start_sample=int(0.2 * stream.fs),
            duration_samples=int(0.4 * stream.fs),
            channel=0,
            amplitude=3.0,
            freq_hz=10.0,
        )
    block = stream.generate(n)
    bp_mu = stream.bandpower_proxy(block, 0, 8.0, 12.0)
    bp_beta = stream.bandpower_proxy(block, 0, 18.0, 25.0)
    print(f"synth_eeg_stream  fs={stream.fs}  ch={stream.n_channels}  n={n}")
    print(f"  bandpower_proxy µ(8–12)={bp_mu:.3f}  β(18–25)={bp_beta:.3f}")
    # ASCII sparkline of ch0
    xs = [row[0] for row in block[:: max(1, n // 40)]]
    lo, hi = min(xs), max(xs)
    span = hi - lo or 1.0
    chars = " .:-=+*#%@"
    line = "".join(chars[min(len(chars) - 1, int((x - lo) / span * (len(chars) - 1)))] for x in xs)
    print(f"  ch0: {line}")


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Neurotech synth EEG emulator")
    p.add_argument("--seconds", type=float, default=1.0)
    p.add_argument("--no-mu", action="store_true")
    args = p.parse_args(argv)
    _demo(seconds=args.seconds, with_mu=not args.no_mu)


if __name__ == "__main__":
    main()
