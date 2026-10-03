"""Tests for real C sandbox execution and validation in edge-mage."""

from __future__ import annotations

import shutil
import pytest

from edge_mage.models import Task
from edge_mage.validators import check_c_code, validate_task

HAS_C_COMPILER = shutil.which("clang") is not None or shutil.which("gcc") is not None


@pytest.mark.skipif(not HAS_C_COMPILER, reason="C compiler (clang/gcc) not available")
def test_c_code_stdout() -> None:
    task = Task(
        id="c-hello",
        type="code",
        language="c",
        prompt="Imprima Hello BCI",
        expected_stdout="Hello BCI",
    )
    code = """
int main() {
    printf("Hello BCI\\n");
    return 0;
}
"""
    ok, msg = validate_task(task, code)
    assert ok is True
    assert "OK" in msg


@pytest.mark.skipif(not HAS_C_COMPILER, reason="C compiler (clang/gcc) not available")
def test_c_code_with_harness_asserts() -> None:
    task = Task(
        id="c-ringbuf-math",
        type="code",
        language="c",
        prompt="Implemente ringbuf_next",
        code_tests="""
int main() {
    assert(ringbuf_next(0, 16) == 1);
    assert(ringbuf_next(15, 16) == 0);
    assert(ringbuf_next(7, 16) == 8);
    printf("OK\\n");
    return 0;
}
""",
    )
    code = """
uint32_t ringbuf_next(uint32_t head, uint32_t size) {
    return (head + 1) % size;
}
"""
    ok, msg = validate_task(task, code)
    assert ok is True
    assert "passaram" in msg


@pytest.mark.skipif(not HAS_C_COMPILER, reason="C compiler (clang/gcc) not available")
def test_c_code_q15_saturation() -> None:
    task = Task(
        id="c-q15-sat",
        type="code",
        language="c",
        prompt="Implemente q15_sat",
        code_tests="""
int main() {
    assert(q15_sat(40000) == 32767);
    assert(q15_sat(-40000) == -32768);
    assert(q15_sat(100) == 100);
    printf("OK\\n");
    return 0;
}
""",
    )
    code = """
int16_t q15_sat(int32_t x) {
    if (x > 32767) return 32767;
    if (x < -32768) return -32768;
    return (int16_t)x;
}
"""
    ok, msg = validate_task(task, code)
    assert ok is True


@pytest.mark.skipif(not HAS_C_COMPILER, reason="C compiler (clang/gcc) not available")
def test_c_code_assertion_failure() -> None:
    task = Task(
        id="c-failing-assert",
        type="code",
        language="c",
        prompt="Test failing assertion",
        code_tests="""
int main() {
    assert(compute_val() == 42);
    printf("OK\\n");
    return 0;
}
""",
    )
    code = """
int compute_val() {
    return 99; // Errado!
}
"""
    ok, msg = validate_task(task, code)
    assert ok is False
    assert "falhou" in msg


@pytest.mark.skipif(not HAS_C_COMPILER, reason="C compiler (clang/gcc) not available")
def test_c_code_compilation_error() -> None:
    task = Task(
        id="c-syntax-err",
        type="code",
        language="c",
        prompt="Test compilation error",
    )
    code = "int main() { this is completely broken syntax ;;; }"
    ok, msg = validate_task(task, code)
    assert ok is False
    assert "Erro de compilação C" in msg


def test_c_code_forbidden_tokens() -> None:
    task = Task(
        id="c-security-check",
        type="code",
        language="c",
        prompt="Test forbidden token",
    )
    code = """
int main() {
    system("rm -rf /");
    return 0;
}
"""
    ok, msg = validate_task(task, code)
    assert ok is False
    assert "bloqueado por segurança" in msg


@pytest.mark.skipif(not HAS_C_COMPILER, reason="C compiler (clang/gcc) not available")
def test_c_code_timeout() -> None:
    task = Task(
        id="c-infinite-loop",
        type="code",
        language="c",
        prompt="Test infinite loop timeout",
    )
    code = """
int main() {
    volatile int x = 0;
    while (1) {
        x++;
    }
    return 0;
}
"""
    ok, msg = validate_task(task, code)
    assert ok is False
    assert "Timeout" in msg
