"""Carrega trilhas YAML + lições Markdown."""

from __future__ import annotations

from pathlib import Path

import yaml

from edge_mage.models import Room, Task, Track


def content_root() -> Path:
    # Prefer project content/ next to package parent
    here = Path(__file__).resolve().parent.parent / "content"
    if here.exists():
        return here
    return Path.cwd() / "content"


def _load_tasks(raw_tasks: list) -> list[Task]:
    tasks: list[Task] = []
    for raw in raw_tasks or []:
        tasks.append(
            Task(
                id=str(raw["id"]),
                type=raw["type"],
                prompt=str(raw["prompt"]),
                xp=int(raw.get("xp", 10)),
                choices=list(raw.get("choices") or []),
                answer=raw.get("answer"),
                answers=list(raw.get("answers") or []),
                tolerance=float(raw.get("tolerance", 1e-3)),
                relative_tolerance=float(raw.get("relative_tolerance", 1e-3)),
                code_template=str(raw.get("code_template") or ""),
                code_tests=str(raw.get("code_tests") or ""),
                expected_stdout=str(raw.get("expected_stdout") or ""),
                hint=str(raw.get("hint") or ""),
            )
        )
    return tasks


def load_room(room_dir: Path) -> Room:
    meta_path = room_dir / "room.yaml"
    meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    lesson_path = room_dir / "lesson.md"
    lesson = lesson_path.read_text(encoding="utf-8") if lesson_path.exists() else ""
    return Room(
        id=str(meta["id"]),
        title=str(meta["title"]),
        summary=str(meta.get("summary") or ""),
        xp_reward=int(meta.get("xp_reward", 15)),
        unlock_xp=int(meta.get("unlock_xp", 0)),
        lesson_md=lesson,
        tasks=_load_tasks(meta.get("tasks") or []),
        path=str(room_dir),
        animation=str(meta.get("animation") or ""),
    )


def load_track(track_dir: Path) -> Track:
    meta = yaml.safe_load((track_dir / "track.yaml").read_text(encoding="utf-8"))
    rooms_root = track_dir / "rooms"
    rooms: list[Room] = []
    if rooms_root.exists():
        for room_dir in sorted(p for p in rooms_root.iterdir() if p.is_dir()):
            if (room_dir / "room.yaml").exists():
                rooms.append(load_room(room_dir))
    return Track(
        id=str(meta["id"]),
        title=str(meta["title"]),
        summary=str(meta.get("summary") or ""),
        order=int(meta.get("order", 99)),
        unlock_xp=int(meta.get("unlock_xp", 0)),
        icon=str(meta.get("icon") or "◆"),
        rooms=rooms,
        path=str(track_dir),
        scaffold=bool(meta.get("scaffold", False)),
    )


def load_all_tracks(root: Path | None = None) -> list[Track]:
    base = root or content_root()
    tracks_dir = base / "tracks"
    tracks: list[Track] = []
    if not tracks_dir.exists():
        return tracks
    for track_dir in sorted(p for p in tracks_dir.iterdir() if p.is_dir()):
        if (track_dir / "track.yaml").exists():
            tracks.append(load_track(track_dir))
    tracks.sort(key=lambda t: t.order)
    return tracks


def find_track(tracks: list[Track], track_id: str) -> Track | None:
    for t in tracks:
        if t.id == track_id:
            return t
    return None


def find_room(track: Track, room_id: str) -> Room | None:
    for r in track.rooms:
        if r.id == room_id:
            return r
    return None
