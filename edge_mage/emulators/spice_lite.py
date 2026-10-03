"""
spice_lite — Pedagogical MNA circuit simulator (pure Python, no external libs).

Implements Modified Nodal Analysis (MNA) for DC and AC circuit analysis,
transfer functions, and ASCII Bode plots.

Algorithm:
  For N non-GND nodes and B voltage sources the MNA system is:
      G × x = I   (size N+B)
  where G combines nodal conductance + KVL stamps and I combines
  current injections + source amplitudes.

DC: C=open-circuit, L=short-circuit (via 0-V voltage source rows).
AC: complex admittances  Y_R=1/R, Y_C=jωC, Y_L=1/(jωL).
"""

from __future__ import annotations

import argparse
import cmath
import math


# ── Gaussian elimination ──────────────────────────────────────────────────────

def _gauss_solve(A: list[list[complex]], b: list[complex]) -> list[complex]:
    """
    Solve Ax = b via Gaussian elimination with partial pivoting.
    Works with real or complex entries.
    Raises ValueError for singular matrices (floating node / short-circuit).
    """
    n = len(b)
    # Build augmented matrix [A | b]
    M = [row[:] + [b[i]] for i, row in enumerate(A)]

    for col in range(n):
        # Partial pivot: swap the row with the largest |value| in this column
        pivot_row = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[pivot_row] = M[pivot_row], M[col]
        if abs(M[col][col]) < 1e-15:
            raise ValueError("Circuito singular: nó flutuante ou curto-circuito")
        # Eliminate below pivot
        for row in range(col + 1, n):
            factor = M[row][col] / M[col][col]
            for j in range(col, n + 1):
                M[row][j] -= factor * M[col][j]

    # Back substitution
    x = [complex(0)] * n
    for i in range(n - 1, -1, -1):
        x[i] = M[i][n]
        for j in range(i + 1, n):
            x[i] -= M[i][j] * x[j]
        x[i] /= M[i][i]
    return x


# ── Circuit class ─────────────────────────────────────────────────────────────

class Circuit:
    """
    Pedagogical MNA circuit simulator (pure Python, no external libraries).

    Supports: resistors, capacitors, inductors, DC voltage sources,
    DC current sources.

    Units: Ω, F, H, V, A, Hz.

    Example — RC low-pass filter::

        c = Circuit()
        c.add_vsource('Vin', 'vin', 'GND', 1.0)
        c.add_resistor('R1', 'vin', 'vout', 1000.0)
        c.add_capacitor('C1', 'vout', 'GND', 1e-6)
        print(c.ascii_bode('vin', 'vout'))
    """

    def __init__(self) -> None:
        self._resistors:  list[tuple[str, str, str, float]] = []
        self._capacitors: list[tuple[str, str, str, float]] = []
        self._inductors:  list[tuple[str, str, str, float]] = []
        self._vsources:   list[tuple[str, str, str, float]] = []
        self._isources:   list[tuple[str, str, str, float]] = []

    # ── Element API ───────────────────────────────────────────────────────────

    def add_resistor(self, name: str, n1: str, n2: str, r_ohms: float) -> None:
        """Add resistor between nodes n1 and n2."""
        if r_ohms <= 0:
            raise ValueError(f"{name}: resistance must be > 0 Ω")
        self._resistors.append((name, n1, n2, r_ohms))

    def add_capacitor(self, name: str, n1: str, n2: str, c_farads: float) -> None:
        """Add capacitor between nodes n1 and n2 (open-circuit in DC analysis)."""
        if c_farads <= 0:
            raise ValueError(f"{name}: capacitance must be > 0 F")
        self._capacitors.append((name, n1, n2, c_farads))

    def add_inductor(self, name: str, n1: str, n2: str, l_henry: float) -> None:
        """Add inductor between nodes n1 and n2 (short-circuit in DC analysis)."""
        if l_henry <= 0:
            raise ValueError(f"{name}: inductance must be > 0 H")
        self._inductors.append((name, n1, n2, l_henry))

    def add_vsource(
        self, name: str, n_pos: str, n_neg: str, v_dc: float = 1.0
    ) -> None:
        """Add ideal voltage source. n_neg may be 'GND' or '0'."""
        self._vsources.append((name, n_pos, n_neg, v_dc))

    def add_isource(
        self, name: str, n_pos: str, n_neg: str, i_dc: float = 1.0
    ) -> None:
        """
        Add ideal current source (conventional current flows from n_neg
        to n_pos *inside* the source, i.e. it pushes current into n_pos).
        """
        self._isources.append((name, n_pos, n_neg, i_dc))

    def reset(self) -> None:
        """Remove all circuit elements."""
        self._resistors.clear()
        self._capacitors.clear()
        self._inductors.clear()
        self._vsources.clear()
        self._isources.clear()

    # ── Internal helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _is_gnd(node: str) -> bool:
        return node.lower() in ("gnd", "0")

    def _node_map(self) -> dict[str, int]:
        """
        Build ordered mapping: non-GND node name → 1-based matrix index.
        GND ('GND' / '0') is always index 0 and is NOT stored in the map.
        Insertion order determines indices (deterministic for a given build order).
        """
        seen: dict[str, int] = {}
        idx = 1

        def _add(n: str) -> None:
            nonlocal idx
            if self._is_gnd(n):
                return
            if n not in seen:
                seen[n] = idx
                idx += 1

        for elems in (self._resistors, self._capacitors, self._inductors):
            for _, n1, n2, _ in elems:
                _add(n1); _add(n2)
        for _, np_, nn, _ in self._vsources:
            _add(np_); _add(nn)
        for _, np_, nn, _ in self._isources:
            _add(np_); _add(nn)
        return seen

    def _ni(self, node: str, nmap: dict[str, int]) -> int:
        """Return matrix index for node (0 = GND)."""
        return 0 if self._is_gnd(node) else nmap[node]

    def _build_mna(
        self, omega: float | None
    ) -> tuple[list[list[complex]], list[complex], dict[str, int], int]:
        """
        Assemble the MNA linear system  G × x = I_vec.

        omega=None  → DC: capacitors=open, inductors=short (extra 0-V rows).
        omega=2πf   → AC: complex admittances for C and L.

        Returns (G, I_vec, nmap, n_nodes).
        n_nodes = number of non-GND nodes (= len(nmap)).
        """
        nmap = self._node_map()
        n_nodes = len(nmap)
        n_vsrc = len(self._vsources)
        # DC: each inductor becomes an ideal 0-V short (adds a KVL row)
        n_ind_dc = len(self._inductors) if omega is None else 0
        size = n_nodes + n_vsrc + n_ind_dc

        if size == 0:
            return [], [], nmap, 0

        G: list[list[complex]] = [[complex(0)] * size for _ in range(size)]
        I_vec: list[complex] = [complex(0)] * size

        def stamp_y(y: complex, pi: int, ni: int) -> None:
            """Stamp admittance y between nodes pi and ni (0 = GND)."""
            if pi > 0:
                G[pi - 1][pi - 1] += y
            if ni > 0:
                G[ni - 1][ni - 1] += y
            if pi > 0 and ni > 0:
                G[pi - 1][ni - 1] -= y
                G[ni - 1][pi - 1] -= y

        # Resistors ────────────────────────────────────────────────────────────
        for _, n1, n2, r in self._resistors:
            stamp_y(complex(1.0 / r), self._ni(n1, nmap), self._ni(n2, nmap))

        # Reactive elements (AC only) ──────────────────────────────────────────
        if omega is not None:
            for _, n1, n2, c in self._capacitors:
                # Y_C = jωC
                stamp_y(complex(0.0, omega * c), self._ni(n1, nmap), self._ni(n2, nmap))
            for _, n1, n2, l in self._inductors:
                # Y_L = 1/(jωL) = −j/(ωL)
                stamp_y(complex(0.0, -1.0 / (omega * l)), self._ni(n1, nmap), self._ni(n2, nmap))

        # Voltage sources (MNA stamp: adds current variable rows) ─────────────
        for k, (_, np_, nn, v) in enumerate(self._vsources):
            row = n_nodes + k
            pi = self._ni(np_, nmap)
            ni = self._ni(nn, nmap)
            # KVL equation row: V_pos − V_neg = v
            if pi > 0:
                G[row][pi - 1] = complex(1)
                G[pi - 1][row] = complex(1)
            if ni > 0:
                G[row][ni - 1] = complex(-1)
                G[ni - 1][row] = complex(-1)
            I_vec[row] = complex(v)

        # Inductors as DC shorts (0-V voltage sources) ────────────────────────
        if omega is None:
            for k, (_, n1, n2, _) in enumerate(self._inductors):
                row = n_nodes + n_vsrc + k
                pi = self._ni(n1, nmap)
                ni = self._ni(n2, nmap)
                if pi > 0:
                    G[row][pi - 1] = complex(1)
                    G[pi - 1][row] = complex(1)
                if ni > 0:
                    G[row][ni - 1] = complex(-1)
                    G[ni - 1][row] = complex(-1)
                I_vec[row] = complex(0)

        # Current sources ─────────────────────────────────────────────────────
        for _, np_, nn, i_val in self._isources:
            pi = self._ni(np_, nmap)
            ni = self._ni(nn, nmap)
            if pi > 0:
                I_vec[pi - 1] += complex(i_val)
            if ni > 0:
                I_vec[ni - 1] -= complex(i_val)

        return G, I_vec, nmap, n_nodes

    # ── Analysis ──────────────────────────────────────────────────────────────

    def dc_solve(self) -> dict[str, float]:
        """
        Solve DC operating point (C=open-circuit, L=short-circuit).

        Returns {node_name: voltage_V} for every non-GND node.
        Raises ValueError if the circuit is singular (floating node or
        short-circuit that makes the system underdetermined).
        """
        G, I_vec, nmap, _n = self._build_mna(None)
        if not G:
            return {}
        x = _gauss_solve(G, I_vec)
        return {node: x[idx - 1].real for node, idx in nmap.items()}

    def ac_solve(self, freq_hz: float) -> dict[str, complex]:
        """
        Solve AC small-signal analysis at freq_hz.

        Returns {node_name: complex_phasor_voltage}.
        """
        omega = 2.0 * math.pi * freq_hz
        G, I_vec, nmap, _n = self._build_mna(omega)
        if not G:
            return {}
        x = _gauss_solve(G, I_vec)
        return {node: x[idx - 1] for node, idx in nmap.items()}

    def transfer_function(
        self,
        v_in_node: str,
        v_out_node: str,
        freqs_hz: list[float],
    ) -> list[complex]:
        """
        Compute H(f) = V_out(f) / V_in(f) for each frequency in freqs_hz.

        The voltage source in the circuit sets V_in; dividing normalises it
        so the result is independent of the source amplitude.
        """
        results: list[complex] = []
        for f in freqs_hz:
            voltages = self.ac_solve(f)
            v_in = voltages.get(v_in_node, complex(0))
            v_out = voltages.get(v_out_node, complex(0))
            results.append(v_out / v_in if abs(v_in) > 1e-30 else complex(0))
        return results

    def bode_magnitude_db(
        self,
        v_in_node: str,
        v_out_node: str,
        freqs_hz: list[float],
    ) -> list[float]:
        """Return |H(f)| in dB for each frequency in freqs_hz."""
        out: list[float] = []
        for h in self.transfer_function(v_in_node, v_out_node, freqs_hz):
            mag = abs(h)
            out.append(20.0 * math.log10(mag) if mag > 1e-300 else -300.0)
        return out

    def bode_phase_deg(
        self,
        v_in_node: str,
        v_out_node: str,
        freqs_hz: list[float],
    ) -> list[float]:
        """Return phase of H(f) in degrees for each frequency in freqs_hz."""
        return [
            math.degrees(cmath.phase(h))
            for h in self.transfer_function(v_in_node, v_out_node, freqs_hz)
        ]

    def ascii_bode(
        self,
        v_in_node: str,
        v_out_node: str,
        f_start: float = 1.0,
        f_stop: float = 100_000.0,
        n_points: int = 40,
        width: int = 60,
    ) -> str:
        """
        Return a multi-line ASCII Bode magnitude plot (dB vs log₁₀ frequency).

        Visual key:
          █  curve at the exact dB level for that column (frequency)
          ░  level above the curve — signal has rolled off past this row
          (space)  level below the curve — not yet attenuated to here

        Example (RC low-pass, R=1 kΩ, C=1 µF, fc≈159 Hz)::

          +  3 dB │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
          -  5 dB │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
          - 13 dB │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
          - 22 dB │          ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
          - 30 dB │                ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
          - 38 dB │                      ░░░░░░░░░░░░░░░░░░░░░░░░░
          - 46 dB │                              ░░░░░░░░░░░░░░░░░
          - 55 dB │                                      ░░░░░░░░░
                  └───────────────────────────────────────────────
                    1    10   100   1k   10k  100k (Hz)
        """
        n_points = max(2, n_points)
        log_start = math.log10(max(f_start, 1e-9))
        log_stop = math.log10(max(f_stop, f_start * 2.0))
        freqs = [
            10 ** (log_start + (log_stop - log_start) * i / (n_points - 1))
            for i in range(n_points)
        ]
        dbs = self.bode_magnitude_db(v_in_node, v_out_node, freqs)

        plot_h = 8
        label_w = 9   # e.g. " - 40 dB"
        plot_w = max(8, width - label_w - 1)

        db_max = max(3.0, max(dbs))
        db_min = min(-60.0, min(dbs))
        db_span = db_max - db_min

        grid: list[list[str]] = [[" "] * plot_w for _ in range(plot_h)]

        for xi, db in enumerate(dbs):
            col = min(plot_w - 1, int(xi * (plot_w - 1) / (n_points - 1)))
            if db <= db_min:
                # Signal beyond lower plot range — mark entire column as ░
                for r in range(plot_h):
                    if grid[r][col] == " ":
                        grid[r][col] = "░"
            else:
                row_f = (db_max - db) / db_span * (plot_h - 1)
                row = max(0, min(plot_h - 1, int(row_f + 0.5)))
                grid[row][col] = "█"
                # Rows above the curve: signal has rolled off to this row
                for r in range(row):
                    if grid[r][col] == " ":
                        grid[r][col] = "░"

        lines: list[str] = []
        for r in range(plot_h):
            db_level = db_max - r * db_span / max(1, plot_h - 1)
            label = f"{db_level:+5.0f} dB"
            lines.append(f"{label} │{''.join(grid[r])}")

        lines.append(" " * label_w + "└" + "─" * plot_w)

        # Frequency tick labels (6 ticks, log-spaced)
        n_ticks = 6
        tick_line = [" "] * plot_w
        for ti in range(n_ticks):
            tf = 10 ** (log_start + (log_stop - log_start) * ti / max(1, n_ticks - 1))
            pos = min(plot_w - 1, int(ti * (plot_w - 1) / max(1, n_ticks - 1)))
            ts = f"{tf:.0f}" if tf < 1_000 else f"{tf / 1_000:.0f}k"
            for j, ch in enumerate(ts):
                if pos + j < plot_w:
                    tick_line[pos + j] = ch
        lines.append(" " * (label_w + 1) + "".join(tick_line) + " (Hz)")

        return "\n".join(lines)


# ── Demo / CLI ────────────────────────────────────────────────────────────────

def _demo() -> None:
    """Self-contained demo: voltage divider + RC filters."""
    print("spice_lite demo (MNA circuit simulator — pedagogical, no external libs)\n")

    # ── Demo 1: voltage divider ───────────────────────────────────────────────
    print("[Demo 1: Voltage divider  R=R=1 kΩ, Vin=5 V]")
    c1 = Circuit()
    c1.add_vsource("V1", "vin", "GND", 5.0)
    c1.add_resistor("R1", "vin", "vmid", 1_000.0)
    c1.add_resistor("R2", "vmid", "GND", 1_000.0)
    r1 = c1.dc_solve()
    vmid = r1["vmid"]
    ok = "✓" if abs(vmid - 2.5) < 1e-6 else "✗"
    print(f"  V_mid = {vmid:.3f} V  {ok}")
    print()

    # ── Demo 2: RC low-pass filter ────────────────────────────────────────────
    R = 1_000.0
    C = 1e-6
    fc = 1.0 / (2 * math.pi * R * C)
    print(f"[Demo 2: RC Low-Pass Filter  R={R:.0f} Ω, C={C*1e6:.1f} µF, fc≈{fc:.1f} Hz]")
    c2 = Circuit()
    c2.add_vsource("Vin", "vin", "GND", 1.0)
    c2.add_resistor("R1", "vin", "vout", R)
    c2.add_capacitor("C1", "vout", "GND", C)
    bode_str = c2.ascii_bode("vin", "vout", f_start=1.0, f_stop=100_000.0, n_points=40, width=60)
    print("  Bode magnitude (dB) vs frequency:")
    for line in bode_str.splitlines():
        print("  " + line)
    h_at_fc = c2.transfer_function("vin", "vout", [fc])[0]
    db_at_fc = c2.bode_magnitude_db("vin", "vout", [fc])[0]
    ok2 = "✓" if abs(db_at_fc - (-3.01)) < 0.5 else "✗"
    print(f"  At fc={fc:.1f} Hz: |H| = {db_at_fc:.2f} dB  {ok2} (half-power point)")
    print()

    # ── Demo 3: RC high-pass filter ───────────────────────────────────────────
    print(f"[Demo 3: RC High-Pass Filter  R={R:.0f} Ω, C={C*1e6:.1f} µF]")
    c3 = Circuit()
    c3.add_vsource("Vin", "vin", "GND", 1.0)
    c3.add_capacitor("C1", "vin", "vhp", C)
    c3.add_resistor("R1", "vhp", "GND", R)
    bode_hp = c3.ascii_bode("vin", "vhp", f_start=1.0, f_stop=100_000.0, n_points=40, width=60)
    for line in bode_hp.splitlines():
        print("  " + line)
    db_hp_low = c3.bode_magnitude_db("vin", "vhp", [1.0])[0]
    db_hp_high = c3.bode_magnitude_db("vin", "vhp", [10_000.0])[0]
    print(f"  At   1 Hz: {db_hp_low:.1f} dB (blocked)")
    print(f"  At 10kHz: {db_hp_high:.2f} dB (passed)")
    print()

    # ── Demo 4: 3-resistor series divider ────────────────────────────────────
    print("[Demo 4: Series divider  R1=1 kΩ, R2=2 kΩ, R3=3 kΩ, Vin=12 V]")
    c4 = Circuit()
    c4.add_vsource("V1", "top", "GND", 12.0)
    c4.add_resistor("R1", "top", "n1", 1_000.0)
    c4.add_resistor("R2", "n1", "n2", 2_000.0)
    c4.add_resistor("R3", "n2", "GND", 3_000.0)
    r4 = c4.dc_solve()
    ok4a = "✓" if abs(r4["n1"] - 10.0) < 1e-4 else "✗"
    ok4b = "✓" if abs(r4["n2"] - 6.0) < 1e-4 else "✗"
    print(f"  V_n1 = {r4['n1']:.3f} V  {ok4a}  (expected 10.000 V)")
    print(f"  V_n2 = {r4['n2']:.3f} V  {ok4b}  (expected  6.000 V)")


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(
        description="spice_lite: MNA circuit simulator (pedagogical, no external libs)"
    )
    p.parse_args(argv)
    _demo()


if __name__ == "__main__":
    main()
