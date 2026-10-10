"""Testes do motor de verificação de labs (Fase 1): PASS/FAIL/timeout/build/ruído."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from edge_mage.labs import aggregate_runs, run_lab
from edge_mage.labs.bench import percentile
from edge_mage.labs.spec import load_spec

REPO = Path(__file__).resolve().parents[1]

HAS_CPP = shutil.which("clang++") is not None or shutil.which("g++") is not None
needs_compiler = pytest.mark.skipif(not HAS_CPP, reason="C++ compiler unavailable")

TEST_SRC = (
    '#include "sum.hpp"\n'
    "#include <cassert>\n"
    "#include <cstdint>\n"
    "#include <cstdio>\n"
    "int main() {\n"
    "    const std::int64_t xs[] = {1, 2, 3, 4};\n"
    "    assert(mage_sum(xs, 4) == 10);\n"
    "    std::puts(\"OK\");\n"
    "    return 0;\n"
    "}\n"
)

CORRECT = (
    "#pragma once\n"
    "#include <cstddef>\n"
    "#include <cstdint>\n"
    "inline std::int64_t mage_sum(const std::int64_t* xs, std::size_t n) {\n"
    "    std::int64_t t = 0;\n"
    "    for (std::size_t i = 0; i < n; ++i) t += xs[i];\n"
    "    return t;\n"
    "}\n"
)

WRONG = (
    "#pragma once\n"
    "#include <cstddef>\n"
    "#include <cstdint>\n"
    "inline std::int64_t mage_sum(const std::int64_t*, std::size_t) { return 0; }\n"
)

BROKEN = (
    "#pragma once\n"
    "#include <cstddef>\n"
    "inline std::int64_t mage_sum(this is not valid\n"
)

INFINITE = (
    "#pragma once\n"
    "#include <cstddef>\n"
    "#include <cstdint>\n"
    "inline std::int64_t mage_sum(const std::int64_t*, std::size_t) {\n"
    "    volatile std::int64_t x = 0;\n"
    "    while (1) { ++x; }\n"
    "    return 0;\n"
    "}\n"
)


def _fixture_lab(tmp_path: Path, name: str, header: str, *, run_s: float = 10.0) -> tuple[Path, Path]:
    root = tmp_path / "labs"
    d = root / name
    (d / "src").mkdir(parents=True)
    (d / "src" / "sum.hpp").write_text(header, encoding="utf-8")
    tests = d / "tests"
    tests.mkdir()
    (tests / "test_sum.cpp").write_text(TEST_SRC, encoding="utf-8")
    (d / "spec.yaml").write_text(
        (
            f"id: {name}\n"
            "title: fixture\n"
            "std: c++20\n"
            "flags: [\"-O2\", \"-pthread\"]\n"
            "solution: []\n"
            "test_sources: [\"test_sum.cpp\"]\n"
            "bench_source: \"\"\n"
            "bench_reps: 7\n"
            "bench_warmup: 0\n"
            f"timeout:\n  build_s: 20\n  run_s: {run_s}\n"
        ),
        encoding="utf-8",
    )
    shutil.copytree(REPO / "content" / "labs" / "_common", root / "_common", dirs_exist_ok=True)
    return root, d


@pytest.fixture()
def mage_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    home = tmp_path / "mage-home"
    monkeypatch.setenv("MAGE_HOME", str(home))
    return home


# --- engine: pass/fail/build/timeout ---------------------------------------

@needs_compiler
def test_lab_pass(tmp_path: Path, mage_home: Path) -> None:
    root, _ = _fixture_lab(tmp_path, "pass-lab", CORRECT)
    work = root / "pass-lab" / "src"
    result = run_lab("pass-lab", root=root, work_dir=work, evidence_root=mage_home / "evidence")
    assert result.ok, result.message
    assert result.tests_ok
    assert result.evidence_path is not None
    assert result.evidence_path.exists()
    assert result.evidence_path.parent.name == "pass-lab"


@needs_compiler
def test_lab_test_failure(tmp_path: Path, mage_home: Path) -> None:
    root, _ = _fixture_lab(tmp_path, "fail-lab", WRONG)
    work = root / "fail-lab" / "src"
    result = run_lab("fail-lab", root=root, work_dir=work, evidence_root=mage_home / "evidence")
    assert not result.ok
    assert result.stage == "tests"


@needs_compiler
def test_lab_broken_compile(tmp_path: Path, mage_home: Path) -> None:
    root, _ = _fixture_lab(tmp_path, "broken-lab", BROKEN)
    work = root / "broken-lab" / "src"
    result = run_lab("broken-lab", root=root, work_dir=work, evidence_root=mage_home / "evidence")
    assert not result.ok
    assert result.stage == "build"


@needs_compiler
def test_lab_test_timeout(tmp_path: Path, mage_home: Path) -> None:
    root, _ = _fixture_lab(tmp_path, "hang-lab", INFINITE, run_s=2.0)
    work = root / "hang-lab" / "src"
    result = run_lab("hang-lab", root=root, work_dir=work, evidence_root=mage_home / "evidence")
    assert not result.ok
    assert result.stage == "tests"
    assert "timeout" in result.message


# --- engine: real demo lab with benchmark (metrics + evidence) --------------

@needs_compiler
def test_demo_sum_benchmark(tmp_path: Path, mage_home: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    labs_root = REPO / "content" / "labs"
    monkeypatch.setenv("MAGE_LABS_ROOT", str(labs_root))
    work = tmp_path / "work"
    work.mkdir()
    shutil.copy(labs_root / "demo-sum" / "solution" / "sum.hpp", work / "sum.hpp")
    result = run_lab("demo-sum", work_dir=work, evidence_root=mage_home / "evidence")
    assert result.ok, result.message
    assert result.tests_ok
    assert result.bench_ok
    assert "latency_ns.p50" in result.metrics
    assert result.metrics["latency_ns.p50"]["median"] > 0
    assert not result.noisy


# --- init -------------------------------------------------------------------

def test_init_lab_seeds_src(tmp_path: Path) -> None:
    from edge_mage.labs import init_lab

    root, _ = _fixture_lab(tmp_path, "init-lab", CORRECT)
    work = tmp_path / "work"
    _, copied = init_lab("init-lab", root=root, work_dir=work)
    assert (work / "sum.hpp").exists()
    assert "sum.hpp" in copied
    # idempotente
    _, again = init_lab("init-lab", root=root, work_dir=work, force=False)
    assert again == []


# --- spec / regras -----------------------------------------------------------

def test_spec_rejects_single_run(tmp_path: Path) -> None:
    root, d = _fixture_lab(tmp_path, "single-lab", CORRECT)
    spec_path = d / "spec.yaml"
    text = spec_path.read_text(encoding="utf-8").replace("bench_reps: 7", "bench_reps: 1")
    spec_path.write_text(text, encoding="utf-8")
    spec = load_spec("single-lab", root=root)
    assert spec.bench_reps == 1  # runner bloqueia no run_lab (nunca 1 execução)


# --- unit: percentis e ruído --------------------------------------------------

def test_percentile() -> None:
    values = [1.0, 2.0, 3.0, 4.0, 100.0]
    assert percentile(values, 50) == 3.0
    assert percentile(values, 100) == 100.0
    assert percentile([5.0], 50) == 5.0


def test_aggregate_no_noise() -> None:
    runs = [
        {"latency_ns": {"p50": 100.0, "p99": 110.0}},
        {"latency_ns": {"p50": 102.0, "p99": 108.0}},
        {"latency_ns": {"p50": 101.0, "p99": 112.0}},
        {"latency_ns": {"p50": 99.0, "p99": 105.0}},
        {"latency_ns": {"p50": 103.0, "p99": 115.0}},
    ]
    agg = aggregate_runs(runs, noise_cv=0.15)
    assert agg.valid_runs == 5
    assert not agg.noisy
    assert agg.metrics["latency_ns.p50"].mean == pytest.approx(101.0)


def test_aggregate_detects_noise() -> None:
    runs = [
        {"latency_ns": {"p50": 100.0}},
        {"latency_ns": {"p50": 950.0}},
        {"latency_ns": {"p50": 1200.0}},
        {"latency_ns": {"p50": 80.0}},
        {"latency_ns": {"p50": 1500.0}},
    ]
    agg = aggregate_runs(runs, noise_cv=0.35)
    assert agg.noisy
    assert "latency_ns.p50" in agg.noisy_metrics


def test_aggregate_ignores_single_run() -> None:
    agg = aggregate_runs([{"latency_ns": {"p50": 10.0}}])
    # 1 execução nunca conta (não gera métricas)
    assert agg.metrics == {}