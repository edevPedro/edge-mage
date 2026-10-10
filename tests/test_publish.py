"""Testes do artefato publicável (Fase 3): ARTIFACT/ + gate de rank."""

from __future__ import annotations

import json
from pathlib import Path

from edge_mage.git_journal import LEDGER_PATH
from edge_mage.labs.evidence import write_evidence
from edge_mage.progress import ProgressStore
from edge_mage.publish import (
    PUBLISH_DIR_NAME,
    REQUIRED_SECTIONS,
    approved_published_bosses,
    cumulative_xp_by_day,
    known_bosses,
    publish_boss,
    status_report,
    validate_published_boss,
)
from edge_mage.rituals import write_artifact


def _seed_repo(tmp_path: Path) -> Path:
    (tmp_path / "study-log" / "artifacts").mkdir(parents=True)
    ledger = tmp_path / LEDGER_PATH
    rows = [
        {"timestamp": "2026-01-01T10:00:00+00:00", "track_id": "edge-ai", "room_id": "on-device", "task_id": "a", "xp_awarded": 10},
        {"timestamp": "2026-01-01T11:00:00+00:00", "track_id": "edge-ai", "room_id": "on-device", "task_id": "b", "xp_awarded": 20},
        {"timestamp": "2026-01-03T09:00:00+00:00", "track_id": "ml-math", "room_id": "quantizacao", "task_id": "c", "xp_awarded": 30},
    ]
    ledger.write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8"
    )
    write_artifact(
        "on-device",
        "\n".join(
            [
                "- latency_ms: 12.5",
                "- ram_mb: 64",
                "- model: mobilenet-int8",
                "- device: rpi5",
            ]
        ),
        repo_root=tmp_path,
    )
    return tmp_path


def test_cumulative_xp_by_day() -> None:
    entries = [
        {"timestamp": "2026-01-01T00:00:00", "xp_awarded": 10},
        {"timestamp": "2026-01-01T12:00:00", "xp_awarded": 5},
        {"timestamp": "2026-01-02T00:00:00", "xp_awarded": 7},
    ]
    assert cumulative_xp_by_day(entries) == [("2026-01-01", 15), ("2026-01-02", 22)]


def test_publish_generates_artifact(tmp_path: Path) -> None:
    repo = _seed_repo(tmp_path)
    result = publish_boss("on-device", repo_root=repo)
    assert result.ok, result.message
    out = repo / PUBLISH_DIR_NAME / "on-device"
    readme = (out / "README.md").read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        assert section in readme
    assert "█" in readme  # gráfico ASCII dos dados
    data = json.loads((out / "evidence.json").read_text(encoding="utf-8"))
    assert data["evidence_summary"]["entries"] == 3
    assert data["evidence_summary"]["total_xp"] == 60


def test_publish_requires_approved_ritual(tmp_path: Path) -> None:
    (tmp_path / "study-log" / "artifacts").mkdir(parents=True)
    result = publish_boss("on-device", repo_root=tmp_path)
    assert result.ok is False
    assert "não aprovado" in result.message
    assert result.next_steps


def test_publish_unknown_boss(tmp_path: Path) -> None:
    result = publish_boss("nao-existe", repo_root=tmp_path)
    assert result.ok is False
    assert "desconhecido" in result.message


def test_validate_and_approve(tmp_path: Path) -> None:
    repo = _seed_repo(tmp_path)
    assert validate_published_boss("on-device", repo)[0] is False
    publish_boss("on-device", repo_root=repo)
    assert validate_published_boss("on-device", repo)[0] is True
    assert "on-device" in approved_published_bosses(repo)
    report = status_report(repo)
    assert "on-device" in report


def test_rank_gate_requires_publish(tmp_path: Path) -> None:
    repo = _seed_repo(tmp_path)
    store = ProgressStore(tmp_path / "p.json", repo_root=repo)
    store.state.xp = 3000
    store.state.rituals["on-device"] = True
    store.state.courses["fundamentals"] = {"cleared": True, "mago_base": True}
    # ritual sem artefato publicado → teto
    assert store.profile_summary("edge")["rank"].id == "arquimago"
    assert store.global_rank().id == "mago_base"
    # gera artefato → destrava
    publish_boss("on-device", repo_root=repo)
    assert store.profile_summary("edge")["rank"].id == "edge_mage"
    assert store.global_rank().id == "intermediate"


# --- Fase 1 × Fase 3: boss cuja prova é um lab verificável -------------------

def _lab_record(*, status: str = "PASS") -> dict:
    return {
        "schema": 1,
        "lab_id": "lowlat-demo",
        "status": status,
        "timestamp": "2026-02-01T00:00:00+00:00",
        "code_hash": "a" * 64,
        "tests_ok": status == "PASS",
        "noisy": False,
        "noisy_metrics": [],
        "valid_runs": 7,
        "compiler": {"kind": "clang++", "path": "/usr/bin/clang++", "version": "Apple clang 21"},
        "std": "c++20",
        "flags": ["-O2", "-pthread"],
        "host": {"cpu_model": "Apple M5", "machine": "arm64", "system": "Darwin", "cores": 10, "python": "3.11"},
        "metrics": {"latency_ns.p50": {"median": 79400.0, "p50": 79400.0, "p99": 81200.0, "cv": 0.017, "samples": 7}},
        "requirements": [{"metric": "latency_ns.p50", "op": "<=", "value": 150000, "actual": 79400.0, "ok": True}],
        "requirements_ok": True,
        "detail": "",
    }


def _seed_lab_boss(tmp_path: Path) -> Path:
    lab_dir = tmp_path / "content" / "labs" / "lowlat-demo"
    lab_dir.mkdir(parents=True)
    (lab_dir / "spec.yaml").write_text(
        "id: lowlat-demo\ntitle: Demo lowlat\nboss: true\ntest_sources: [t.cpp]\n",
        encoding="utf-8",
    )
    (tmp_path / "study-log" / "artifacts").mkdir(parents=True)
    return tmp_path


def test_lab_boss_requires_evidence(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("MAGE_HOME", str(tmp_path / "mage-home"))
    repo = _seed_lab_boss(tmp_path)
    assert "lowlat-demo" in known_bosses(repo)
    result = publish_boss("lowlat-demo", repo_root=repo)
    assert result.ok is False
    assert "lab" in result.message
    assert result.next_steps


def test_lab_boss_publishes_with_evidence(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("MAGE_HOME", str(tmp_path / "mage-home"))
    repo = _seed_lab_boss(tmp_path)
    write_evidence("lowlat-demo", _lab_record(status="PASS"))

    result = publish_boss("lowlat-demo", repo_root=repo)
    assert result.ok, result.message
    out = repo / PUBLISH_DIR_NAME / "lowlat-demo"
    readme = (out / "README.md").read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        assert section in readme
    assert "Medição verificável" in readme
    assert "latency_ns.p50" in readme
    assert "mage lab run lowlat-demo" in readme
    data = json.loads((out / "evidence.json").read_text(encoding="utf-8"))
    assert data["lab_id"] == "lowlat-demo"
    assert data["lab_evidence"]["status"] == "PASS"
    assert "lowlat-demo" in approved_published_bosses(repo)


def test_lab_boss_failed_evidence_blocks(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("MAGE_HOME", str(tmp_path / "mage-home"))
    repo = _seed_lab_boss(tmp_path)
    write_evidence("lowlat-demo", _lab_record(status="FAIL"))
    result = publish_boss("lowlat-demo", repo_root=repo)
    assert result.ok is False
    assert "não aprovado" in result.message
