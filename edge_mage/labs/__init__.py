"""Motor de verificação de labs (C++) — Fase 1 do e-mage.

API pública:
    run_lab(lab_id, ...)  -> LabResult
    init_lab(lab_id, ...) -> (work_dir, copied)
    format_result(result) -> str
    available_labs()      -> list[str]
"""

from __future__ import annotations

from edge_mage.labs.bench import Aggregate, MetricSummary, aggregate_runs, percentile
from edge_mage.labs.errors import LabError, LabNotFound, LabSpecError, ToolchainError
from edge_mage.labs.evidence import build_record, code_hash, read_latest, write_evidence
from edge_mage.labs.runner import LabResult, format_result, init_lab, run_lab
from edge_mage.labs.spec import LabSpec, available_labs, load_spec, labs_root
from edge_mage.labs.toolchain import Compiler, find_cpp_compiler, has_cpp_toolchain

__all__ = [
    "Aggregate",
    "Compiler",
    "LabError",
    "LabNotFound",
    "LabResult",
    "LabSpec",
    "LabSpecError",
    "MetricSummary",
    "ToolchainError",
    "aggregate_runs",
    "available_labs",
    "build_record",
    "code_hash",
    "find_cpp_compiler",
    "format_result",
    "has_cpp_toolchain",
    "init_lab",
    "labs_root",
    "load_spec",
    "percentile",
    "read_latest",
    "run_lab",
    "write_evidence",
]
