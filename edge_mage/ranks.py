"""Tabela de ranks/níveis do Mage Academy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Rank:
    id: str
    title: str
    title_en: str
    min_xp: int
    min_level: int
    blurb: str


# Progressão: noviço em trig → Edge Mage (competência on-device real)
RANKS: tuple[Rank, ...] = (
    Rank(
        "novico",
        "Noviço",
        "Novice",
        0,
        1,
        "Ângulos, razões trigonométricas e primeiros passos.",
    ),
    Rank(
        "aprendiz",
        "Aprendiz",
        "Apprentice",
        100,
        2,
        "Vetores, exp/log e primeiros scripts Python.",
    ),
    Rank(
        "adepto",
        "Adepto",
        "Adept",
        280,
        4,
        "Álgebra linear, sinais e amostragem.",
    ),
    Rank(
        "evocador",
        "Evocador",
        "Evoker",
        550,
        6,
        "Elétrica edge, ADC e transforms em robótica.",
    ),
    Rank(
        "mago",
        "Mago",
        "Mage",
        1100,
        9,
        "Derivadas, gradiente, loss e batch.",
    ),
    Rank(
        "arquimago",
        "Arquimago",
        "Archmage",
        1750,
        12,
        "Probabilidade, softmax/CE, FLOPs e quantização.",
    ),
    Rank(
        "edge_mage",
        "Edge Mage",
        "Edge Mage",
        2900,
        17,
        "Layout, banda, SIMD e checklist on-device de ponta a ponta.",
    ),
)

# XP acumulado mínimo para cada nível (1-indexed via enumerate)
LEVEL_THRESHOLDS: tuple[int, ...] = (
    0,  # L1
    40,  # L2
    100,  # L3
    180,  # L4
    280,  # L5
    400,  # L6
    550,  # L7
    700,  # L8
    900,  # L9
    1100,  # L10
    1300,  # L11
    1500,  # L12
    1750,  # L13
    2000,  # L14
    2300,  # L15
    2500,  # L16
    2700,  # L17
    2900,  # L18 Edge Mage floor
    3100,  # L19
    3300,  # L20
)


def level_from_xp(xp: int) -> int:
    level = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if xp >= threshold:
            level = i + 1
        else:
            break
    return level


def xp_for_next_level(xp: int) -> tuple[int, int | None]:
    """Retorna (xp_atual_no_nível, xp_necessário_proximo) ou (xp, None) no cap."""
    level = level_from_xp(xp)
    current_floor = LEVEL_THRESHOLDS[level - 1]
    if level >= len(LEVEL_THRESHOLDS):
        return xp - current_floor, None
    next_floor = LEVEL_THRESHOLDS[level]
    return xp - current_floor, next_floor - current_floor


def rank_from_xp(xp: int) -> Rank:
    current = RANKS[0]
    for rank in RANKS:
        if xp >= rank.min_xp:
            current = rank
        else:
            break
    return current


def next_rank(xp: int) -> Rank | None:
    current = rank_from_xp(xp)
    for i, rank in enumerate(RANKS):
        if rank.id == current.id and i + 1 < len(RANKS):
            return RANKS[i + 1]
    return None


def format_level_table() -> str:
    lines = ["Nível | XP mín. | Rank típico", "------|---------|------------"]
    for i, thr in enumerate(LEVEL_THRESHOLDS):
        lvl = i + 1
        rank = rank_from_xp(thr)
        lines.append(f"{lvl:5d} | {thr:7d} | {rank.title}")
    return "\n".join(lines)
