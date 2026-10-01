"""Persistência local de progresso + mana de streak + daily/mastery/rituais."""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from edge_mage.courses import COURSE_EDGE, COURSE_FUNDAMENTALS, COURSE_SYSTEMS
from edge_mage.models import ProgressState, Room, Track
from edge_mage.paths import progress_path
from edge_mage.ranks import (
    effective_rank,
    global_rank_from_flags,
    level_from_xp,
    next_global_rank,
    next_rank,
    rank_from_xp,
    xp_for_next_level,
)

STREAK_MANA_THRESHOLD = 3
STREAK_MANA_MULT = 1.25

# Shared-core aliases: clearing either id credits both (no Systems↔Edge farm).
ROOM_CREDIT_ALIASES: dict[str, tuple[str, ...]] = {
    "vectors": ("vetores",),
    "vetores": ("vectors",),
    "trig-waves": ("trigonometria", "ondas"),
    "trigonometria": ("trig-waves",),
    "ondas": ("trig-waves",),
    "bits": ("llvm-bits",),
    "intro-asm": ("sys-asm-read", "llvm-asm-host"),
}


def default_progress_path() -> Path:
    return progress_path()


class ProgressStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_progress_path()
        self.state = self._load()

    def _load(self) -> ProgressState:
        if not self.path.exists():
            return ProgressState()
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        by_id = dict(raw.get("completed_rooms_by_id", {}))
        # backfill room_id credit from legacy track/room keys
        if not by_id:
            for key, done in dict(raw.get("completed_rooms", {})).items():
                if done and "/" in str(key):
                    by_id[str(key).rsplit("/", 1)[-1]] = True
        return ProgressState(
            xp=int(raw.get("xp", 0)),
            completed_tasks=dict(raw.get("completed_tasks", {})),
            completed_rooms=dict(raw.get("completed_rooms", {})),
            completed_rooms_by_id=by_id,
            unlocked_skills=dict(raw.get("unlocked_skills", {})),
            rituals=dict(raw.get("rituals", {})),
            mastery={k: int(v) for k, v in dict(raw.get("mastery", {})).items()},
            streak_days=int(raw.get("streak_days", 0)),
            last_active=str(raw.get("last_active", "")),
            daily_run=dict(raw.get("daily_run", {})),
            daily_combo=int(raw.get("daily_combo", 0)),
            combo_date=str(raw.get("combo_date", "")),
            unlocked_tracks=dict(raw.get("unlocked_tracks", {})),
            courses=dict(raw.get("courses", {})),
            evidence=dict(raw.get("evidence", {})),
            version=int(raw.get("version", 4)),
        )

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "xp": self.state.xp,
            "completed_tasks": self.state.completed_tasks,
            "completed_rooms": self.state.completed_rooms,
            "completed_rooms_by_id": self.state.completed_rooms_by_id,
            "unlocked_skills": self.state.unlocked_skills,
            "rituals": self.state.rituals,
            "mastery": self.state.mastery,
            "streak_days": self.state.streak_days,
            "last_active": self.state.last_active,
            "daily_run": self.state.daily_run,
            "daily_combo": self.state.daily_combo,
            "combo_date": self.state.combo_date,
            "unlocked_tracks": self.state.unlocked_tracks,
            "courses": self.state.courses,
            "evidence": self.state.evidence,
            "version": self.state.version,
        }
        self.path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {
            "xp": self.state.xp,
            "completed_rooms": self.state.completed_rooms,
            "completed_rooms_by_id": self.state.completed_rooms_by_id,
            "courses": self.state.courses,
            "rituals": self.state.rituals,
            "version": self.state.version,
            "last_active": self.state.last_active,
        }

    def xp_multiplier(self) -> float:
        if self.state.streak_days >= STREAK_MANA_THRESHOLD:
            return STREAK_MANA_MULT
        return 1.0

    def touch_streak(self) -> None:
        today = date.today().isoformat()
        if self.state.last_active == today:
            return
        if self.state.last_active:
            try:
                prev = date.fromisoformat(self.state.last_active)
                gap = (date.today() - prev).days
                if gap == 1:
                    self.state.streak_days += 1
                elif gap > 1:
                    self.state.streak_days = 1
            except ValueError:
                self.state.streak_days = 1
        else:
            self.state.streak_days = 1
        self.state.last_active = today
        self.save()

    def bump_daily_combo(self) -> int:
        today = date.today().isoformat()
        if self.state.combo_date != today:
            self.state.combo_date = today
            self.state.daily_combo = 1
        else:
            self.state.daily_combo = min(4, self.state.daily_combo + 1)
        self.save()
        return self.state.daily_combo

    def is_task_done(self, track_id: str, room_id: str, task_id: str) -> bool:
        return bool(
            self.state.completed_tasks.get(self.state.task_key(track_id, room_id, task_id))
        )

    def is_room_done(self, track_id: str, room_id: str) -> bool:
        if self.state.completed_rooms.get(self.state.room_key(track_id, room_id)):
            return True
        # shared core: single room_id credit (+ aliases)
        if self.state.completed_rooms_by_id.get(room_id):
            return True
        for alias in ROOM_CREDIT_ALIASES.get(room_id, ()):
            if self.state.completed_rooms_by_id.get(alias):
                return True
        return False

    def mark_room_id(self, room_id: str) -> None:
        """Credit room_id once + shared aliases (Systems↔Edge anti-farm)."""
        self.state.completed_rooms_by_id[room_id] = True
        for alias in ROOM_CREDIT_ALIASES.get(room_id, ()):
            self.state.completed_rooms_by_id[alias] = True

    def is_skill_unlocked(self, skill_id: str) -> bool:
        return bool(self.state.unlocked_skills.get(skill_id))

    def has_ritual(self, ritual_id: str) -> bool:
        return bool(self.state.rituals.get(ritual_id))

    def course_meta(self, course_id: str) -> dict[str, Any]:
        raw = self.state.courses.get(course_id)
        return dict(raw) if isinstance(raw, dict) else {}

    def set_course_flag(self, course_id: str, **flags: Any) -> None:
        cur = self.course_meta(course_id)
        cur.update(flags)
        self.state.courses[course_id] = cur
        self.save()

    def has_mago_base(self) -> bool:
        fund = self.course_meta(COURSE_FUNDAMENTALS)
        if fund.get("cleared") or fund.get("mago_base"):
            return True
        # heuristic: shared core + clearance (trig-waves recommended, not hard gate)
        needed = {"intro-asm", "bits", "vectors", "fundamentals-clear"}
        done = set(k for k, v in self.state.completed_rooms_by_id.items() if v)
        return needed.issubset(done) or bool(fund.get("cleared"))

    def has_systems_boss(self) -> bool:
        sys = self.course_meta(COURSE_SYSTEMS)
        return bool(sys.get("boss_craft") or self.has_ritual("systems-boss-craft"))

    def has_evidence(self) -> bool:
        """Shared math / portfolio evidence — never XP alone; separate from boss rites."""
        return bool(
            self.state.evidence.get("portfolio")
            or self.state.evidence.get("signed")
            or self.state.evidence.get("shared_math")
            or self.has_ritual("shared-math")
        )

    def unlock_skills(self, skill_ids: list[str]) -> list[str]:
        newly: list[str] = []
        for sid in skill_ids:
            if not sid or self.state.unlocked_skills.get(sid):
                continue
            self.state.unlocked_skills[sid] = True
            newly.append(sid)
        return newly

    def complete_ritual(self, ritual_id: str) -> bool:
        if not ritual_id or self.state.rituals.get(ritual_id):
            return False
        self.state.rituals[ritual_id] = True
        self.save()
        return True

    def mastery_count(self, track_id: str, room_id: str) -> int:
        return int(self.state.mastery.get(self.state.room_key(track_id, room_id), 0))

    def bump_mastery(self, track_id: str, room_id: str) -> int:
        key = self.state.room_key(track_id, room_id)
        cur = int(self.state.mastery.get(key, 0))
        if cur >= 3:
            return cur
        cur += 1
        self.state.mastery[key] = cur
        self.save()
        return cur

    def award_xp(self, base: int) -> int:
        """Aplica multiplicador de streak mana."""
        gained = int(round(base * self.xp_multiplier()))
        self.state.xp += gained
        return gained

    def mark_task(
        self,
        track_id: str,
        room_id: str,
        task_id: str,
        xp: int,
        room: Room,
        *,
        mastery: bool = False,
    ) -> dict:
        key = self.state.task_key(track_id, room_id, task_id)
        gained = 0
        room_completed = False
        before_level = level_from_xp(self.state.xp)
        before_rank = effective_rank(self.state.xp, self.has_ritual("on-device"))

        first_completion = False
        mastery_bump = 0

        if mastery:
            base = max(1, xp // 3)
            gained = self.award_xp(base)
            self.touch_streak()
            mastery_bump = self.bump_mastery(track_id, room_id)
            combo = self.bump_daily_combo()
            self.save()
        elif not self.state.completed_tasks.get(key):
            first_completion = True
            self.state.completed_tasks[key] = True
            gained = self.award_xp(xp)
            self.touch_streak()
            combo = self.bump_daily_combo()

            all_done = all(
                self.is_task_done(track_id, room_id, t.id) for t in room.tasks
            )
            if all_done and not self.state.completed_rooms.get(
                self.state.room_key(track_id, room_id)
            ):
                self.state.completed_rooms[self.state.room_key(track_id, room_id)] = True
                self.mark_room_id(room_id)
                gained += self.award_xp(room.xp_reward)
                room_completed = True
                if room.elite_skill:
                    self.unlock_skills([room.elite_skill])
                if room.unlocks_track:
                    self.state.unlocked_tracks[room.unlocks_track] = True
                if room.boss:
                    self.state.rituals[room.id] = True
                if room_id == "fundamentals-clear" or room.id == "fundamentals-clear":
                    self.state.courses.setdefault(COURSE_FUNDAMENTALS, {})
                    self.state.courses[COURSE_FUNDAMENTALS]["cleared"] = True
                    self.state.courses[COURSE_FUNDAMENTALS]["mago_base"] = True

            self.save()
        else:
            combo = self.state.daily_combo

        after_level = level_from_xp(self.state.xp)
        after_rank = effective_rank(self.state.xp, self.has_ritual("on-device"))
        return {
            "gained": gained,
            "first_completion": first_completion,
            "task_xp": gained if first_completion or mastery else 0,
            "xp": self.state.xp,
            "level": after_level,
            "rank": after_rank,
            "leveled": after_level > before_level,
            "ranked_up": after_rank.id != before_rank.id,
            "room_completed": room_completed,
            "combo": combo if first_completion or mastery else self.state.daily_combo,
            "mult": self.xp_multiplier(),
            "mastery": mastery_bump,
            "before_level": before_level,
            "into_level": xp_for_next_level(self.state.xp)[0],
            "need_level": xp_for_next_level(self.state.xp)[1],
        }

    def room_progress(self, track_id: str, room: Room) -> tuple[int, int]:
        done = sum(1 for t in room.tasks if self.is_task_done(track_id, room.id, t.id))
        return done, len(room.tasks)

    def track_progress(self, track: Track) -> tuple[int, int]:
        done = sum(1 for r in track.rooms if self.is_room_done(track.id, r.id))
        return done, len(track.rooms)

    def is_track_unlocked(self, track: Track) -> bool:
        xp_ok = self.state.xp >= track.unlock_xp
        boss_ok = bool(self.state.unlocked_tracks.get(track.id))
        if not xp_ok and not boss_ok:
            return False
        if track.requires_skills:
            if not all(self.is_skill_unlocked(s) for s in track.requires_skills):
                return False
        if track.requires_ritual and not self.has_ritual(track.requires_ritual):
            return False
        return True

    def is_room_unlocked(self, track: Track, room: Room) -> bool:
        if not self.is_track_unlocked(track):
            return False
        if self.state.xp < room.unlock_xp and not room.boss:
            return False
        if room.requires_skills:
            if not all(self.is_skill_unlocked(s) for s in room.requires_skills):
                return False
        return True

    def missing_skills_for_room(self, room: Room) -> list[str]:
        return [s for s in room.requires_skills if not self.is_skill_unlocked(s)]

    def get_daily_run(self) -> dict[str, Any]:
        return dict(self.state.daily_run or {})

    def set_daily_run(self, data: dict[str, Any]) -> None:
        self.state.daily_run = dict(data)
        self.save()

    def global_rank(self):
        edge_progress = bool(
            self.course_meta(COURSE_EDGE).get("started")
            or self.state.xp > 0
            or any(self.state.completed_rooms.values())
        )
        systems_progress = bool(
            self.course_meta(COURSE_SYSTEMS).get("started") or self.has_systems_boss()
        )
        return global_rank_from_flags(
            has_mago_base=self.has_mago_base(),
            has_systems_boss=self.has_systems_boss(),
            has_edge_on_device=self.has_ritual("on-device"),
            has_evidence=self.has_evidence(),
            any_advanced_progress=edge_progress or systems_progress,
        )

    def profile_summary(self) -> dict:
        xp = self.state.xp
        level = level_from_xp(xp)
        has_od = self.has_ritual("on-device")
        rank = effective_rank(xp, has_od)
        into, need = xp_for_next_level(xp)
        nxt = next_rank(xp)
        if rank.id == "arquimago" and xp >= 2900 and not has_od:
            from edge_mage.ranks import EDGE_RANKS

            nxt = next(r for r in EDGE_RANKS if r.id == "edge_mage")
        g_rank = self.global_rank()
        return {
            "xp": xp,
            "level": level,
            "rank": rank,
            "global_rank": g_rank,
            "next_global_rank": next_global_rank(g_rank.id),
            "mago_base": self.has_mago_base(),
            "into_level": into,
            "need_level": need,
            "next_rank": nxt,
            "streak": self.state.streak_days,
            "mult": self.xp_multiplier(),
            "combo": self.state.daily_combo if self.state.combo_date == date.today().isoformat() else 0,
            "tasks_done": sum(1 for v in self.state.completed_tasks.values() if v),
            "rooms_done": sum(1 for v in self.state.completed_rooms.values() if v),
            "skills_done": sum(1 for v in self.state.unlocked_skills.values() if v),
            "rituals_done": sum(1 for v in self.state.rituals.values() if v),
            "on_device": has_od,
            "updated": datetime.now(timezone.utc).isoformat(),
        }
