"""Ranks: global e-mage path + Edge ML + Neurotech course-internal ranks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Rank:
    id: str
    title: str
    title_en: str
    min_xp: int
    min_level: int
    blurb: str


# --- Neurotech parallel circle (rune + boss gated; never Edge ladder) --------
NEURO_RUNE_ACQ = "rune-neuro-acq"
NEURO_RUNE_DECODE = "rune-neuro-decode"
NEURO_RUNE_ONLINE = "rune-neuro-online"
NEURO_RUNE_IDS: tuple[str, ...] = (
    NEURO_RUNE_ACQ,
    NEURO_RUNE_DECODE,
    NEURO_RUNE_ONLINE,
)

# Room clears that materialize inventory runes (parallel circle).
NEURO_RUNE_DROP_ROOMS: dict[str, str] = {
    "nt-filter-bank": NEURO_RUNE_ACQ,
    "nt-decode-mvp": NEURO_RUNE_DECODE,
    "nt-online-stub": NEURO_RUNE_ONLINE,
}

# Alternate acq path: full F2 electrode chain without filter-bank yet.
NEURO_ACQ_CHAIN: tuple[str, ...] = (
    "nt-electrode-snr",
    "nt-ground-ref",
    "nt-adc-bio",
)

NEURO_MILESTONE_ROOMS: frozenset[str] = frozenset(
    {
        "nt-filter-bank",
        "nt-decode-mvp",
        "nt-online-stub",
        "nt-neuro-mage",
    }
)

NEURO_RUNE_META: dict[str, tuple[str, str]] = {
    NEURO_RUNE_ACQ: ("◈", "Aquisição"),
    NEURO_RUNE_DECODE: ("λ", "Decode"),
    NEURO_RUNE_ONLINE: ("↺", "Online"),
}

NEURO_RANKS: tuple[Rank, ...] = (
    Rank(
        "neuro_novice",
        "Novice",
        "Novice",
        0,
        1,
        "Portal do círculo Neural — Estuda → Sala.",
    ),
    Rank(
        "signal_adept",
        "Signal Adept",
        "Signal Adept",
        1,
        2,
        "Cadeia de aquisição / filter-bank — rune-neuro-acq.",
    ),
    Rank(
        "decode_adept",
        "Decode Adept",
        "Decode Adept",
        2,
        3,
        "Decode MVP offline (LDA→κ) — rune-neuro-decode.",
    ),
    Rank(
        "closed_loop_adept",
        "Closed-Loop Adept",
        "Closed-Loop Adept",
        3,
        4,
        "Loop online stub — rune-neuro-online.",
    ),
    Rank(
        "neuro_mage",
        "Neuro Mage",
        "Neuro Mage",
        4,
        5,
        "3 runas neuro + boss ritual — círculo paralelo (≠ Mago Supremo).",
    ),
)


def neuro_runes_earned_from_rooms(completed_room_ids: Iterable[str]) -> set[str]:
    """Derive which neuro runes rooms should grant (idempotent inventory)."""
    done = {str(r) for r in completed_room_ids}
    earned: set[str] = set()
    if "nt-filter-bank" in done or set(NEURO_ACQ_CHAIN).issubset(done):
        earned.add(NEURO_RUNE_ACQ)
    if "nt-decode-mvp" in done:
        earned.add(NEURO_RUNE_DECODE)
    if "nt-online-stub" in done:
        earned.add(NEURO_RUNE_ONLINE)
    return earned


def effective_neuro_rank(
    owned_runes: Iterable[str],
    *,
    has_neuro_mage_boss: bool,
) -> Rank:
    """
    Neurotech course ranks — rune ladder + boss for Neuro Mage.
    Does not use Edge XP / on-device ritual.
    """
    runes = {str(r) for r in owned_runes}
    has_acq = NEURO_RUNE_ACQ in runes
    has_decode = NEURO_RUNE_DECODE in runes
    has_online = NEURO_RUNE_ONLINE in runes
    if has_acq and has_decode and has_online and has_neuro_mage_boss:
        return next(r for r in NEURO_RANKS if r.id == "neuro_mage")
    if has_online:
        return next(r for r in NEURO_RANKS if r.id == "closed_loop_adept")
    if has_decode:
        return next(r for r in NEURO_RANKS if r.id == "decode_adept")
    if has_acq:
        return next(r for r in NEURO_RANKS if r.id == "signal_adept")
    return NEURO_RANKS[0]


def next_neuro_rank(current: Rank) -> Rank | None:
    for i, rank in enumerate(NEURO_RANKS):
        if rank.id == current.id and i + 1 < len(NEURO_RANKS):
            return NEURO_RANKS[i + 1]
    return None


# --- Edge ML Mage course (internal feeling; preserved from Edge Mage) --------
EDGE_RANKS: tuple[Rank, ...] = (
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
        "Checklist on-device (ritual) + XP ≥2900 — competência embarcada real.",
    ),
)

# Back-compat alias used across the Edge course UI
RANKS = EDGE_RANKS

# --- Global e-mage path (cross-course) ---------------------------------------
# none → Mago base (fundamentals clear) → intermediate → Mago Supremo (evidence)
GLOBAL_RANKS: tuple[Rank, ...] = (
    Rank(
        "none",
        "Sem rank",
        "Unranked",
        0,
        1,
        "Comece por Fundamentals para conquistar Mago base.",
    ),
    Rank(
        "mago_base",
        "Mago base",
        "Base Mage",
        0,
        1,
        "Fundamentals concluído — Systems e Edge liberados (soft gate).",
    ),
    Rank(
        "intermediate",
        "Intermediário",
        "Intermediate",
        0,
        1,
        "Progresso em Systems e/ou Edge — ainda sem evidência completa.",
    ),
    Rank(
        "mago_supremo",
        "Mago Supremo",
        "Supreme Mage",
        0,
        1,
        "Mago Supremo: Systems LLVM craft + Edge on-device + shared math evidence.",
    ),
)


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
    """Edge-course rank from XP alone (ignores on-device ritual)."""
    current = EDGE_RANKS[0]
    for rank in EDGE_RANKS:
        if xp >= rank.min_xp:
            current = rank
        else:
            break
    return current


def effective_rank(xp: int, has_on_device_ritual: bool) -> Rank:
    """
    Edge-course ranks: intermediários = XP.
    Edge Mage exige ritual on-device além do XP floor (2900).
    """
    by_xp = rank_from_xp(xp)
    if by_xp.id != "edge_mage":
        return by_xp
    if has_on_device_ritual:
        return by_xp
    return next(r for r in EDGE_RANKS if r.id == "arquimago")


def next_rank(xp: int) -> Rank | None:
    current = rank_from_xp(xp)
    for i, rank in enumerate(EDGE_RANKS):
        if rank.id == current.id and i + 1 < len(EDGE_RANKS):
            return EDGE_RANKS[i + 1]
    return None


def global_rank_from_flags(
    *,
    has_mago_base: bool,
    has_systems_boss: bool = False,
    has_edge_on_device: bool = False,
    has_evidence: bool = False,
    any_advanced_progress: bool = False,
) -> Rank:
    """
    Global path:
      none → Mago base → intermediate → Mago Supremo
    Mago Supremo gated by systems boss craft + edge on-device + evidence.
    """
    if has_mago_base and has_systems_boss and has_edge_on_device and has_evidence:
        return next(r for r in GLOBAL_RANKS if r.id == "mago_supremo")
    if has_mago_base and (any_advanced_progress or has_systems_boss or has_edge_on_device):
        return next(r for r in GLOBAL_RANKS if r.id == "intermediate")
    if has_mago_base:
        return next(r for r in GLOBAL_RANKS if r.id == "mago_base")
    return next(r for r in GLOBAL_RANKS if r.id == "none")


def next_global_rank(current_id: str) -> Rank | None:
    for i, rank in enumerate(GLOBAL_RANKS):
        if rank.id == current_id and i + 1 < len(GLOBAL_RANKS):
            return GLOBAL_RANKS[i + 1]
    return None


def format_level_table() -> str:
    lines = ["Nível | XP mín. | Rank típico (Edge)", "------|---------|--------------------"]
    for i, thr in enumerate(LEVEL_THRESHOLDS):
        lvl = i + 1
        rank = rank_from_xp(thr)
        lines.append(f"{lvl:5d} | {thr:7d} | {rank.title}")
    return "\n".join(lines)
