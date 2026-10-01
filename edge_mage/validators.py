"""Validadores locais de respostas (sem rede)."""

from __future__ import annotations

import math
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from edge_mage.models import Task


def normalize_text(value: str) -> str:
    s = value.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = s.replace(",", ".")
    return s


def _resolve_mcq_answer(task: Task) -> int:
    ans = task.answer
    if isinstance(ans, int):
        if 0 <= ans < len(task.choices):
            return ans
        if 1 <= ans <= len(task.choices):
            return ans - 1
    s = str(ans).strip()
    if s.isdigit():
        n = int(s)
        if 0 <= n < len(task.choices):
            return n
        if 1 <= n <= len(task.choices):
            return n - 1
    if len(s) == 1 and s.isalpha():
        return ord(s.upper()) - ord("A")
    for i, c in enumerate(task.choices):
        if normalize_text(c) == normalize_text(s):
            return i
    return 0


def check_mcq(task: Task, user_input: str) -> tuple[bool, str]:
    raw = user_input.strip()
    if not raw:
        return False, "Escolha uma opção."

    choices = task.choices
    idx: int | None = None
    if raw.isdigit():
        idx = int(raw) - 1
    elif len(raw) == 1 and raw.isalpha():
        idx = ord(raw.upper()) - ord("A")
    else:
        for i, c in enumerate(choices):
            if normalize_text(c) == normalize_text(raw):
                idx = i
                break

    if idx is None or idx < 0 or idx >= len(choices):
        return False, "Opção inválida."

    correct_idx = _resolve_mcq_answer(task)
    if idx == correct_idx:
        return True, "Correto!"
    return False, "Ainda não. Revise o Conceito e tente de novo."


def check_numeric(task: Task, user_input: str) -> tuple[bool, str]:
    text = user_input.strip().replace(",", ".")
    try:
        value = float(text)
    except ValueError:
        return False, "Digite um número (use ponto ou vírgula)."

    expected = float(task.answer)
    abs_tol = float(task.tolerance)
    rel_tol = float(task.relative_tolerance)
    if math.isclose(value, expected, rel_tol=rel_tol, abs_tol=abs_tol):
        return True, "Correto!"
    from edge_mage.juice import numeric_near_miss

    return False, numeric_near_miss(value, expected)


def check_fill(task: Task, user_input: str) -> tuple[bool, str]:
    pattern = (task.answer_pattern or "").strip()
    if pattern:
        try:
            if re.search(pattern, user_input.strip(), flags=re.IGNORECASE):
                return True, "Correto!"
        except re.error:
            return False, "Padrão de resposta inválido no conteúdo."
        return False, "Resposta não confere com o padrão esperado."

    candidates = [normalize_text(a) for a in (task.answers or [str(task.answer)])]
    if normalize_text(user_input) in candidates:
        return True, "Correto!"
    return False, "Resposta não confere. Normalize espaços e acentos se preciso."


_FORBIDDEN = (
    "import socket",
    "import urllib",
    "import requests",
    "import subprocess",
    "import os",
    "import pathlib",
    "import shutil",
    "import ctypes",
    "open(",
    "__import__",
    "eval(",
    "exec(",
    "compile(",
    "input(",
)


def check_code(task: Task, user_code: str) -> tuple[bool, str]:
    code = user_code.strip("\n")
    if not code:
        return False, "Cole ou digite o código."

    lower = code.lower()
    for token in _FORBIDDEN:
        if token in lower:
            return False, f"Construto bloqueado por segurança: {token}"

    with tempfile.TemporaryDirectory(prefix="edge-mage-") as tmp:
        script = Path(tmp) / "solution.py"
        harness = Path(tmp) / "harness.py"

        if task.code_tests.strip():
            script.write_text(code + "\n", encoding="utf-8")
            harness_src = (
                "import importlib.util, sys\n"
                f"spec = importlib.util.spec_from_file_location('solution', r'{script}')\n"
                "mod = importlib.util.module_from_spec(spec)\n"
                "spec.loader.exec_module(mod)\n"
                + task.code_tests
                + "\nprint('OK')\n"
            )
            harness.write_text(harness_src, encoding="utf-8")
            target = harness
        else:
            script.write_text(code + "\n", encoding="utf-8")
            target = script

        try:
            proc = subprocess.run(
                [sys.executable, str(target)],
                capture_output=True,
                text=True,
                timeout=3,
                cwd=tmp,
                env={
                    "PATH": os.environ.get("PATH", ""),
                    "PYTHONPATH": "",
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "HOME": tmp,
                    "TMPDIR": tmp,
                },
            )
        except subprocess.TimeoutExpired:
            return False, "Timeout (3s). Simplifique o código."

        if proc.returncode != 0:
            err = (proc.stderr or proc.stdout or "erro").strip().splitlines()
            tip = err[-1] if err else "falhou"
            return False, f"Execução falhou: {tip}"

        out = proc.stdout.strip()
        if task.expected_stdout.strip():
            expected = task.expected_stdout.strip()
            if out == expected or out.endswith(expected):
                return True, "Feitiço OK!"
            return False, f"Stdout esperado:\n{expected}\nObtido:\n{out}"

        if task.code_tests.strip():
            if out.endswith("OK") or out == "OK":
                return True, "Testes passaram — feitiço selado!"
            return False, f"Saída inesperada:\n{out}"

        return True, "Executou sem erro."


def check_ritual(task: Task, user_input: str) -> tuple[bool, str]:
    from edge_mage.rituals import validate_ritual_file

    rid = task.ritual_id or task.id
    return validate_ritual_file(rid)


def validate_task(task: Task, user_input: str) -> tuple[bool, str]:
    if task.type == "mcq":
        return check_mcq(task, user_input)
    if task.type == "numeric":
        return check_numeric(task, user_input)
    if task.type == "fill":
        return check_fill(task, user_input)
    if task.type == "code":
        return check_code(task, user_input)
    if task.type == "ritual":
        return check_ritual(task, user_input)
    return False, f"Tipo desconhecido: {task.type}"
