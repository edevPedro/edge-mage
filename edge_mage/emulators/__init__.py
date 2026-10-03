"""Neurotech / Edge educational emulators (synthetic EEG + Cortex-M stub)."""

from edge_mage.emulators.artifact_inject import inject_artifacts
from edge_mage.emulators.cortex_m_stub import CortexMPipelineStub
from edge_mage.emulators.latency_budget import from_cortex_window, stage_budget
from edge_mage.emulators.online_loop import run_online_stub
from edge_mage.emulators.synth_eeg import SynthEEGStream

__all__ = [
    "SynthEEGStream",
    "inject_artifacts",
    "CortexMPipelineStub",
    "stage_budget",
    "from_cortex_window",
    "run_online_stub",
]
