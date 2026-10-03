"""Neurotech / Edge educational emulators (synthetic EEG + Cortex-M stub)."""

from edge_mage.emulators.artifact_inject import inject_artifacts
from edge_mage.emulators.cortex_m_stub import CortexMPipelineStub
from edge_mage.emulators.synth_eeg import SynthEEGStream

__all__ = [
    "SynthEEGStream",
    "inject_artifacts",
    "CortexMPipelineStub",
]
