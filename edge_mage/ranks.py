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


# Progressão: noviço em trig → Edge Mage
RANKS: tuple[Rank, ...] = (
    Rank(
        "novico",
        "Noviço",
        "Novice",
        0,
        1,
        "Primeiros passos: ângulos, razões trigonométricas.",
    ),
    Rank(
        "aprendiz",
        "Aprendiz",
        "Apprentice",
        80,
        2,
        "Vetores e bases do cálculo espacial.",
    ),
    Rank(
        "adepto",
        "Adepto",
        "Adept",
        220,
        4,
        "Álgebra linear e física de sinais.",
    ),
    Rank(
        "evocador",
        "Evocador",
        "Evoker",
        450,
        6,
        "Elétrica edge e transforms em robótica.",
    ),
    Rank(
        "mago",
        "Mago",
        "Mage",
        800,
        9,
        "Otimização e intuição de loss/gradiente.",
    ),
    Rank(
        "arquimago",
        "Arquimago",
        "Archmage",
        1300,
        12,
        "ML math: softmax, matmul, quantização.",
    ),
    Rank(
        "edge_mage",
        "Edge Mage",
        "Edge Mage",
        2000,
        16,
        "Inferência on-device, latência e layout de tensores.",
    ),
)

# XP por nível (nível N requer LEVEL_XP[N-1] XP acumulado)
LEVEL_THRESHOLDS: tuple[int, ...] = (
    0,  # L1
    40,  # L2
    80,  # L3
    140,  # L4
    220,  # L5
    320,  # L6
    450,  # L7
    600,  # L8
    800,  # L9
    1000,  # L10
    1150,  # L11
    1300,  # L12
    1500,  # L13
    1700,  # L14
    1850,  # L15
    2000,  # L16 Edge Mage floor
    2300,  # L17
    2600,  # L18
    3000,  # L19
    3500,  # L20
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
