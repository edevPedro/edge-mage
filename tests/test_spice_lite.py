"""Tests for SPICE-lite pedagogical MNA circuit simulator."""

from __future__ import annotations

import math
import pytest

from edge_mage.emulators.spice_lite import Circuit


def test_dc_voltage_divider() -> None:
    c = Circuit()
    c.add_vsource("V1", "vin", "GND", 10.0)
    c.add_resistor("R1", "vin", "vmid", 10_000.0)
    c.add_resistor("R2", "vmid", "GND", 10_000.0)
    sol = c.dc_solve()
    assert abs(sol["vin"] - 10.0) < 1e-6
    assert abs(sol["vmid"] - 5.0) < 1e-6


def test_dc_series_three_resistors() -> None:
    c = Circuit()
    c.add_vsource("V1", "top", "GND", 12.0)
    c.add_resistor("R1", "top", "n1", 1_000.0)
    c.add_resistor("R2", "n1", "n2", 2_000.0)
    c.add_resistor("R3", "n2", "GND", 3_000.0)
    sol = c.dc_solve()
    assert abs(sol["top"] - 12.0) < 1e-6
    assert abs(sol["n1"] - 10.0) < 1e-6
    assert abs(sol["n2"] - 6.0) < 1e-6


def test_dc_current_source_parallel() -> None:
    c = Circuit()
    # 5 mA current source into two 1 kΩ resistors in parallel (Req = 500 Ω)
    c.add_isource("I1", "node1", "GND", 0.005)
    c.add_resistor("R1", "node1", "GND", 1_000.0)
    c.add_resistor("R2", "node1", "GND", 1_000.0)
    sol = c.dc_solve()
    assert abs(sol["node1"] - 2.5) < 1e-6


def test_dc_inductor_short_and_capacitor_open() -> None:
    c = Circuit()
    c.add_vsource("V1", "vin", "GND", 5.0)
    c.add_resistor("R1", "vin", "n1", 1_000.0)
    # L1 shorts n1 to n2
    c.add_inductor("L1", "n1", "n2", 1e-3)
    # C1 opens between n2 and GND
    c.add_capacitor("C1", "n2", "GND", 1e-6)
    # R2 to GND
    c.add_resistor("R2", "n2", "GND", 1_000.0)
    sol = c.dc_solve()
    # Inductor is ideal short, so V(n1) == V(n2)
    assert abs(sol["n1"] - sol["n2"]) < 1e-6
    # Total resistance is R1 + R2 = 2 kΩ, V(n2) = 2.5 V
    assert abs(sol["n2"] - 2.5) < 1e-6


def test_rc_lowpass_cutoff_and_rolloff() -> None:
    R = 1_000.0
    C = 1e-6
    fc = 1.0 / (2.0 * math.pi * R * C)  # ≈ 159.155 Hz

    c = Circuit()
    c.add_vsource("Vin", "vin", "GND", 1.0)
    c.add_resistor("R1", "vin", "vout", R)
    c.add_capacitor("C1", "vout", "GND", C)

    # Low frequency (1 Hz): |H| ≈ 0 dB, phase ≈ 0°
    h_low = c.transfer_function("vin", "vout", [1.0])[0]
    db_low = c.bode_magnitude_db("vin", "vout", [1.0])[0]
    phase_low = c.bode_phase_deg("vin", "vout", [1.0])[0]
    assert abs(db_low) < 0.1
    assert abs(phase_low) < 2.0

    # At cutoff fc: |H| ≈ -3.01 dB, phase ≈ -45°
    db_fc = c.bode_magnitude_db("vin", "vout", [fc])[0]
    phase_fc = c.bode_phase_deg("vin", "vout", [fc])[0]
    assert abs(db_fc - (-3.0103)) < 0.05
    assert abs(phase_fc - (-45.0)) < 0.5

    # At 10 * fc: roll-off of -20 dB
    db_10fc = c.bode_magnitude_db("vin", "vout", [10.0 * fc])[0]
    assert abs(db_10fc - (-20.04)) < 0.2

    # At 100 * fc: roll-off of -40 dB
    db_100fc = c.bode_magnitude_db("vin", "vout", [100.0 * fc])[0]
    assert abs(db_100fc - (-40.0)) < 0.2


def test_rc_highpass_ac() -> None:
    R = 1_000.0
    C = 1e-6
    fc = 1.0 / (2.0 * math.pi * R * C)

    c = Circuit()
    c.add_vsource("Vin", "vin", "GND", 1.0)
    c.add_capacitor("C1", "vin", "vout", C)
    c.add_resistor("R1", "vout", "GND", R)

    # Low frequency (1 Hz): blocked
    db_low = c.bode_magnitude_db("vin", "vout", [1.0])[0]
    assert db_low < -40.0

    # At cutoff fc: -3.01 dB, phase +45°
    db_fc = c.bode_magnitude_db("vin", "vout", [fc])[0]
    phase_fc = c.bode_phase_deg("vin", "vout", [fc])[0]
    assert abs(db_fc - (-3.0103)) < 0.05
    assert abs(phase_fc - 45.0) < 0.5

    # High frequency (100 kHz): passed, 0 dB
    db_high = c.bode_magnitude_db("vin", "vout", [100_000.0])[0]
    assert abs(db_high) < 0.01


def test_ascii_bode_rendering() -> None:
    c = Circuit()
    c.add_vsource("Vin", "vin", "GND", 1.0)
    c.add_resistor("R1", "vin", "vout", 1_000.0)
    c.add_capacitor("C1", "vout", "GND", 1e-6)

    plot = c.ascii_bode("vin", "vout", f_start=1.0, f_stop=100_000.0, n_points=30, width=50)
    assert "dB" in plot
    assert "(Hz)" in plot
    assert "─" in plot
    assert "│" in plot
    # Plot should contain at least 8 lines
    lines = plot.splitlines()
    assert len(lines) >= 8


def test_invalid_component_values_raise() -> None:
    c = Circuit()
    with pytest.raises(ValueError, match="resistance must be > 0"):
        c.add_resistor("R0", "a", "b", 0.0)
    with pytest.raises(ValueError, match="resistance must be > 0"):
        c.add_resistor("Rneg", "a", "b", -10.0)
    with pytest.raises(ValueError, match="capacitance must be > 0"):
        c.add_capacitor("C0", "a", "b", 0.0)
    with pytest.raises(ValueError, match="inductance must be > 0"):
        c.add_inductor("L0", "a", "b", 0.0)


def test_singular_circuit_raises() -> None:
    c = Circuit()
    # Floating node without reference to GND
    c.add_resistor("R1", "n1", "n2", 1000.0)
    with pytest.raises(ValueError, match="Circuito singular"):
        c.dc_solve()
