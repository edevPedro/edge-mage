"""Erros do motor de roadmap/verificação."""

from __future__ import annotations


class RoadmapError(Exception):
    """Base para erros do roadmap."""


class RoadmapNotFound(RoadmapError):
    """roadmap/ ou challenges/ ausentes."""


class RoadmapSpecError(RoadmapError):
    """YAML inválido ou contrato incompleto."""


class ChallengeNotFound(RoadmapError):
    """Desafio inexistente."""


class VerifyError(RoadmapError):
    """Falha ao executar o verificador."""


class WorkDirError(RoadmapError):
    """Diretório de trabalho do desafio ausente/inválido."""
