"""Testes do runner de código (Fase 4): PASS, FAIL, timeout, compilação, ruído.

Cobre o sandbox Python e (quando há compilador) o sandbox C.
"""

from __future__ import annotations

import shutil

import pytest

from edge_mage.models import Task
from edge_mage.validators import MAX_OUTPUT_CHARS, validate_task

HAS_C_COMPILER = shutil.which("clang") is not None or shutil.which("gcc") is not None


def _code_task(**kw) -> Task:
    base = dict(id="runner", type="code", prompt="runner")
    base.update(kw)
    return Task(**base)


# --- PASS -------------------------------------------------------------------


def test_runner_pass_expected_stdout() -> None:
    task = _code_task(expected_stdout="42")
    ok, msg = validate_task(task, "print(6 * 7)\n")
    assert ok is True, msg


def test_runner_pass_harness() -> None:
    task = _code_task(
        code_tests=(
            "assert mod.add(2, 3) == 5\n"
            "assert mod.add(-1, 1) == 0\n"
            "print('OK')\n"
        )
    )
    ok, msg = validate_task(task, "def add(a, b):\n    return a + b\n")
    assert ok is True, msg


# --- FAIL -------------------------------------------------------------------


def test_runner_fail_harness_assertion() -> None:
    task = _code_task(
        code_tests="assert mod.square(3) == 9\nprint('OK')\n"
    )
    ok, msg = validate_task(task, "def square(x):\n    return x + 1\n")
    assert ok is False
    assert msg


def test_runner_fail_wrong_stdout() -> None:
    task = _code_task(expected_stdout="42")
    ok, msg = validate_task(task, "print(41)\n")
    assert ok is False
    assert "Stdout esperado" in msg or "esperado" in msg.lower()


# --- timeout ----------------------------------------------------------------


def test_runner_timeout_python() -> None:
    task = _code_task(prompt="loop infinito")
    ok, msg = validate_task(task, "while True:\n    pass\n")
    assert ok is False
    assert "Timeout" in msg


# --- compilação quebrada ----------------------------------------------------


def test_runner_broken_python_syntax() -> None:
    task = _code_task(prompt="sintaxe quebrada")
    ok, msg = validate_task(task, "def broken(:\n    return 1\n")
    assert ok is False
    assert "Execução falhou" in msg or "falhou" in msg.lower()


@pytest.mark.skipif(not HAS_C_COMPILER, reason="C compiler (clang/gcc) não disponível")
def test_runner_broken_c_compile() -> None:
    task = _code_task(type="code", language="c", prompt="C quebrado")
    ok, msg = validate_task(task, "int main() { this is not C ;;; }")
    assert ok is False
    assert "compilação" in msg.lower() or "Erro de compilação C" in msg


# --- ruído alto -------------------------------------------------------------


def test_runner_high_noise_python() -> None:
    task = _code_task(prompt="saída ruidosa")
    noisy = "for i in range(500):\n    print('x' * 200)\n"
    ok, msg = validate_task(task, noisy)
    assert ok is False
    assert "ruído" in msg or "excessiva" in msg
    assert MAX_OUTPUT_CHARS == 20_000


@pytest.mark.skipif(not HAS_C_COMPILER, reason="C compiler (clang/gcc) não disponível")
def test_runner_high_noise_c() -> None:
    task = _code_task(type="code", language="c", prompt="C ruidoso")
    noisy = (
        "int main(void) {\n"
        "    for (int i = 0; i < 500; i++) {\n"
        "        for (int j = 0; j < 200; j++) putchar('y');\n"
        "        putchar('\\n');\n"
        "    }\n"
        "    return 0;\n"
        "}\n"
    )
    ok, msg = validate_task(task, noisy)
    assert ok is False
    assert "ruído" in msg or "excessiva" in msg
