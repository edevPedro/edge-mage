"""Diário de estudo versionado: uma conclusão de task → commit no git."""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from edge_mage.paths import config_path

LEDGER_PATH = Path("study-log/completions.jsonl")
CONFIG_PATH = config_path()


@dataclass(frozen=True)
class JournalSettings:
    auto_git_commit: bool = True
    auto_git_push: bool = True


@dataclass(frozen=True)
class JournalResult:
    ok: bool
    committed: bool = False
    pushed: bool = False
    message: str = ""
    warning: str = ""


def load_journal_settings(repo_root: Path | None) -> JournalSettings:
    raw: dict[str, Any] = {}
    if CONFIG_PATH.is_file():
        try:
            raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            raw = {}
    commit_flag = raw.get("auto_git_commit")
    push_flag = raw.get("auto_git_push")
    auto_commit = bool(commit_flag) if commit_flag is not None else repo_root is not None
    auto_push = bool(push_flag) if push_flag is not None else False
    if push_flag is None and repo_root is not None:
        auto_push = _has_origin(repo_root)
    return JournalSettings(auto_git_commit=auto_commit, auto_git_push=auto_push)


def find_repo_root() -> Path | None:
    seen: set[Path] = set()
    candidates: list[Path] = []
    env_root = os.environ.get("EDGE_MAGE_REPO_ROOT")
    if env_root:
        candidates.append(Path(env_root))
    candidates.append(Path.cwd())
    pkg = Path(__file__).resolve().parent
    candidates.extend(list(pkg.parents))
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        if (resolved / ".git").is_dir():
            return resolved
    return None


def task_label(task_id: str, prompt: str) -> str:
    line = (prompt or "").strip().split("\n")[0].strip()
    if not line:
        return task_id
    if len(line) > 72:
        return line[:69] + "..."
    return line


def format_commit_message(
    track_id: str,
    room_id: str,
    task_id: str,
    prompt: str,
) -> str:
    label = task_label(task_id, prompt)
    return f"study: concluiu {track_id}/{room_id} — {label}"


def completion_in_ledger(ledger_file: Path, track_id: str, room_id: str, task_id: str) -> bool:
    if not ledger_file.is_file():
        return False
    for line in ledger_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if (
            row.get("track_id") == track_id
            and row.get("room_id") == room_id
            and row.get("task_id") == task_id
        ):
            return True
    return False


def append_ledger_entry(
    repo_root: Path,
    *,
    track_id: str,
    room_id: str,
    task_id: str,
    xp_awarded: int,
    timestamp: str | None = None,
) -> Path:
    ledger_file = repo_root / LEDGER_PATH
    ledger_file.parent.mkdir(parents=True, exist_ok=True)
    if not ledger_file.exists():
        ledger_file.write_text("", encoding="utf-8")
    if completion_in_ledger(ledger_file, track_id, room_id, task_id):
        return ledger_file
    ts = timestamp or datetime.now(timezone.utc).isoformat()
    row = {
        "timestamp": ts,
        "track_id": track_id,
        "room_id": room_id,
        "task_id": task_id,
        "xp_awarded": xp_awarded,
    }
    with ledger_file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return ledger_file


def _run_git(
    args: list[str],
    cwd: Path,
    *,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=check,
    )


def _has_origin(repo_root: Path) -> bool:
    proc = _run_git(["remote", "get-url", "origin"], repo_root)
    return proc.returncode == 0 and bool(proc.stdout.strip())


def journal_task_completion(
    *,
    track_id: str,
    room_id: str,
    task_id: str,
    task_prompt: str,
    xp_awarded: int,
    repo_root: Path | None = None,
    settings: JournalSettings | None = None,
    run_git=_run_git,
) -> JournalResult:
    """Registra conclusão no ledger e opcionalmente commit/push."""
    root = repo_root or find_repo_root()
    if root is None:
        return JournalResult(
            ok=False,
            warning="git: repositório não encontrado (defina EDGE_MAGE_REPO_ROOT)",
        )
    cfg = settings or load_journal_settings(root)
    if not cfg.auto_git_commit:
        return JournalResult(ok=True, message="auto_git_commit desligado")

    ledger_rel = str(LEDGER_PATH)
    ledger_file = root / LEDGER_PATH
    if completion_in_ledger(ledger_file, track_id, room_id, task_id):
        return JournalResult(ok=True, message="task já registrada no diário")

    append_ledger_entry(
        root,
        track_id=track_id,
        room_id=room_id,
        task_id=task_id,
        xp_awarded=xp_awarded,
    )

    add_proc = run_git(["add", "--", ledger_rel], root)
    if add_proc.returncode != 0:
        return JournalResult(
            ok=False,
            warning=f"git add falhou: {(add_proc.stderr or add_proc.stdout).strip()}",
        )

    diff = run_git(["diff", "--cached", "--quiet", "--", ledger_rel], root)
    if diff.returncode == 0:
        return JournalResult(ok=True, message="ledger já commitado para esta task")

    msg = format_commit_message(track_id, room_id, task_id, task_prompt)
    commit_proc = run_git(["commit", "-m", msg], root)
    if commit_proc.returncode != 0:
        err = (commit_proc.stderr or commit_proc.stdout).strip()
        return JournalResult(
            ok=False,
            committed=False,
            warning=f"git commit falhou: {err}",
        )

    pushed = False
    if cfg.auto_git_push:
        push_proc = run_git(["push", "-u", "origin", "HEAD"], root)
        if push_proc.returncode != 0:
            err = (push_proc.stderr or push_proc.stdout).strip()
            return JournalResult(
                ok=True,
                committed=True,
                pushed=False,
                message=msg,
                warning=f"git push falhou: {err} (use :sync)",
            )
        pushed = True

    return JournalResult(ok=True, committed=True, pushed=pushed, message=msg)


def journal_artifact(
    ritual_id: str,
    *,
    repo_root: Path | None = None,
    settings: JournalSettings | None = None,
    run_git=_run_git,
) -> JournalResult:
    """Commita study-log/artifacts/<ritual>.md no diário git."""
    root = repo_root or find_repo_root()
    if root is None:
        return JournalResult(
            ok=False,
            warning="git: repositório não encontrado",
        )
    cfg = settings or load_journal_settings(root)
    if not cfg.auto_git_commit:
        return JournalResult(ok=True, message="auto_git_commit desligado")

    safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in ritual_id)
    rel = f"study-log/artifacts/{safe}.md"
    path = root / rel
    if not path.is_file():
        return JournalResult(ok=False, warning=f"artefato ausente: {rel}")

    add_proc = run_git(["add", "--", rel], root)
    if add_proc.returncode != 0:
        return JournalResult(
            ok=False,
            warning=f"git add falhou: {(add_proc.stderr or add_proc.stdout).strip()}",
        )

    diff = run_git(["diff", "--cached", "--quiet", "--", rel], root)
    if diff.returncode == 0:
        return JournalResult(ok=True, message="artefato já commitado")

    msg = f"study: ritual {ritual_id} — artifact"
    commit_proc = run_git(["commit", "-m", msg], root)
    if commit_proc.returncode != 0:
        err = (commit_proc.stderr or commit_proc.stdout).strip()
        return JournalResult(ok=False, warning=f"git commit falhou: {err}")

    pushed = False
    if cfg.auto_git_push:
        push_proc = run_git(["push", "-u", "origin", "HEAD"], root)
        if push_proc.returncode != 0:
            err = (push_proc.stderr or push_proc.stdout).strip()
            return JournalResult(
                ok=True,
                committed=True,
                message=msg,
                warning=f"git push falhou: {err} (use :sync)",
            )
        pushed = True
    return JournalResult(ok=True, committed=True, pushed=pushed, message=msg)


def sync_study_journal(
    repo_root: Path | None = None,
    settings: JournalSettings | None = None,
    run_git=_run_git,
) -> JournalResult:
    """Commita ledger + artifacts pendentes e faz push."""
    root = repo_root or find_repo_root()
    if root is None:
        return JournalResult(
            ok=False,
            warning="git: repositório não encontrado",
        )
    cfg = settings or load_journal_settings(root)
    ledger_rel = str(LEDGER_PATH)
    arts = "study-log/artifacts"
    ledger_file = root / LEDGER_PATH
    arts_path = root / arts
    if not ledger_file.is_file() and not arts_path.exists():
        return JournalResult(ok=True, message="nenhum ledger ainda")

    paths = [ledger_rel]
    if arts_path.exists():
        paths.append(arts)
    add_proc = run_git(["add", "--", *paths], root)
    if add_proc.returncode != 0:
        return JournalResult(
            ok=False,
            warning=f"git add falhou: {(add_proc.stderr or add_proc.stdout).strip()}",
        )

    diff = run_git(["diff", "--cached", "--quiet"], root)
    if diff.returncode != 0:
        msg = "study: sync completions + artifacts"
        commit_proc = run_git(["commit", "-m", msg], root)
        if commit_proc.returncode != 0:
            err = (commit_proc.stderr or commit_proc.stdout).strip()
            return JournalResult(ok=False, warning=f"git commit falhou: {err}")

    if not cfg.auto_git_push:
        return JournalResult(ok=True, committed=True, message="commit local (push desligado)")

    push_proc = run_git(["push", "-u", "origin", "HEAD"], root)
    if push_proc.returncode != 0:
        err = (push_proc.stderr or push_proc.stdout).strip()
        return JournalResult(ok=False, warning=f"git push falhou: {err}")
    return JournalResult(ok=True, committed=True, pushed=True, message="sync ok")
