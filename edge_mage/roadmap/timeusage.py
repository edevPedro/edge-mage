"""Estimativa de tempo por eventos (§8).

Tempo = soma dos intervalos entre eventos consecutivos, com gap máximo de 30 min
por intervalo. Eventos: evidências, commits no work dir do desafio e commits no
próprio repo do e-mage. Commits no repo do e-mage contam como "tempo de
plataforma" (para a regra anti-dispersão dos 10%).

É uma ESTIMATIVA — sem `mage start/stop` (decisão registrada).
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

from edge_mage.paths import practice_dir, repo_root
from edge_mage.roadmap import evidence as evidence_mod

MAX_GAP = timedelta(minutes=30)


@dataclass
class TimeUsage:
    platform_minutes: float = 0.0
    challenge_minutes: float = 0.0
    events: int = 0


def _parse_iso(ts: str) -> datetime | None:
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _git_commit_times(path, start: date, end: date) -> list[datetime]:
    if path is None or not path.exists():
        return []
    since = datetime.combine(start, datetime.min.time(), tzinfo=timezone.utc).isoformat()
    until = datetime.combine(end + timedelta(days=1), datetime.min.time(), tzinfo=timezone.utc).isoformat()
    try:
        proc = subprocess.run(
            ["git", "-C", str(path), "log", f"--since={since}", f"--until={until}", "--format=%cI"],
            capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if proc.returncode != 0:
        return []
    out: list[datetime] = []
    for line in proc.stdout.splitlines():
        dt = _parse_iso(line.strip())
        if dt is not None:
            out.append(dt)
    return out


def _evidence_times(records, start: date, end: date) -> list[datetime]:
    out: list[datetime] = []
    for rec in records:
        dt = _parse_iso(rec.timestamp)
        if dt is not None and start <= dt.date() <= end:
            out.append(dt)
    return out


def weekly_time(
    start: date,
    end: date,
    *,
    roadmap=None,
    work_root=None,
    records=None,
) -> TimeUsage:
    work_root = work_root or practice_dir()
    records = records if records is not None else evidence_mod.iter_all()

    challenge_events = _evidence_times(records, start, end)
    platform_events: list[datetime] = []

    if roadmap is not None:
        for ch in roadmap.challenges.values():
            wd = ch.resolved_work_dir(work_root)
            challenge_events.extend(_git_commit_times(wd, start, end))

    platform_events.extend(_git_commit_times(repo_root(), start, end))

    tagged: list[tuple[datetime, bool]] = [(t, False) for t in challenge_events]
    tagged.extend((t, True) for t in platform_events)
    tagged.sort(key=lambda x: x[0])

    usage = TimeUsage(events=len(tagged))
    for (t0, p0), (t1, p1) in zip(tagged, tagged[1:]):
        gap = t1 - t0
        if gap < timedelta(0) or gap > MAX_GAP:
            continue
        minutes = gap.total_seconds() / 60.0
        if p0 and p1:
            usage.platform_minutes += minutes
        else:
            usage.challenge_minutes += minutes
    return usage
