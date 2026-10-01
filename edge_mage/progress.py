"""Persistência local de progresso."""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

from edge_mage.models import ProgressState, Room, Track
from edge_mage.ranks import level_from_xp, next_rank, rank_from_xp, xp_for_next_level


def default_progress_path() -> Path:
    home = Path.home() / ".edge-mage"
    home.mkdir(parents=True, exist_ok=True)
    return home / "progress.json"


class ProgressStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_progress_path()
        self.state = self._load()

    def _load(self) -> ProgressState:
        if not self.path.exists():
            return ProgressState()
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return ProgressState(
            xp=int(raw.get("xp", 0)),
            completed_tasks=dict(raw.get("completed_tasks", {})),
            completed_rooms=dict(raw.get("completed_rooms", {})),
            unlocked_skills=dict(raw.get("unlocked_skills", {})),
            streak_days=int(raw.get("streak_days", 0)),
            last_active=str(raw.get("last_active", "")),
            version=int(raw.get("version", 2)),
        )

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "xp": self.state.xp,
            "completed_tasks": self.state.completed_tasks,
            "completed_rooms": self.state.completed_rooms,
            "unlocked_skills": self.state.unlocked_skills,
            "streak_days": self.state.streak_days,
            "last_active": self.state.last_active,
            "version": self.state.version,
        }
        self.path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def touch_streak(self) -> None:
        today = date.today().isoformat()
        if self.state.last_active == today:
            return
        if self.state.last_active:
            try:
                prev = date.fromisoformat(self.state.last_active)
                if (date.today() - prev).days == 1:
                    self.state.streak_days += 1
                elif (date.today() - prev).days > 1:
                    self.state.streak_days = 1
            except ValueError:
                self.state.streak_days = 1
        else:
            self.state.streak_days = 1
        self.state.last_active = today
        self.save()

    def is_task_done(self, track_id: str, room_id: str, task_id: str) -> bool:
        return bool(
            self.state.completed_tasks.get(self.state.task_key(track_id, room_id, task_id))
        )

    def is_room_done(self, track_id: str, room_id: str) -> bool:
        return bool(self.state.completed_rooms.get(self.state.room_key(track_id, room_id)))

    def is_skill_unlocked(self, skill_id: str) -> bool:
        return bool(self.state.unlocked_skills.get(skill_id))

    def unlock_skills(self, skill_ids: list[str]) -> list[str]:
        """Marca skills novas; retorna ids recém-desbloqueados."""
        newly: list[str] = []
        for sid in skill_ids:
            if not sid or self.state.unlocked_skills.get(sid):
                continue
            self.state.unlocked_skills[sid] = True
            newly.append(sid)
        return newly

    def mark_task(
        self, track_id: str, room_id: str, task_id: str, xp: int, room: Room
    ) -> dict:
        key = self.state.task_key(track_id, room_id, task_id)
        gained = 0
        leveled = False
        ranked_up = False
        room_completed = False
        before_level = level_from_xp(self.state.xp)
        before_rank = rank_from_xp(self.state.xp)

        first_completion = False
        if not self.state.completed_tasks.get(key):
            first_completion = True
            self.state.completed_tasks[key] = True
            self.state.xp += xp
            gained = xp
            self.touch_streak()

            all_done = all(
                self.is_task_done(track_id, room_id, t.id) for t in room.tasks
            )
            if all_done and not self.is_room_done(track_id, room_id):
                self.state.completed_rooms[self.state.room_key(track_id, room_id)] = True
                self.state.xp += room.xp_reward
                gained += room.xp_reward
                room_completed = True

            self.save()

        after_level = level_from_xp(self.state.xp)
        after_rank = rank_from_xp(self.state.xp)
        leveled = after_level > before_level
        ranked_up = after_rank.id != before_rank.id
        return {
            "gained": gained,
            "first_completion": first_completion,
            "task_xp": xp if first_completion else 0,
            "xp": self.state.xp,
            "level": after_level,
            "rank": after_rank,
            "leveled": leveled,
            "ranked_up": ranked_up,
            "room_completed": room_completed,
        }

    def room_progress(self, track_id: str, room: Room) -> tuple[int, int]:
        done = sum(1 for t in room.tasks if self.is_task_done(track_id, room.id, t.id))
        return done, len(room.tasks)

    def track_progress(self, track: Track) -> tuple[int, int]:
        done = sum(1 for r in track.rooms if self.is_room_done(track.id, r.id))
        return done, len(track.rooms)

    def is_track_unlocked(self, track: Track) -> bool:
        return self.state.xp >= track.unlock_xp

    def is_room_unlocked(self, track: Track, room: Room) -> bool:
        if not self.is_track_unlocked(track):
            return False
        return self.state.xp >= room.unlock_xp

    def profile_summary(self) -> dict:
        xp = self.state.xp
        level = level_from_xp(xp)
        rank = rank_from_xp(xp)
        into, need = xp_for_next_level(xp)
        nxt = next_rank(xp)
        return {
            "xp": xp,
            "level": level,
            "rank": rank,
            "into_level": into,
            "need_level": need,
            "next_rank": nxt,
            "streak": self.state.streak_days,
            "tasks_done": sum(1 for v in self.state.completed_tasks.values() if v),
            "rooms_done": sum(1 for v in self.state.completed_rooms.values() if v),
            "skills_done": sum(1 for v in self.state.unlocked_skills.values() if v),
            "updated": datetime.now(timezone.utc).isoformat(),
        }
