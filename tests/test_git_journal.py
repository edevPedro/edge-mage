"""Testes do diário git (sem rede)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from edge_mage.git_journal import (
    JournalSettings,
    append_ledger_entry,
    completion_in_ledger,
    format_commit_message,
    journal_task_completion,
    sync_study_journal,
    task_label,
)


def _init_repo(path: Path) -> None:
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@edge-mage.local"],
        cwd=path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Edge Mage Test"],
        cwd=path,
        check=True,
        capture_output=True,
    )
    (path / "README.md").write_text("# test\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=path,
        check=True,
        capture_output=True,
    )


def test_task_label_truncates() -> None:
    long_prompt = "x" * 100
    assert len(task_label("id", long_prompt)) == 72
    assert task_label("tid", "") == "tid"


def test_format_commit_message() -> None:
    msg = format_commit_message("fundamentos", "trigonometria", "rad-90", "Quantos radianos?")
    assert msg == "study: concluiu fundamentos/trigonometria — Quantos radianos?"


def test_append_ledger_and_dedup(tmp_path: Path) -> None:
    append_ledger_entry(
        tmp_path,
        track_id="t",
        room_id="r",
        task_id="a",
        xp_awarded=10,
        timestamp="2026-01-01T00:00:00+00:00",
    )
    ledger = tmp_path / "study-log/completions.jsonl"
    assert ledger.is_file()
    row = json.loads(ledger.read_text(encoding="utf-8").strip())
    assert row["xp_awarded"] == 10
    assert completion_in_ledger(ledger, "t", "r", "a")
    append_ledger_entry(
        tmp_path,
        track_id="t",
        room_id="r",
        task_id="a",
        xp_awarded=99,
    )
    lines = [ln for ln in ledger.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 1


def test_journal_commits_ledger(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    settings = JournalSettings(auto_git_commit=True, auto_git_push=False)
    jr = journal_task_completion(
        track_id="fundamentos",
        room_id="trigonometria",
        task_id="rad-90",
        task_prompt="Quantos radianos?",
        xp_awarded=21,
        repo_root=tmp_path,
        settings=settings,
    )
    assert jr.ok
    assert jr.committed
    assert not jr.pushed
    assert "study: concluiu" in jr.message
    log = subprocess.run(
        ["git", "log", "-1", "--format=%s"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )
    assert log.stdout.strip() == jr.message


def test_journal_idempotent_second_call(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    settings = JournalSettings(auto_git_commit=True, auto_git_push=False)
    kwargs = dict(
        track_id="fundamentos",
        room_id="trigonometria",
        task_id="rad-90",
        task_prompt="Quantos radianos?",
        xp_awarded=21,
        repo_root=tmp_path,
        settings=settings,
    )
    journal_task_completion(**kwargs)
    jr2 = journal_task_completion(**kwargs)
    assert jr2.ok
    assert not jr2.committed
    assert "já registrada" in jr2.message


def test_sync_commits_uncommitted_ledger(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    append_ledger_entry(
        tmp_path,
        track_id="t",
        room_id="r",
        task_id="x",
        xp_awarded=5,
    )
    settings = JournalSettings(auto_git_commit=True, auto_git_push=False)
    jr = sync_study_journal(repo_root=tmp_path, settings=settings)
    assert jr.ok
    assert jr.committed
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )
    assert status.stdout.strip() == ""
