"""Systems Mage offline pack: bundled snapshot + ~/.mage/packs cache."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from edge_mage.paths import packs_dir

# Minimum FLAG rooms from systems+llvm+math (seed catalog). Boss YAML rooms extra.
MIN_SYSTEMS_FLAG_ROOMS = 70

TRACK_META: dict[str, dict[str, Any]] = {
    "systems": {
        "title": "Systems · Círculo da Máquina",
        "summary": "Memória → ABI/ELF/asm — portal antes do LLVM.",
        "order": 1,
        "icon": "⚙",
    },
    "llvm": {
        "title": "LLVM · Círculo do IR",
        "summary": "Toolchain → IR/passes → AArch64 → DIY/RE.",
        "order": 2,
        "icon": "◈",
    },
    "math": {
        "title": "Math bridge",
        "summary": "Vetores → gradiente → prob — prep for Edge.",
        "order": 3,
        "icon": "∑",
    },
    "craft": {
        "title": "Systems craft",
        "summary": "Boss rituals — systems-boss-craft + shared math evidence.",
        "order": 4,
        "icon": "⚔",
    },
}


def _package_content_root() -> Path:
    here = Path(__file__).resolve().parent.parent / "content"
    if here.exists():
        return here
    return Path.cwd() / "content"


def bundled_systems_pack_path() -> Path:
    return _package_content_root() / "packs" / "systems.json"


def user_systems_pack_path() -> Path:
    return packs_dir() / "systems.json"


def seed_systems_pack(*, force: bool = False) -> Path | None:
    """
    Copy bundled Systems Mage pack into ~/.mage/packs/systems.json.
    Returns destination path when seeded (or already present), else None.
    """
    src = bundled_systems_pack_path()
    if not src.exists():
        return None
    dest = user_systems_pack_path()
    if dest.exists() and not force:
        try:
            data = json.loads(dest.read_text(encoding="utf-8"))
            rooms = _extract_rooms(data)
            if len(rooms) >= MIN_SYSTEMS_FLAG_ROOMS:
                return dest
            # Thin stub / old cache — refresh from bundle
        except (json.JSONDecodeError, OSError, TypeError):
            pass
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return dest


def _extract_rooms(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Accept flat pack, systemsMagePack wrapper, or catalog API envelope."""
    if not isinstance(data, dict):
        return []

    # Direct pack or nested systemsMagePack (catalog GET)
    for key in ("rooms",):
        rooms = data.get(key)
        if isinstance(rooms, list) and rooms:
            return [r for r in rooms if isinstance(r, dict) and r.get("id")]

    nested = data.get("systemsMagePack")
    if isinstance(nested, dict):
        rooms = nested.get("rooms")
        if isinstance(rooms, list) and rooms:
            return [r for r in rooms if isinstance(r, dict) and r.get("id")]

    # Flatten systems.phases[].rooms (metadata-only — may lack tasks)
    systems = data.get("systems")
    if isinstance(systems, dict):
        phases = systems.get("phases")
        if isinstance(phases, list):
            out: list[dict[str, Any]] = []
            for phase in phases:
                if not isinstance(phase, dict):
                    continue
                track_id = str(phase.get("trackId") or phase.get("id") or "systems")
                for room in phase.get("rooms") or []:
                    if isinstance(room, dict) and room.get("id"):
                        entry = dict(room)
                        entry.setdefault("track", track_id)
                        out.append(entry)
            if out:
                return out
    return []


def load_systems_pack_data() -> tuple[dict[str, Any], Path]:
    """
    Load best available Systems pack (user cache, else bundled).
    Seeds user cache from bundle when missing/thin.
    """
    seed_systems_pack(force=False)
    candidates = [user_systems_pack_path(), bundled_systems_pack_path()]
    for path in candidates:
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        rooms = _extract_rooms(data)
        if rooms:
            # Prefer nested pack metadata when present
            if isinstance(data.get("systemsMagePack"), dict):
                return data["systemsMagePack"], path
            if data.get("rooms"):
                return data, path
            return {"rooms": rooms, "course": "systems", "version": 1}, path
    return {"rooms": [], "course": "systems", "version": 1, "stub": True}, user_systems_pack_path()


def write_systems_pack(data: dict[str, Any]) -> Path:
    """Normalize catalog/API payload and write ~/.mage/packs/systems.json."""
    dest = user_systems_pack_path()
    if isinstance(data.get("systemsMagePack"), dict):
        payload = data["systemsMagePack"]
    elif isinstance(data.get("rooms"), list):
        payload = data
    else:
        rooms = _extract_rooms(data)
        payload = {
            "version": data.get("version", 1),
            "course": "systems",
            "title": "Systems Mage",
            "generatedAt": data.get("generatedAt"),
            "rooms": rooms,
            "roomCount": len(rooms),
            "source": "catalog-normalized",
        }
    dest.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return dest


def pack_room_count(data: dict[str, Any] | None = None) -> int:
    if data is None:
        data, _ = load_systems_pack_data()
    return len(_extract_rooms(data))
