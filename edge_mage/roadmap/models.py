"""Modelos do roadmap (tronco + ramos) e do contrato de desafio/nó.

Ver PLATFORM.md §3 (grafo tronco/ramos) e §6 (contrato de desafio).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Source:
    """Fonte de verdade primária com seção exata (§4)."""

    name: str
    url: str = ""
    section: str = ""
    why: str = ""

    def label(self) -> str:
        if self.section:
            return f"{self.name} ({self.section})"
        return self.name


@dataclass(frozen=True)
class DailyGoal:
    """Menor passo com verificador (§6)."""

    id: str
    goal: str
    verify: str = ""  # override do cmd do desafio; vazio → challenge.verify.cmd
    lens: str | None = None


@dataclass(frozen=True)
class VerifyConfig:
    cmd: str
    timeout_s: float = 120.0
    runs: int = 3
    noise_cv: float = 0.15


@dataclass(frozen=True)
class ExitCriteria:
    metric: str = ""
    target: str = ""


@dataclass(frozen=True)
class Challenge:
    id: str
    track: str
    title: str
    dir: Path
    summary: str = ""
    timebox_days: int = 21
    work_dir: str = ""
    exit_criteria: ExitCriteria = field(default_factory=ExitCriteria)
    sources: list[Source] = field(default_factory=list)
    daily_goals: list[DailyGoal] = field(default_factory=list)
    lens: str | None = None
    verify: VerifyConfig = field(default_factory=lambda: VerifyConfig(cmd=""))
    readme_sections: list[str] = field(default_factory=list)

    def goal(self, goal_id: str) -> DailyGoal | None:
        for g in self.daily_goals:
            if g.id == goal_id:
                return g
        return None

    def verify_command(self, goal: DailyGoal | None) -> str:
        if goal is not None and goal.verify:
            return goal.verify
        return self.verify.cmd

    def resolved_work_dir(self, fallback_root: Path | None = None) -> Path:
        """Diretório de trabalho do aluno (fora do repo)."""
        if self.work_dir:
            return Path(self.work_dir).expanduser()
        base = fallback_root if fallback_root is not None else self.dir.parent.parent / ".."
        return (base / self.id).resolve()

    def scaffold_dir(self) -> Path:
        return self.dir / "scaffold"


@dataclass(frozen=True)
class OpenWhen:
    """Ramo abre quando (semana >= week) OU (desafio concluído), o que vier primeiro (§3/§5)."""

    week: int | None = None
    challenge: str | None = None

    def describe(self) -> str:
        parts: list[str] = []
        if self.week is not None:
            parts.append(f"semana {self.week}")
        if self.challenge:
            parts.append(f"{self.challenge} concluído")
        return " ou ".join(parts) if parts else "manual"


@dataclass(frozen=True)
class Branch:
    id: str
    title: str
    opens_when: OpenWhen = field(default_factory=OpenWhen)
    weekly_cap_pct: float = 10.0
    content: str = ""


@dataclass(frozen=True)
class RoadmapRules:
    trunk_min_pct: float = 65.0
    branches_max_pct: float = 35.0
    max_active_branches: int = 2
    stagnation_weeks: int = 2
    dispersion_alert_pct: float = 10.0
    rollover_max: int = 1


@dataclass(frozen=True)
class Roadmap:
    version: int = 1
    daily_minutes: int = 60
    weekend_review: bool = True
    trunk_track: str = "A"
    trunk_order: list[str] = field(default_factory=list)
    rules: RoadmapRules = field(default_factory=RoadmapRules)
    branches: list[Branch] = field(default_factory=list)
    challenges: dict[str, Challenge] = field(default_factory=dict)

    def trunk_challenges(self) -> list[Challenge]:
        out: list[Challenge] = []
        for cid in self.trunk_order:
            ch = self.challenges.get(cid)
            if ch is not None:
                out.append(ch)
        return out

    def challenge(self, cid: str) -> Challenge | None:
        return self.challenges.get(cid)

    def branch(self, bid: str) -> Branch | None:
        for b in self.branches:
            if b.id == bid:
                return b
        return None
