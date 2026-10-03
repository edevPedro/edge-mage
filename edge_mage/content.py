"""Carrega trilhas YAML + lições Markdown + cursos (fundamentals/systems/edge/neurotech)."""

from __future__ import annotations

from pathlib import Path

import yaml

from edge_mage.courses import (
    COURSE_EDGE,
    COURSE_FUNDAMENTALS,
    COURSE_NEUROTECH,
    COURSE_SYSTEMS,
)
from edge_mage.models import Resource, Room, Task, Track

# Track folder ids that belong to the parallel Neurotech course (not Edge).
_NEUROTECH_TRACK_IDS = frozenset({"neurotech"})


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
                answer_pattern=str(raw.get("answer_pattern") or ""),
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


def _as_str_list(raw) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        return [raw]
    return [str(x) for x in raw]


def load_room(room_dir: Path) -> Room:
    meta_path = room_dir / "room.yaml"
    meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    lesson = _read_md(room_dir / "lesson.md")
    story = _read_md(room_dir / "story.md", str(meta.get("story") or ""))
    concept = _read_md(room_dir / "concept.md", str(meta.get("concept") or ""))
    # Fallback order from NN- folder prefix when yaml omits `order`.
    folder_order = 99
    name = room_dir.name
    if len(name) >= 2 and name[:2].isdigit():
        folder_order = int(name[:2])
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
        requires_skills=_as_str_list(meta.get("requires_skills")),
        requires_rooms=_as_str_list(meta.get("requires_rooms")),
        requires_rooms_any=_as_str_list(meta.get("requires_rooms_any")),
        order=int(meta.get("order", folder_order)),
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
    rooms.sort(key=lambda r: (r.order, r.id))
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


def load_all_tracks(root: Path | None = None, *, exclude_neurotech: bool = True) -> list[Track]:
    """Edge course: content/tracks (current TUI content). Neurotech is a sibling course."""
    base = root or content_root()
    tracks_dir = base / "tracks"
    tracks: list[Track] = []
    if not tracks_dir.exists():
        return tracks
    for track_dir in sorted(p for p in tracks_dir.iterdir() if p.is_dir()):
        if not (track_dir / "track.yaml").exists():
            continue
        track = load_track(track_dir)
        if exclude_neurotech and (
            track.id in _NEUROTECH_TRACK_IDS or track.course == COURSE_NEUROTECH
        ):
            continue
        tracks.append(track)
    tracks.sort(key=lambda t: t.order)
    return tracks


def load_neurotech_tracks(root: Path | None = None) -> list[Track]:
    """Parallel Neurotech circle: content/tracks/10-neurotech (and any course=neurotech)."""
    base = root or content_root()
    tracks_dir = base / "tracks"
    tracks: list[Track] = []
    if not tracks_dir.exists():
        return tracks
    for track_dir in sorted(p for p in tracks_dir.iterdir() if p.is_dir()):
        if not (track_dir / "track.yaml").exists():
            continue
        track = load_track(track_dir)
        if track.id in _NEUROTECH_TRACK_IDS or track.course == COURSE_NEUROTECH:
            track.course = COURSE_NEUROTECH
            tracks.append(track)
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


def _bundled_craft_rooms() -> list[Room]:
    """Keep Edge richness: boss-craft + shared-math-evidence (not flag-hello)."""
    rooms: list[Room] = []
    craft_ids = ("boss-craft", "shared-math-evidence")
    base = content_root() / "courses" / "systems" / "rooms"
    for name in craft_ids:
        room_dir = base / name
        if (room_dir / "room.yaml").exists():
            rooms.append(load_room(room_dir))
    return rooms


def load_systems_from_pack() -> list[Track]:
    """
    Systems Mage FLAG catalog: bundled / ~/.mage/packs/systems.json
    (systems + llvm + math), plus craft YAML rooms and shared core credit.
    """
    from edge_mage.packs import TRACK_META, load_systems_pack_data

    data, pack_path = load_systems_pack_data()
    entries = list(data.get("rooms") or [])
    by_track: dict[str, list[Room]] = {"systems": [], "llvm": [], "math": []}

    for entry in entries:
        if not isinstance(entry, dict) or not entry.get("id"):
            continue
        # Skip thin stub when real catalog is present
        if entry.get("id") == "flag-hello" and len(entries) > 3:
            continue
        track_id = str(entry.get("track") or "systems")
        if track_id not in by_track:
            by_track[track_id] = []
        by_track[track_id].append(_room_from_pack_entry(entry, str(pack_path)))

    for rooms in by_track.values():
        rooms.sort(key=lambda r: (r.unlock_xp, r.id))

    # Prefer pack order field when present
    for track_id, rooms in list(by_track.items()):
        keyed: list[tuple[int, Room]] = []
        for i, room in enumerate(rooms):
            order = i
            # recover order from matching entry
            for entry in entries:
                if isinstance(entry, dict) and entry.get("id") == room.id:
                    order = int(entry.get("order", i))
                    break
            keyed.append((order, room))
        keyed.sort(key=lambda x: x[0])
        by_track[track_id] = [r for _, r in keyed]

    craft = _bundled_craft_rooms()
    shared = load_shared_rooms()

    tracks: list[Track] = []
    for track_id in ("systems", "llvm", "math"):
        rooms = by_track.get(track_id) or []
        if track_id == "systems":
            # Shared core once at the front of systems phase
            seen = {r.id for r in rooms}
            rooms = [r for r in shared if r.id not in seen] + rooms
        if not rooms:
            continue
        meta = TRACK_META.get(track_id, {})
        tracks.append(
            Track(
                id=track_id,
                title=str(meta.get("title") or track_id),
                summary=str(meta.get("summary") or ""),
                order=int(meta.get("order", 99)),
                unlock_xp=0,
                icon=str(meta.get("icon") or "◆"),
                rooms=rooms,
                path=str(pack_path),
                course=COURSE_SYSTEMS,
            )
        )

    if craft:
        meta = TRACK_META["craft"]
        tracks.append(
            Track(
                id="craft",
                title=str(meta["title"]),
                summary=str(meta["summary"]),
                order=int(meta["order"]),
                unlock_xp=0,
                icon=str(meta["icon"]),
                rooms=craft,
                path=str(content_root() / "courses" / "systems"),
                course=COURSE_SYSTEMS,
            )
        )

    if tracks:
        return tracks

    # Absolute last resort: YAML stub track (flag-hello era)
    stub_dir = content_root() / "courses" / "systems"
    if (stub_dir / "track.yaml").exists():
        track = load_track(stub_dir)
        seen = {r.id for r in track.rooms}
        track.rooms = [r for r in shared if r.id not in seen] + track.rooms
        return [track]

    return [
        Track(
            id="systems",
            title="Systems Mage",
            summary="Offline stub — run mage sync / reinstall for full pack.",
            order=1,
            unlock_xp=0,
            icon="⚙",
            rooms=shared
            or [
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
                    path=str(pack_path),
                    course=COURSE_SYSTEMS,
                )
            ],
            path=str(pack_path),
            course=COURSE_SYSTEMS,
        )
    ]


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
        tracks = load_all_tracks(root, exclude_neurotech=True)
        for t in tracks:
            if not t.course:
                t.course = COURSE_EDGE
        return tracks
    if course_id == COURSE_NEUROTECH:
        return load_neurotech_tracks(root)
    if course_id == COURSE_SYSTEMS:
        return load_systems_from_pack()
    if course_id == COURSE_FUNDAMENTALS:
        return load_fundamentals_tracks()
    return load_all_tracks(root, exclude_neurotech=True)


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
