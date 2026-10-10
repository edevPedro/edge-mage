"""Motor da plataforma diária: roadmap (tronco/ramos), verificação e evidência.

API pública:
    load_roadmap()            -> Roadmap
    load_challenge(id)        -> Challenge
    run_verifier(ch, goal, wd)-> VerifyOutcome
    verify_goal(ch, goal, wd) -> VerifyRun
    load_state()/save_state() -> DailyState
    today_context(...)        -> GoalContext | None
    streak(records)           -> int
"""

from __future__ import annotations

from edge_mage.roadmap.daily import (
    DailyState,
    GoalContext,
    close_day,
    day_closed,
    load_state,
    save_state,
    streak,
    today_context,
)
from edge_mage.roadmap.errors import (
    ChallengeNotFound,
    RoadmapError,
    RoadmapNotFound,
    RoadmapSpecError,
    VerifyError,
    WorkDirError,
)
from edge_mage.roadmap.evidence import (
    SCHEMA_VERSION,
    Evidence,
    iter_all,
    iter_namespace,
    read_latest,
    write,
)
from edge_mage.roadmap.loader import (
    available_challenges,
    load_challenge,
    load_roadmap,
)
from edge_mage.roadmap.models import (
    Branch,
    Challenge,
    DailyGoal,
    ExitCriteria,
    OpenWhen,
    Roadmap,
    RoadmapRules,
    Source,
    VerifyConfig,
)
from edge_mage.roadmap.runner import VerifyRun, format_outcome, verify_goal
from edge_mage.roadmap.verifier import VerifyOutcome, parse_json_stdout, run_verifier

__all__ = [
    "Branch",
    "Challenge",
    "ChallengeNotFound",
    "DailyGoal",
    "DailyState",
    "Evidence",
    "ExitCriteria",
    "GoalContext",
    "OpenWhen",
    "Roadmap",
    "RoadmapError",
    "RoadmapNotFound",
    "RoadmapRules",
    "RoadmapSpecError",
    "SCHEMA_VERSION",
    "Source",
    "VerifyConfig",
    "VerifyError",
    "VerifyOutcome",
    "VerifyRun",
    "WorkDirError",
    "available_challenges",
    "close_day",
    "day_closed",
    "format_outcome",
    "iter_all",
    "iter_namespace",
    "load_challenge",
    "load_roadmap",
    "load_state",
    "parse_json_stdout",
    "read_latest",
    "run_verifier",
    "save_state",
    "streak",
    "today_context",
    "verify_goal",
    "write",
]
