#!/usr/bin/env python3
"""Benchmark smoke do runner (Fase 4) — roda em CI Linux.

Exercita o sandbox de código (PASS, FAIL, timeout, ruído alto) e falha se algum
caso estourar o orçamento de tempo ou se comportar diferente do esperado.
"""

from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from edge_mage.models import Task  # noqa: E402
from edge_mage.validators import validate_task  # noqa: E402

HAS_C_COMPILER = shutil.which("clang") is not None or shutil.which("gcc") is not None


def _task(**kw) -> Task:
    base = dict(id="bench", type="code", prompt="bench")
    base.update(kw)
    return Task(**base)


def _time(fn) -> tuple[float, bool, str]:
    start = time.perf_counter()
    ok, msg = fn()
    return time.perf_counter() - start, ok, msg


def main() -> int:
    cases: list[tuple[str, object, bool, float, float]] = []

    pass_task = _task(expected_stdout="42")
    cases.append(
        ("PASS", lambda: validate_task(pass_task, "print(6*7)\n"), True, 0.0, 2.0)
    )

    fail_task = _task(code_tests="assert mod.f(2) == 4\nprint('OK')\n")
    cases.append(
        ("FAIL", lambda: validate_task(fail_task, "def f(x):\n    return x\n"), False, 0.0, 2.0)
    )

    timeout_task = _task()
    cases.append(
        ("TIMEOUT", lambda: validate_task(timeout_task, "while True:\n    pass\n"), False, 0.0, 6.0)
    )

    noise_task = _task()
    cases.append(
        (
            "NOISE",
            lambda: validate_task(noise_task, "for i in range(500):\n    print('x'*200)\n"),
            False,
            0.0,
            6.0,
        )
    )

    if HAS_C_COMPILER:
        c_task = _task(type="code", language="c", expected_stdout="42")
        cases.append(
            (
                "C-PASS",
                lambda: validate_task(c_task, "int main(void){printf(\"42\\n\");return 0;}\n"),
                True,
                0.0,
                5.0,
            )
        )

    print(f"{'case':<10} {'ok':<6} {'elapsed':>8} {'budget':>8}  verdict")
    failures: list[str] = []
    for name, fn, expect_ok, _lo, budget in cases:
        elapsed, ok, msg = _time(fn)  # type: ignore[arg-type]
        within = elapsed <= budget
        verdict = "ok" if (ok == expect_ok and within) else "FAIL"
        if verdict == "FAIL":
            failures.append(f"{name}: ok={ok} elapsed={elapsed:.2f}s -> {msg[:80]}")
        print(f"{name:<10} {str(ok):<6} {elapsed:>7.2f}s {budget:>7.2f}s  {verdict}")

    if failures:
        print("\nBenchmark smoke FAILED:", file=sys.stderr)
        for line in failures:
            print(f"  - {line}", file=sys.stderr)
        return 1
    print("\nBenchmark smoke OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
