"""Helpers de XP juice, banners ASCII e feedback animado (texto)."""

from __future__ import annotations


def xp_banner(gained: int) -> str:
    n = max(0, int(gained))
    return (
        "╔══════════════════════════╗\n"
        f"║   +{n:<5d} XP            ║\n"
        "╚══════════════════════════╝"
    )


def skill_drop_banner(glyph: str, name: str) -> str:
    g = (glyph or "✦")[:3]
    return (
        "╔══════════════════════════════════╗\n"
        f"║          {g:^8s}                ║\n"
        f"║   SKILL · {name[:22]:<22s} ║\n"
        "╚══════════════════════════════════╝"
    )


def level_up_banner(level: int) -> str:
    return (
        "╔══════════════════════════════════╗\n"
        "║         ★  LEVEL UP  ★           ║\n"
        f"║            Nível {level:<3d}              ║\n"
        "╚══════════════════════════════════╝"
    )


def rank_up_banner(title: str) -> str:
    return (
        "╔══════════════════════════════════╗\n"
        "║        ✦  NOVO RANK  ✦           ║\n"
        f"║      {title:^26s}  ║\n"
        "╚══════════════════════════════════╝"
    )


def rune_drop_banner(glyph: str, name: str) -> str:
    g = (glyph or "◈")[:3]
    return (
        "╔══════════════════════════════════╗\n"
        f"║          {g:^8s}                ║\n"
        f"║   RUNA · {name[:22]:<22s} ║\n"
        "╚══════════════════════════════════╝"
    )


def milestone_banner(label: str) -> str:
    return (
        "╔══════════════════════════════════╗\n"
        "║     ◆  MARCO DO CÍRCULO  ◆       ║\n"
        f"║      {label[:26]:^26s}  ║\n"
        "╚══════════════════════════════════╝"
    )


def xp_bar(into: int, need: int | None, width: int = 20) -> str:
    if not need:
        return "[" + "█" * width + "] CAP"
    filled = int(width * into / need) if need else 0
    filled = max(0, min(width, filled))
    return "[" + "█" * filled + "░" * (width - filled) + f"] {into}/{need}"


def combo_line(combo: int) -> str:
    if combo <= 1:
        return ""
    fire = "🔥" * min(combo, 5)
    return f"Combo diário {combo}/4 {fire}"


def numeric_near_miss(value: float, expected: float) -> str:
    delta = value - expected
    ad = abs(delta)
    if ad < 1e-12:
        return "Quase perfeito — confira arredondamento."
    if expected != 0 and ad / abs(expected) < 0.05:
        return f"Perto! Off by ~{delta:+.4g} (≈{100 * ad / abs(expected):.1f}%)."
    if ad < 1:
        return f"Off by ~{delta:+.4g}. Revise a fórmula."
    return f"Off by ~{delta:+.4g}. Ordens de grandeza: esperado ≈ {expected:g}."
