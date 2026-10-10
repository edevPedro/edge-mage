"""Ciclo de vida dos ramos (§3/§5/§8).

Um ramo abre por evidência (desafio do tronco concluído) OU calendário (semana
do programa), o que vier primeiro. Regras: no máximo `max_active_branches` ramos
ativos; o tronco deve manter ≥ `trunk_min_pct` da atenção; sem evidência PASS no
tronco por `stagnation_weeks` semanas → aviso de estagnação.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta

from edge_mage.roadmap import daily as daily_mod
from edge_mage.roadmap.models import Branch, Roadmap


def _start_date(started_at: str) -> date | None:
    if not started_at:
        return None
    try:
        return datetime.fromisoformat(started_at).date()
    except ValueError:
        return None


def program_week(roadmap: Roadmap, state, *, today: date | None = None) -> int:
    d = today or date.today()
    start = _start_date(state.started_at)
    if start is None:
        return 1
    return max(1, (d - start).days // 7 + 1)


def challenge_done(roadmap: Roadmap, state, challenge_id: str) -> bool:
    ch = roadmap.challenge(challenge_id)
    if ch is None:
        return False
    return len(daily_mod.done_goals(state, challenge_id)) >= len(ch.daily_goals)


@dataclass
class BranchStatus:
    branch: Branch
    open: bool
    active: bool
    reason: str
    share_pct: float = 0.0


def branch_is_open(branch: Branch, roadmap: Roadmap, state, *, today: date | None = None) -> tuple[bool, str]:
    ow = branch.opens_when
    if ow.week is None and ow.challenge is None:
        return True, "manual"
    week = program_week(roadmap, state, today=today)
    if ow.week is not None and week >= ow.week:
        return True, f"semana {week} ≥ {ow.week}"
    if ow.challenge and challenge_done(roadmap, state, ow.challenge):
        return True, f"{ow.challenge} concluído"
    return False, f"abre em {ow.describe()}"


def statuses(roadmap: Roadmap, state, *, today: date | None = None) -> list[BranchStatus]:
    out: list[BranchStatus] = []
    for b in roadmap.branches:
        is_open, reason = branch_is_open(b, roadmap, state, today=today)
        active = (b.id in state.branches_active) and is_open
        out.append(BranchStatus(b, is_open, active, reason))
    return out


def activate(roadmap: Roadmap, state, branch_id: str, *, today: date | None = None) -> tuple[bool, str]:
    b = roadmap.branch(branch_id)
    if b is None:
        return False, f"ramo '{branch_id}' não existe"
    is_open, reason = branch_is_open(b, roadmap, state, today=today)
    if not is_open:
        return False, f"ramo '{branch_id}' ainda não abre ({reason})"
    if branch_id in state.branches_active:
        return True, "já ativo"
    if len(state.branches_active) >= roadmap.rules.max_active_branches:
        return False, f"máximo de {roadmap.rules.max_active_branches} ramos ativos — feche um antes (§3)"
    state.branches_active.append(branch_id)
    return True, f"ramo '{branch_id}' ativado"


def deactivate(state, branch_id: str) -> bool:
    if branch_id in state.branches_active:
        state.branches_active.remove(branch_id)
        return True
    return False


def trunk_share(records: list, roadmap: Roadmap, *, days: int = 7, today: date | None = None) -> tuple[float, int, int]:
    """% de evidências PASS no tronco na janela. Retorna (pct, tronco_n, total_n)."""
    d = today or date.today()
    cutoff = d - timedelta(days=days)
    trunk_ids = set(roadmap.trunk_order)
    trunk_n = total_n = 0
    for r in records:
        if not getattr(r, "is_pass", False) or not r.timestamp:
            continue
        try:
            rd = datetime.fromisoformat(r.timestamp).date()
        except ValueError:
            continue
        if rd < cutoff:
            continue
        total_n += 1
        if r.challenge_id in trunk_ids:
            trunk_n += 1
    pct = 100.0 * trunk_n / total_n if total_n else 100.0
    return pct, trunk_n, total_n


def stagnation_warning(roadmap: Roadmap, state, records: list, *, today: date | None = None) -> str | None:
    d = today or date.today()
    limit = timedelta(weeks=roadmap.rules.stagnation_weeks)
    trunk_ids = set(roadmap.trunk_order)
    latest: date | None = None
    for r in records:
        if not getattr(r, "is_pass", False) or not r.timestamp or r.challenge_id not in trunk_ids:
            continue
        try:
            rd = datetime.fromisoformat(r.timestamp).date()
        except ValueError:
            continue
        if latest is None or rd > latest:
            latest = rd
    if latest is None:
        start = _start_date(state.started_at)
        if start is not None and (d - start) > limit:
            return (f"tronco sem nenhuma evidência PASS há {(d-start).days} dias — "
                    f"reabra o tronco (§5).")
        return None
    if (d - latest) > limit:
        return (f"tronco estagnado: última evidência PASS há {(d-latest).days} dias "
                f"(>{roadmap.rules.stagnation_weeks} semanas) — reabra o tronco (§5).")
    return None
