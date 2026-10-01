"""Modelos de conteúdo e progresso."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


TaskType = Literal["mcq", "numeric", "fill", "code"]


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
    # unit_circle | sine_wave | vector | matrix | "" (heurística por id)
    animation: str = ""


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


@dataclass
class ProgressState:
    xp: int = 0
    completed_tasks: dict[str, bool] = field(default_factory=dict)
    completed_rooms: dict[str, bool] = field(default_factory=dict)
    streak_days: int = 0
    last_active: str = ""
    version: int = 1

    def task_key(self, track_id: str, room_id: str, task_id: str) -> str:
        return f"{track_id}/{room_id}/{task_id}"

    def room_key(self, track_id: str, room_id: str) -> str:
        return f"{track_id}/{room_id}"
