"""Modelos de conteúdo e progresso."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


TaskType = Literal["mcq", "numeric", "fill", "code", "ritual"]
ResourceKind = Literal["docs", "video", "paper", "book", "tool", "other"]


@dataclass
class Resource:
    title: str
    url: str
    kind: ResourceKind = "docs"


@dataclass
class Task:
    id: str
    type: TaskType
    prompt: str
    xp: int = 10
    choices: list[str] = field(default_factory=list)
    answer: Any = None
    answers: list[str] = field(default_factory=list)
    tolerance: float = 1e-3
    relative_tolerance: float = 1e-3
    code_template: str = ""
    code_tests: str = ""
    expected_stdout: str = ""
    hint: str = ""
    # ritual: nome do artefato em study-log/artifacts/<id>.md
    ritual_id: str = ""
    mastery_variant: bool = False
    # fill: optional regex (Systems FLAG packs from web catalog)
    answer_pattern: str = ""


@dataclass
class Room:
    id: str
    title: str
    summary: str
    xp_reward: int
    unlock_xp: int
    lesson_md: str
    tasks: list[Task]
    path: str
    animation: str = ""
    story_md: str = ""
    concept_md: str = ""
    boss: bool = False
    requires_skills: list[str] = field(default_factory=list)
    elite_skill: str = ""  # skill id concedida ao concluir boss
    unlocks_track: str = ""  # ex.: edge-ai após Softmax Estável
    resources: list[Resource] = field(default_factory=list)
    shared: bool = False  # shared-core room (single room_id credit)
    course: str = ""  # optional course tag: fundamentals|systems|edge


@dataclass
class Track:
    id: str
    title: str
    summary: str
    order: int
    unlock_xp: int
    icon: str
    rooms: list[Room]
    path: str
    scaffold: bool = False
    requires_skills: list[str] = field(default_factory=list)
    requires_ritual: str = ""
    course: str = ""


@dataclass
class Skill:
    id: str
    name: str
    description: str
    glyph: str = "◆"
    unlock_room: str = ""
    unlock_track: str = ""
    elite: bool = False


@dataclass
class ProgressState:
    xp: int = 0
    completed_tasks: dict[str, bool] = field(default_factory=dict)
    completed_rooms: dict[str, bool] = field(default_factory=dict)
    # Shared credit: room_id → done (systems + edge maps reference same ids)
    completed_rooms_by_id: dict[str, bool] = field(default_factory=dict)
    unlocked_skills: dict[str, bool] = field(default_factory=dict)
    rituals: dict[str, bool] = field(default_factory=dict)
    mastery: dict[str, int] = field(default_factory=dict)  # room_key -> 0..3
    streak_days: int = 0
    last_active: str = ""
    daily_run: dict[str, Any] = field(default_factory=dict)
    daily_combo: int = 0
    combo_date: str = ""
    unlocked_tracks: dict[str, bool] = field(default_factory=dict)
    # per-course flags: { fundamentals: { cleared: bool }, … }
    courses: dict[str, Any] = field(default_factory=dict)
    evidence: dict[str, bool] = field(default_factory=dict)
    version: int = 4

    def task_key(self, track_id: str, room_id: str, task_id: str) -> str:
        return f"{track_id}/{room_id}/{task_id}"

    def room_key(self, track_id: str, room_id: str) -> str:
        return f"{track_id}/{room_id}"
