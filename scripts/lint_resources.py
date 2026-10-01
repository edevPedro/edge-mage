#!/usr/bin/env python3
"""Fail if any room.yaml lacks ≥1 resource entry."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"


def room_files() -> list[Path]:
    files: list[Path] = []
    for path in CONTENT.rglob("room.yaml"):
        # skip broken symlinks
        if path.is_file() or path.is_symlink():
            try:
                path.resolve(strict=True)
            except FileNotFoundError:
                continue
            files.append(path)
    # de-dupe resolved paths (shared rooms via symlink)
    seen: set[Path] = set()
    unique: list[Path] = []
    for p in files:
        key = p.resolve()
        if key in seen:
            continue
        seen.add(key)
        unique.append(p)
    return sorted(unique)


def main() -> int:
    missing: list[str] = []
    for path in room_files():
        meta = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        resources = meta.get("resources") or []
        ok = isinstance(resources, list) and len(resources) >= 1
        if ok:
            for r in resources:
                if not isinstance(r, dict) or not r.get("title") or not r.get("url"):
                    ok = False
                    break
        if not ok:
            missing.append(str(path.relative_to(ROOT)))
    if missing:
        print("Rooms missing resources (≥1 {title,url,kind}):", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1
    print(f"OK: {len(room_files())} rooms have resources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
