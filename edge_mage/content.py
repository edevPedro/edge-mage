"""Carrega trilhas YAML + lições Markdown + cursos (fundamentals/systems/edge)."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from edge_mage.courses import COURSE_EDGE, COURSE_FUNDAMENTALS, COURSE_SYSTEMS
from edge_mage.models import Resource, Room, Task, Track
from edge_mage.paths import packs_dir


def content_root() -> Path:
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
                ritual_id=str(raw.get("ritual_id") or ""),
                mastery_variant=bool(raw.get("mastery_variant", False)),
            )
        )
    return tasks


def _load_resources(raw: list | None) -> list[Resource]:
    out: list[Resource] = []
    for item in raw or []:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or "").strip()
        url = str(item.get("url") or "").strip()
        if not title or not url:
            continue
        kind = str(item.get("kind") or "docs")
        if kind not in {"docs", "video", "paper", "book", "tool", "other"}:
            kind = "other"
        out.append(Resource(title=title, url=url, kind=kind))  # type: ignore[arg-type]
    return out


def _read_md(path: Path, fallback: str = "") -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return fallback


def load_room(room_dir: Path) -> Room:
    meta_path = room_dir / "room.yaml"
    meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    lesson = _read_md(room_dir / "lesson.md")
    story = _read_md(room_dir / "story.md", str(meta.get("story") or ""))
    concept = _read_md(room_dir / "concept.md", str(meta.get("concept") or ""))
    req = meta.get("requires_skills") or []
    if isinstance(req, str):
        req = [req]
    return Room(
        id=str(meta["id"]),
        title=str(meta["title"]),
        summary=str(meta.get("summary") or ""),
        xp_reward=int(meta.get("xp_reward", 15)),
        unlock_xp=int(meta.get("unlock_xp", 0)),
        lesson_md=lesson,
        story_md=story,
        concept_md=concept,
        tasks=_load_tasks(meta.get("tasks") or []),
        path=str(room_dir),
        animation=str(meta.get("animation") or ""),
        boss=bool(meta.get("boss", False)),
        requires_skills=[str(x) for x in req],
        elite_skill=str(meta.get("elite_skill") or ""),
        unlocks_track=str(meta.get("unlocks_track") or ""),
        resources=_load_resources(meta.get("resources")),
        shared=bool(meta.get("shared", False)),
        course=str(meta.get("course") or ""),
    )


def load_track(track_dir: Path) -> Track:
    meta = yaml.safe_load((track_dir / "track.yaml").read_text(encoding="utf-8"))
    rooms_root = track_dir / "rooms"
    rooms: list[Room] = []
    if rooms_root.exists():
        for room_dir in sorted(p for p in rooms_root.iterdir() if p.is_dir()):
            if (room_dir / "room.yaml").exists():
                rooms.append(load_room(room_dir))
    req = meta.get("requires_skills") or []
    if isinstance(req, str):
        req = [req]
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
        requires_skills=[str(x) for x in req],
        requires_ritual=str(meta.get("requires_ritual") or ""),
        course=str(meta.get("course") or ""),
    )


def load_all_tracks(root: Path | None = None) -> list[Track]:
    """Edge course: content/tracks (current TUI content)."""
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


def load_shared_rooms(root: Path | None = None) -> list[Room]:
    base = (root or content_root()) / "shared"
    rooms: list[Room] = []
    if not base.exists():
        return rooms
    for room_dir in sorted(p for p in base.iterdir() if p.is_dir()):
        if (room_dir / "room.yaml").exists():
            room = load_room(room_dir)
            room.shared = True
            rooms.append(room)
    return rooms


def _room_from_pack_entry(entry: dict, path_hint: str) -> Room:
    tasks_raw = entry.get("tasks")
    if not tasks_raw:
        tasks_raw = [
            {
                "id": "ack",
                "type": "mcq",
                "prompt": "Stub room — sync catalog when online. Continue?",
                "xp": 5,
                "answer": 0,
                "choices": ["Yes — acknowledge", "Skip"],
            }
        ]
    return Room(
        id=str(entry["id"]),
        title=str(entry.get("title") or entry["id"]),
        summary=str(entry.get("summary") or ""),
        xp_reward=int(entry.get("xp_reward", 10)),
        unlock_xp=int(entry.get("unlock_xp", 0)),
        lesson_md=str(entry.get("lesson_md") or entry.get("summary") or "Pack stub."),
        story_md=str(entry.get("story_md") or ""),
        concept_md=str(entry.get("concept_md") or ""),
        tasks=_load_tasks(tasks_raw),
        path=path_hint,
        resources=_load_resources(entry.get("resources")),
        shared=bool(entry.get("shared", False)),
        course=str(entry.get("course") or COURSE_SYSTEMS),
        boss=bool(entry.get("boss", False)),
    )


def load_systems_from_pack() -> list[Track]:
    """FLAG-lab player stub: load ~/.mage/packs/systems.json if present."""
    pack = packs_dir() / "systems.json"
    rooms: list[Room] = []
    if pack.exists():
        try:
            data = json.loads(pack.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {}
        for entry in data.get("rooms") or []:
            if isinstance(entry, dict) and entry.get("id"):
                rooms.append(_room_from_pack_entry(entry, str(pack)))

    bundled: list[Track] = []
    stub_dir = content_root() / "courses" / "systems"
    if (stub_dir / "track.yaml").exists():
        bundled = [load_track(stub_dir)]

    if not rooms and bundled:
        # still prepend shared core into bundled track
        track = bundled[0]
        shared = load_shared_rooms()
        seen = {r.id for r in track.rooms}
        track.rooms = [r for r in shared if r.id not in seen] + track.rooms
        return [track]

    if not rooms:
        rooms = [
            Room(
                id="flag-hello",
                title="FLAG lab hello",
                summary="Offline stub — run mage sync to refresh packs.",
                xp_reward=10,
                unlock_xp=0,
                lesson_md="Systems Mage pack cache is empty. Use `:sync` / `mage sync`.",
                tasks=_load_tasks(
                    [
                        {
                            "id": "ack",
                            "type": "mcq",
                            "prompt": "Acknowledge systems stub?",
                            "xp": 5,
                            "answer": 0,
                            "choices": ["Yes", "Later"],
                        }
                    ]
                ),
                path=str(pack),
                course=COURSE_SYSTEMS,
                resources=[
                    Resource(
                        title="Computer Systems: A Programmer's Perspective",
                        url="https://csapp.cs.cmu.edu/",
                        kind="book",
                    )
                ],
            )
        ]
    shared = load_shared_rooms()
    merged = {r.id: r for r in shared}
    for r in rooms:
        merged[r.id] = r
    track = Track(
        id="systems",
        title="Systems Mage",
        summary="FLAG-lab / systems catalog (pack-backed).",
        order=1,
        unlock_xp=0,
        icon="⚙",
        rooms=list(merged.values()),
        path=str(pack.parent),
        course=COURSE_SYSTEMS,
    )
    return [track]


def load_fundamentals_tracks() -> list[Track]:
    base = content_root() / "courses" / "fundamentals"
    tracks: list[Track] = []
    if base.exists() and (base / "track.yaml").exists():
        tracks.append(load_track(base))
    else:
        # assemble from shared + clear room if layout is rooms-only
        rooms = load_shared_rooms()
        clear_dir = content_root() / "courses" / "fundamentals" / "rooms" / "fundamentals-clear"
        if (clear_dir / "room.yaml").exists():
            rooms = rooms + [load_room(clear_dir)]
        if rooms:
            tracks.append(
                Track(
                    id="fundamentals",
                    title="Fundamentals",
                    summary="Path to Mago base.",
                    order=1,
                    unlock_xp=0,
                    icon="◇",
                    rooms=rooms,
                    path=str(base),
                    course=COURSE_FUNDAMENTALS,
                )
            )
    return tracks


def load_tracks_for_course(course_id: str, root: Path | None = None) -> list[Track]:
    if course_id == COURSE_EDGE:
        tracks = load_all_tracks(root)
        for t in tracks:
            if not t.course:
                t.course = COURSE_EDGE
        return tracks
    if course_id == COURSE_SYSTEMS:
        return load_systems_from_pack()
    if course_id == COURSE_FUNDAMENTALS:
        return load_fundamentals_tracks()
    return load_all_tracks(root)


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
