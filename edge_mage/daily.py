"""Daily Run — pacote ~20 min (review + new + skill drop)."""

from __future__ import annotations

import hashlib
import random
from datetime import date
from typing import Any

from edge_mage.curriculum import next_open_room, pedagogical_rooms
from edge_mage.models import Room, Task, Track


def _seed_for(day: str) -> int:
    h = hashlib.sha256(day.encode()).hexdigest()
    return int(h[:8], 16)


def _pick_review(
    store, tracks: list[Track], rng: random.Random
) -> tuple[Track, Room, Task] | None:
    cleared: list[tuple[Track, Room, Task]] = []
    for track, room in pedagogical_rooms(tracks):
        if not store.is_room_done(track.id, room.id):
            continue
        for t in room.tasks:
            if t.type in {"numeric", "mcq", "fill"} and not t.mastery_variant:
                cleared.append((track, room, t))
    if not cleared:
        return None
    return rng.choice(cleared)


def _variant_numeric(task: Task, rng: random.Random) -> Task:
    """Cria variante leve de numeric (mesma fórmula, números trocados se possível)."""
    if task.type != "numeric":
        return task
    # escala leve do expected para "related numeric"
    scale = rng.choice([0.5, 2.0, 1.0, 1.5])
    expected = float(task.answer) * scale
    # arredonda de forma amigável
    if abs(expected) >= 10:
        expected = round(expected, 1)
    else:
        expected = round(expected, 4)
    return Task(
        id=f"{task.id}-daily",
        type="numeric",
        prompt=f"[Review] {task.prompt}  (variante do dia · escala {scale:g})",
        xp=max(5, task.xp // 2),
        answer=expected,
        tolerance=max(task.tolerance, abs(expected) * 0.02 + 1e-3),
        relative_tolerance=task.relative_tolerance,
        hint=task.hint,
        mastery_variant=True,
    )


def build_daily_run(store, tracks: list[Track], day: str | None = None) -> dict[str, Any]:
    """Gera ou reutiliza o pacote do dia."""
    day = day or date.today().isoformat()
    existing = store.get_daily_run()
    if existing.get("date") == day and existing.get("review") and existing.get("new"):
        return existing

    rng = random.Random(_seed_for(day))
    review_pack = _pick_review(store, tracks, rng)
    nxt = next_open_room(store, tracks)

    review_payload = None
    if review_pack:
        tr, rm, tk = review_pack
        variant = _variant_numeric(tk, rng) if tk.type == "numeric" else tk
        review_payload = {
            "track_id": tr.id,
            "room_id": rm.id,
            "task_id": variant.id,
            "base_task_id": tk.id,
            "prompt": variant.prompt,
            "type": variant.type,
            "xp": variant.xp,
            "answer": variant.answer,
            "tolerance": variant.tolerance,
            "relative_tolerance": variant.relative_tolerance,
            "choices": variant.choices,
            "answers": variant.answers,
            "hint": variant.hint,
        }

    new_payload = None
    if nxt:
        track, room = nxt
        # prefer task ainda não feita; senão primeira
        pending = [t for t in room.tasks if not store.is_task_done(track.id, room.id, t.id)]
        task = pending[0] if pending else room.tasks[0]
        new_payload = {
            "track_id": track.id,
            "room_id": room.id,
            "task_id": task.id,
        }

    data = {
        "date": day,
        "step": 0,  # 0 review, 1 new, 2 done
        "review_done": False,
        "new_done": False,
        "review": review_payload,
        "new": new_payload,
    }
    store.set_daily_run(data)
    return data


def daily_task_from_payload(payload: dict[str, Any]) -> Task:
    return Task(
        id=str(payload["task_id"]),
        type=payload.get("type") or "numeric",
        prompt=str(payload.get("prompt") or ""),
        xp=int(payload.get("xp", 8)),
        answer=payload.get("answer"),
        tolerance=float(payload.get("tolerance", 1e-3)),
        relative_tolerance=float(payload.get("relative_tolerance", 1e-3)),
        choices=list(payload.get("choices") or []),
        answers=list(payload.get("answers") or []),
        hint=str(payload.get("hint") or ""),
        mastery_variant=True,
    )
