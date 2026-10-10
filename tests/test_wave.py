"""Testes do adaptador Wave (degrada para terminal) e widgets de bloco."""

from __future__ import annotations

from pathlib import Path

import pytest

from edge_mage import wave
from edge_mage.widgets.wave import bar_row, metric_text, sparkline


@pytest.fixture()
def fake_exec(monkeypatch: pytest.MonkeyPatch):
    calls: list[list[str]] = []

    def _exec(argv):
        calls.append(list(argv))
        return True, "ok"

    monkeypatch.setattr(wave, "_exec", _exec)
    return calls


def test_terminal_mode_when_no_wsh(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(wave, "wsh_path", lambda: None)
    assert wave.is_wave() is False
    res = wave.notify("oi", title="e-mage")
    assert res.mode == wave.TERMINAL and res.ok
    assert "oi" in res.message


def test_force_off_via_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(wave, "wsh_path", lambda: "/usr/bin/wsh")
    monkeypatch.setenv("MAGE_WAVE", "0")
    assert wave.is_wave() is False
    monkeypatch.setenv("MAGE_WAVE", "1")
    assert wave.is_wave() is True


def test_wave_mode_execs_wsh(monkeypatch: pytest.MonkeyPatch, fake_exec) -> None:
    monkeypatch.setattr(wave, "wsh_path", lambda: "/usr/bin/wsh")
    assert wave.is_wave() is True
    res = wave.run("echo hi", title="t")
    assert res.mode == wave.WAVE and res.ok
    assert fake_exec[-1][:2] == ["wsh", "run"]
    wave.notify("m", title="T")
    assert fake_exec[-1][:2] == ["wsh", "notify"]
    wave.open_url("https://example.com")
    assert fake_exec[-1] == ["wsh", "web", "open", "https://example.com"]


def test_wave_view_requires_file(monkeypatch: pytest.MonkeyPatch, fake_exec, tmp_path: Path) -> None:
    monkeypatch.setattr(wave, "wsh_path", lambda: "/usr/bin/wsh")
    missing = wave.view(tmp_path / "nope.svg")
    assert not missing.ok and "não existe" in missing.message
    f = tmp_path / "chart.svg"
    f.write_text("<svg/>", encoding="utf-8")
    ok = wave.view(f)
    assert ok.ok and ok.mode == wave.WAVE
    assert fake_exec[-1][:2] == ["wsh", "view"]


def test_terminal_run_reports_command(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(wave, "wsh_path", lambda: None)
    res = wave.run(["ls", "-la"])
    assert res.mode == wave.TERMINAL
    assert "ls -la" in res.command


def test_sparkline_and_bar() -> None:
    assert sparkline([]) == ""
    s = sparkline([1, 2, 3, 4, 5])
    assert len(s) == 5
    assert s[0] == "▁" and s[-1] == "█"
    assert bar_row(1.0, width=4) == "████"
    assert bar_row(0.0, width=4) == "░░░░"
    assert bar_row(0.5, width=4) == "██░░"


def test_metric_text() -> None:
    t = metric_text([("streak", "3d"), ("pass", "5")])
    assert "streak" in t.plain and "3d" in t.plain and "5" in t.plain
