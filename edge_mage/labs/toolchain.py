"""Detecção de toolchain para labs verificáveis (C++ e opcional C)."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass

from edge_mage.labs.errors import ToolchainError


@dataclass(frozen=True)
class Compiler:
    kind: str  # "clang++" | "g++"
    path: str
    version: str


_CXX_CANDIDATES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("clang++", ("clang++",)),
    ("g++", ("g++", "c++")),
)


def _version_line(path: str) -> str:
    try:
        proc = subprocess.run(
            [path, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    out = (proc.stdout or proc.stderr or "").strip()
    return out.splitlines()[0].strip() if out else ""


def find_cpp_compiler() -> Compiler:
    """Primeiro compilador C++ disponível (clang++ preferido, depois g++)."""
    for kind, names in _CXX_CANDIDATES:
        for name in names:
            path = shutil.which(name)
            if path:
                return Compiler(kind=kind, path=path, version=_version_line(path))
    raise ToolchainError(
        "Nenhum compilador C++ encontrado (clang++/g++). "
        "Instale Xcode CLT (macOS) ou build-essential/g++ (Linux)."
    )


def find_cmake() -> str | None:
    return shutil.which("cmake")


def find_make() -> str | None:
    return shutil.which("make")


def has_cpp_toolchain() -> bool:
    try:
        find_cpp_compiler()
    except ToolchainError:
        return False
    return True
