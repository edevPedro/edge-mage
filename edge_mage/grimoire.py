"""Grimório de habilidades — carregamento e unlock."""

from __future__ import annotations

from pathlib import Path

import yaml

from edge_mage.content import content_root
from edge_mage.models import Skill


def skills_path(root: Path | None = None) -> Path:
    return (root or content_root()) / "grimoire" / "skills.yaml"


def load_skills(root: Path | None = None) -> list[Skill]:
    path = skills_path(root)
    if not path.exists():
        return []
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    items = raw.get("skills") or []
    skills: list[Skill] = []
    for item in items:
        skills.append(
            Skill(
                id=str(item["id"]),
                name=str(item["name"]),
                description=str(item.get("description") or ""),
                glyph=str(item.get("glyph") or "◆"),
                unlock_room=str(item.get("unlock_room") or ""),
                unlock_track=str(item.get("unlock_track") or ""),
            )
        )
    return skills


def skills_for_room(
    skills: list[Skill], *, track_id: str, room_id: str
) -> list[Skill]:
    out: list[Skill] = []
    for s in skills:
        if s.unlock_room != room_id:
            continue
        if s.unlock_track and s.unlock_track != track_id:
            continue
        out.append(s)
    return out


def skill_by_id(skills: list[Skill], skill_id: str) -> Skill | None:
    for s in skills:
        if s.id == skill_id:
            return s
    return None
