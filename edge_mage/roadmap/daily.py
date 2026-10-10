"""Meta diária (§2): menor passo com verificador, rolagem e fechamento com explicação.

Estado em ~/.mage/daily.json. O streak é derivado do evidence log (fonte de
verdade): um dia só conta se tiver ao menos uma execução PASS registrada.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from edge_mage.paths import daily_path
from edge_mage.roadmap import evidence as evidence_mod
from edge_mage.roadmap.models import Challenge, DailyGoal, Roadmap, Source

STATE_SCHEMA = 1


@dataclass
class GoalContext:
    challenge: Challenge
    goal: DailyGoal
    source: Source | None
    rollovers: int = 0
    needs_breakup: bool = False
    already_passed: bool = False


@dataclass
class DailyState:
    schema_version: int = STATE_SCHEMA
    active_challenge: str = ""
    started_at: str = ""
    goals: dict = field(default_factory=dict)  # challenge -> goal -> {rollovers, last_shown, status}
    days: dict = field(default_factory=dict)   # iso date -> {status, goal_id, challenge_id, ...}
    branches_active: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "active_challenge": self.active_challenge,
            "started_at": self.started_at,
            "goals": self.goals,
            "days": self.days,
            "branches_active": self.branches_active,
        }

    @classmethod
    def from_dict(cls, raw: dict) -> "DailyState":
        data = raw if isinstance(raw, dict) else {}
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in data.items() if k in known})


def load_state(path: Path | None = None) -> DailyState:
    p = path or daily_path()
    if not p.exists():
        return DailyState()
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return DailyState()
    return DailyState.from_dict(raw)


def save_state(state: DailyState, path: Path | None = None) -> Path:
    p = path or daily_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return p


def _goal_state(state: DailyState, challenge_id: str, goal_id: str) -> dict:
    ch = state.goals.setdefault(challenge_id, {})
    return ch.setdefault(goal_id, {"rollovers": 0, "last_shown": "", "status": "todo"})


def passed_goals(records: list, challenge_id: str) -> set[str]:
    """Metas com ao menos uma evidência PASS (podem ainda não ter sido fechadas)."""
    return {r.goal_id for r in records if r.challenge_id == challenge_id and r.is_pass}


def done_goals(state: DailyState, challenge_id: str) -> set[str]:
    """Metas concluídas = verificadas E fechadas com explicação (§2/§7)."""
    ch = state.goals.get(challenge_id, {})
    return {gid for gid, gs in ch.items() if gs.get("status") == "done"}


def pick_active_challenge(roadmap: Roadmap, state: DailyState, records: list = None) -> Challenge | None:
    if state.active_challenge:
        ch = roadmap.challenge(state.active_challenge)
        if ch is not None:
            if len(done_goals(state, ch.id)) >= len(ch.daily_goals):
                state.active_challenge = ""
            else:
                return ch
    for ch in roadmap.trunk_challenges():
        if len(done_goals(state, ch.id)) < len(ch.daily_goals):
            state.active_challenge = ch.id
            if not state.started_at:
                state.started_at = datetime.now(timezone.utc).isoformat()
            return ch
    return None


def next_goal(challenge: Challenge, state: DailyState) -> DailyGoal | None:
    done = done_goals(state, challenge.id)
    for g in challenge.daily_goals:
        if g.id not in done:
            return g
    return None


def _pending_close_goal(challenge: Challenge, state: DailyState, records: list, today: date) -> str | None:
    """Meta verificada hoje e ainda não fechada (pronta para `mage close`)."""
    relevant = [r for r in records if r.challenge_id == challenge.id and r.is_pass and r.timestamp]
    if not relevant:
        return None
    latest = max(relevant, key=lambda r: r.timestamp)
    try:
        rd = datetime.fromisoformat(latest.timestamp).date()
    except ValueError:
        return None
    if rd != today:
        return None
    if latest.goal_id in done_goals(state, challenge.id):
        return None
    return latest.goal_id


def today_context(
    roadmap: Roadmap,
    state: DailyState,
    records: list,
    *,
    today: date | None = None,
) -> GoalContext | None:
    """Seleciona a meta de hoje, aplicando rolagem (quebra após rollover_max)."""
    d = today or date.today()
    ch = pick_active_challenge(roadmap, state, records)
    if ch is None:
        return None
    pending = _pending_close_goal(ch, state, records, d)
    goal = ch.goal(pending) if pending else None
    if goal is None:
        goal = next_goal(ch, state)
    if goal is None:
        return None
    gs = _goal_state(state, ch.id, goal.id)
    last = gs.get("last_shown") or ""
    iso = d.isoformat()
    if pending is None and last and last != iso and gs.get("status") != "done":
        gs["rollovers"] = int(gs.get("rollovers", 0)) + 1
    gs["last_shown"] = iso
    rollovers = int(gs.get("rollovers", 0))
    sources = ch.sources
    source = None
    if sources:
        goals_ids = [g.id for g in ch.daily_goals]
        idx = goals_ids.index(goal.id) if goal.id in goals_ids else 0
        source = sources[idx % len(sources)]
    return GoalContext(
        challenge=ch,
        goal=goal,
        source=source,
        rollovers=rollovers,
        needs_breakup=pending is None and rollovers > roadmap.rules.rollover_max,
        already_passed=goal.id in passed_goals(records, ch.id),
    )


def mark_goal_done(state: DailyState, challenge_id: str, goal_id: str) -> None:
    gs = _goal_state(state, challenge_id, goal_id)
    gs["status"] = "done"


def close_day(
    state: DailyState,
    *,
    challenge_id: str,
    goal_id: str,
    explanation: str,
    evidence_path: str = "",
    day: date | None = None,
) -> dict:
    d = (day or date.today()).isoformat()
    mark_goal_done(state, challenge_id, goal_id)
    entry = {
        "status": "closed",
        "challenge_id": challenge_id,
        "goal_id": goal_id,
        "explanation": explanation,
        "evidence": evidence_path,
        "closed_at": datetime.now(timezone.utc).isoformat(),
    }
    state.days[d] = entry
    return entry


def day_closed(state: DailyState, day: date | None = None) -> bool:
    d = (day or date.today()).isoformat()
    return state.days.get(d, {}).get("status") == "closed"


def days_with_evidence(records: list) -> set[str]:
    out: set[str] = set()
    for r in records:
        if not r.is_pass or not r.timestamp:
            continue
        try:
            ts = datetime.fromisoformat(r.timestamp)
        except ValueError:
            continue
        out.add(ts.date().isoformat())
    return out


def streak(records: list, *, today: date | None = None) -> int:
    """Dias consecutivos com evidência PASS, terminando hoje ou ontem (§2)."""
    days = days_with_evidence(records)
    if not days:
        return 0
    d = today or date.today()
    # permite começar de ontem se hoje ainda não tem evidência
    cursor = d if d.isoformat() in days else d - timedelta(days=1)
    count = 0
    while cursor.isoformat() in days:
        count += 1
        cursor -= timedelta(days=1)
    return count
