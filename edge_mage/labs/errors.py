"""Erros do motor de verificação de labs."""

from __future__ import annotations


class LabError(Exception):
    """Erro base do runner de labs."""


class ToolchainError(LabError):
    """Compilador/ferramenta ausente ou inutilizável."""


class LabNotFound(LabError):
    """Spec de lab não encontrada em content/labs/."""


class LabSpecError(LabError):
    """spec.yaml inválida."""
