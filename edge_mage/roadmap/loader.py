"""Carrega roadmap/*.yaml e challenges/<id>/challenge.yaml."""

from __future__ import annotations

from pathlib import Path

import yaml

from edge_mage.paths import challenges_dir, roadmap_dir
from edge_mage.roadmap.errors import (
    ChallengeNotFound,
    RoadmapNotFound,
    RoadmapSpecError,
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

ROADMAP_FILE = "roadmap.yaml"
BRANCHES_FILE = "branches.yaml"
CHALLENGE_FILE = "challenge.yaml"


def _read_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:  # pragma: no cover - mensagem clara
        raise RoadmapSpecError(f"{path}: YAML inválido: {exc}") from exc
    if not isinstance(raw, dict):
        raise RoadmapSpecError(f"{path}: esperado um mapa YAML")
    return raw


def _as_list(raw) -> list:
    if raw is None:
        return []
    if isinstance(raw, list):
        return raw
    return [raw]


def _source(raw: dict) -> Source:
    return Source(
        name=str(raw.get("name") or "?"),
        url=str(raw.get("url") or ""),
        section=str(raw.get("section") or ""),
        why=str(raw.get("why") or ""),
    )


def _goal(raw: dict) -> DailyGoal:
    lens = raw.get("lens")
    return DailyGoal(
        id=str(raw.get("id") or ""),
        goal=str(raw.get("goal") or ""),
        verify=str(raw.get("verify") or ""),
        lens=str(lens) if lens else None,
    )


def _open_when(raw: dict | None) -> OpenWhen:
    raw = raw or {}
    week = raw.get("week")
    challenge = raw.get("challenge")
    return OpenWhen(
        week=int(week) if week is not None else None,
        challenge=str(challenge) if challenge else None,
    )


def _branch(raw: dict) -> Branch:
    return Branch(
        id=str(raw.get("id") or ""),
        title=str(raw.get("title") or raw.get("id") or ""),
        opens_when=_open_when(raw.get("opens_when")),
        weekly_cap_pct=float(raw.get("weekly_cap_pct", 10)),
        content=str(raw.get("content") or ""),
    )


def load_challenge(challenge_id: str, *, root: Path | None = None) -> Challenge:
    base = root or challenges_dir()
    cdir = base / challenge_id
    path = cdir / CHALLENGE_FILE
    if not path.exists():
        raise ChallengeNotFound(
            f"desafio '{challenge_id}' não encontrado ({path})"
        )
    raw = _read_yaml(path)
    goals_raw = [g for g in _as_list(raw.get("daily_goals")) if isinstance(g, dict)]
    goals = [g for g in (_goal(g) for g in goals_raw) if g.id]
    verify_raw = raw.get("verify") or {}
    if not isinstance(verify_raw, dict):
        raise RoadmapSpecError(f"{path}: campo verify deve ser um mapa")
    exit_raw = raw.get("exit_criteria") or {}
    artifact_raw = raw.get("artifact") or {}
    lens = raw.get("lens")
    return Challenge(
        id=str(raw.get("id") or challenge_id),
        track=str(raw.get("track") or "?"),
        title=str(raw.get("title") or challenge_id),
        dir=cdir,
        summary=str(raw.get("summary") or ""),
        timebox_days=int(raw.get("timebox_days", 21)),
        work_dir=str(raw.get("work_dir") or ""),
        exit_criteria=ExitCriteria(
            metric=str(exit_raw.get("metric") or ""),
            target=str(exit_raw.get("target") or ""),
        ),
        sources=[s for s in (_source(s) for s in _as_list(raw.get("sources")) if isinstance(s, dict))],
        daily_goals=goals,
        lens=str(lens) if lens else None,
        verify=VerifyConfig(
            cmd=str(verify_raw.get("cmd") or ""),
            timeout_s=float(verify_raw.get("timeout_s", 120)),
            runs=int(verify_raw.get("runs", 3)),
            noise_cv=float(verify_raw.get("noise_cv", 0.15)),
        ),
        readme_sections=[str(s) for s in _as_list(artifact_raw.get("readme_sections"))],
    )


def available_challenges(*, root: Path | None = None) -> list[str]:
    base = root or challenges_dir()
    if not base.exists():
        return []
    out: list[str] = []
    for d in sorted(p for p in base.iterdir() if p.is_dir()):
        if (d / CHALLENGE_FILE).exists():
            out.append(d.name)
    return out


def load_roadmap(*, root: Path | None = None, challenges_root: Path | None = None) -> Roadmap:
    base = root or roadmap_dir()
    if not base.exists():
        raise RoadmapNotFound(f"roadmap/ não encontrado em {base}")
    cfg = _read_yaml(base / ROADMAP_FILE)
    rules_raw = cfg.get("rules") or {}
    rules = RoadmapRules(
        trunk_min_pct=float(rules_raw.get("trunk_min_pct", 65)),
        branches_max_pct=float(rules_raw.get("branches_max_pct", 35)),
        max_active_branches=int(rules_raw.get("max_active_branches", 2)),
        stagnation_weeks=int(rules_raw.get("stagnation_weeks", 2)),
        dispersion_alert_pct=float(rules_raw.get("dispersion_alert_pct", 10)),
        rollover_max=int(rules_raw.get("rollover_max", 1)),
    )
    branches_raw = cfg.get("branches")
    if branches_raw is None:
        branches_raw = _read_yaml(base / BRANCHES_FILE).get("branches")
    branches = [b for b in (_branch(b) for b in _as_list(branches_raw) if isinstance(b, dict)) if b.id]

    trunk_order = [str(x) for x in _as_list(cfg.get("trunk_order"))]
    challenges: dict[str, Challenge] = {}
    ch_root = challenges_root or challenges_dir()
    for cid in trunk_order:
        try:
            challenges[cid] = load_challenge(cid, root=ch_root)
        except ChallengeNotFound:
            continue

    return Roadmap(
        version=int(cfg.get("version", 1)),
        daily_minutes=int(cfg.get("daily_minutes", 60)),
        weekend_review=bool(cfg.get("weekend_review", True)),
        trunk_track=str(cfg.get("trunk_track") or "A"),
        trunk_order=trunk_order,
        rules=rules,
        branches=branches,
        challenges=challenges,
    )
