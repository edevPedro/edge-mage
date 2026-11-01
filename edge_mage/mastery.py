"""Minimal viable mastery / remediation hooks (not fake ML adaptivity).

Maps failure themes → Estuda room ids so quiz/spell misses point back to teaching.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Remediation:
    theme: str
    room_ids: tuple[str, ...]
    note: str


# Theme keys can come from task ids, room pillars, or validator hints.
REMEDIATION: tuple[Remediation, ...] = (
    Remediation(
        "cache",
        ("pf-cache-vm", "pf-pipeline"),
        "Revisit cache/VM/TLB Estuda before retrying counters or tiling spells.",
    ),
    Remediation(
        "neon",
        ("pf-neon-intro", "pf-simd-tiling"),
        "NEON load/store + tiling before ARM Math boss.",
    ),
    Remediation(
        "roofline",
        ("pf-roofline", "pf-nla-ieee"),
        "Classify memory-bound vs compute-bound with a Roofline sketch.",
    ),
    Remediation(
        "metal",
        ("pf-metal-intro", "pf-gpu-kernels"),
        "Metal memory model ≠ CUDA; re-read Metal intro before kernel boss.",
    ),
    Remediation(
        "quant",
        ("quantizacao", "softmax-ce", "export-runtime"),
        "PTQ/QAT literacy + stable softmax before on-device ritual.",
    ),
    Remediation(
        "abi",
        ("pf-aarch64-perf", "aarch64-abi", "intro-asm"),
        "AAPCS64 / frames before CMSIS or syscall-flavored labs.",
    ),
    Remediation(
        "m4",
        ("pf-portal",),
        "M4: no SVE; µarch ≠ Cortex-A; Metal ≠ CUDA.",
    ),
)


def remediation_for(theme: str) -> Remediation | None:
    key = (theme or "").strip().lower()
    if not key:
        return None
    for item in REMEDIATION:
        if item.theme == key or key in item.theme:
            return item
    for item in REMEDIATION:
        if any(key in rid for rid in item.room_ids):
            return item
    return None


def remediation_blurb(theme: str) -> str:
    hit = remediation_for(theme)
    if not hit:
        return (
            "Releia o Estuda da sala atual (Conceito) e retente o Spell; "
            "bosses exigem golden + medida, não só XP."
        )
    rooms = ", ".join(hit.room_ids)
    return f"Remediação ({hit.theme}): {hit.note} Salas: {rooms}."
