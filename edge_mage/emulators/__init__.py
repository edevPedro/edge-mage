"""Neurotech / Edge educational emulators (synthetic EEG + Cortex-M stub)."""

from edge_mage.emulators.artifact_inject import inject_artifacts
from edge_mage.emulators.cortex_m_emu import CortexMEmulator
from edge_mage.emulators.cortex_m_stub import CortexMPipelineStub
from edge_mage.emulators.latency_budget import from_cortex_window, stage_budget
from edge_mage.emulators.online_loop import run_online_stub
from edge_mage.emulators.signal_viz import (
    compute_bandpowers,
    compute_simple_psd,
    render_ascii_spectrogram,
    render_ascii_spectrum,
    render_ascii_wave,
    render_bandpower_bars,
    render_multichannel_waves,
)
from edge_mage.emulators.spice_lite import Circuit
from edge_mage.emulators.synth_eeg import SynthEEGStream

__all__ = [
    "SynthEEGStream",
    "inject_artifacts",
    "CortexMPipelineStub",
    "CortexMEmulator",
    "Circuit",
    "render_ascii_wave",
    "render_multichannel_waves",
    "render_ascii_spectrum",
    "render_bandpower_bars",
    "render_ascii_spectrogram",
    "compute_simple_psd",
    "compute_bandpowers",
    "stage_budget",
    "from_cortex_window",
    "run_online_stub",
]

