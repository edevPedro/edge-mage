#!/usr/bin/env python3
"""Lint de conteúdo: resources, salas de teoria curtas, prova verificável, segredos.

Regras (Fase 2/4):
- toda room.yaml tem ≥1 resource {title,url,kind};
- sala de teoria (não-boss) tem lesson.md curta (≤120 linhas / ≤9000 chars);
- sala tem ≥1 prova verificável (não somente MCQ de múltipla escolha);
- nenhum vazamento de segredo (chave privada, token de nuvem, api_key longa).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

VERIFIABLE_TYPES = {"numeric", "fill", "code", "c_code", "ritual"}
MAX_THEORY_LINES = 120
MAX_THEORY_CHARS = 9000

_SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(
        r"(?i)\b(api[_-]?key|secret|password|access[_-]?token)\b\s*[:=]\s*"
        r"['\"]?[A-Za-z0-9_\-/+=]{16,}"
    ),
)


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


def _check_resources(meta: dict) -> bool:
    resources = meta.get("resources") or []
    if not (isinstance(resources, list) and len(resources) >= 1):
        return False
    for r in resources:
        if not isinstance(r, dict) or not r.get("title") or not r.get("url"):
            return False
    return True


def _scannable_text(room_yaml: Path, meta: dict) -> str:
    parts = [room_yaml.read_text(encoding="utf-8")]
    for name in ("lesson.md", "concept.md", "story.md"):
        p = room_yaml.parent / name
        if p.is_file():
            parts.append(p.read_text(encoding="utf-8"))
    return "\n".join(parts)


def main() -> int:
    missing_resources: list[str] = []
    too_long: list[str] = []
    mcq_only: list[str] = []
    secrets: list[str] = []
    empty_lesson: list[str] = []

    for path in room_files():
        rel = str(path.relative_to(ROOT))
        meta = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

        if not _check_resources(meta):
            missing_resources.append(rel)

        is_boss = bool(meta.get("boss", False))
        lesson = path.parent / "lesson.md"
        if not lesson.is_file() or not lesson.read_text(encoding="utf-8").strip():
            empty_lesson.append(rel)
        elif not is_boss:
            text = lesson.read_text(encoding="utf-8")
            if text.count("\n") + 1 > MAX_THEORY_LINES or len(text) > MAX_THEORY_CHARS:
                too_long.append(rel)

        tasks = [t for t in (meta.get("tasks") or []) if isinstance(t, dict)]
        types = {str(t.get("type") or "") for t in tasks}
        if tasks and not (types & VERIFIABLE_TYPES) and not meta.get("mcq_only_ok"):
            mcq_only.append(rel)

        blob = _scannable_text(path, meta)
        for pat in _SECRET_PATTERNS:
            if pat.search(blob):
                secrets.append(f"{rel} → {pat.pattern}")
                break

    failed = False
    if missing_resources:
        failed = True
        print("Rooms missing resources (≥1 {title,url,kind}):", file=sys.stderr)
        for m in missing_resources:
            print(f"  - {m}", file=sys.stderr)
    if empty_lesson:
        failed = True
        print("Rooms sem lesson.md:", file=sys.stderr)
        for m in empty_lesson:
            print(f"  - {m}", file=sys.stderr)
    if too_long:
        failed = True
        print(
            f"Salas de teoria longas (>{MAX_THEORY_LINES} linhas / {MAX_THEORY_CHARS} chars):",
            file=sys.stderr,
        )
        for m in too_long:
            print(f"  - {m}", file=sys.stderr)
    if mcq_only:
        failed = True
        print(
            "Salas só-MCQ (adicione numeric/fill/code/ritual ou marque mcq_only_ok):",
            file=sys.stderr,
        )
        for m in mcq_only:
            print(f"  - {m}", file=sys.stderr)
    if secrets:
        failed = True
        print("Possível segredo/dado sensível no conteúdo:", file=sys.stderr)
        for m in secrets:
            print(f"  - {m}", file=sys.stderr)

    if failed:
        return 1
    print(
        f"OK: {len(room_files())} rooms — resources, teoria curta, prova verificável, sem segredos"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
