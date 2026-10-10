"""Adaptador fino e opcional para o Wave Terminal (§11).

Traduz operações da plataforma para o `wsh` (Wave Shell): abrir blocos, visualizar
arquivos, abrir web e notificar. Quando o Wave não está presente, degrada para o
terminal (macOS `open`, ou apenas mostrando o comando/caminho) — nunca é
obrigatório. Forçar com `MAGE_WAVE=0` (desliga) ou `MAGE_WAVE=1` (exige `wsh`).
"""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

WAVE = "wave"
TERMINAL = "terminal"


@dataclass
class WaveResult:
    ok: bool
    mode: str
    command: str = ""
    message: str = ""


def wsh_path() -> str | None:
    return shutil.which("wsh")


def is_wave() -> bool:
    """True quando o `wsh` está disponível (Wave presente). `MAGE_WAVE=0` desliga."""
    override = os.environ.get("MAGE_WAVE", "").strip().lower()
    if override in ("0", "false", "no"):
        return False
    # `wsh` só existe com o Wave instalado — é o sinal confiável.
    return wsh_path() is not None


def _exec(argv: Sequence[str]) -> tuple[bool, str]:
    try:
        proc = subprocess.run(list(argv), capture_output=True, text=True, timeout=15)
        out = (proc.stdout or proc.stderr or "").strip()
        return proc.returncode == 0, out
    except (OSError, subprocess.SubprocessError) as exc:  # noqa: BLE001
        return False, str(exc)


def _as_argv(cmd: str | Sequence[str]) -> list[str]:
    if isinstance(cmd, str):
        return shlex.split(cmd)
    return [str(c) for c in cmd]


def _open_native(path: str) -> WaveResult:
    if sys.platform == "darwin":
        ok, out = _exec(["open", path])
        return WaveResult(ok, TERMINAL, f"open {path}", out)
    return WaveResult(True, TERMINAL, "", f"abra manualmente: {path}")


def run(cmd: str | Sequence[str], *, title: str = "", cwd: str | Path | None = None) -> WaveResult:
    """Abre um bloco Wave executando o comando; no terminal, apenas informa."""
    argv = _as_argv(cmd)
    display = " ".join(argv)
    if is_wave():
        wargv = ["wsh", "run", "--"]
        if title:
            wargv += ["-t", title]
        if cwd:
            wargv += ["--cwd", str(cwd)]
        wargv += argv
        ok, out = _exec(wargv)
        return WaveResult(ok, WAVE, " ".join(wargv), out)
    return WaveResult(True, TERMINAL, display, f"execute no terminal: {display}")


def view(path: str | Path) -> WaveResult:
    """Visualiza um arquivo (SVG/PNG/Markdown) no Wave; no terminal, abre nativo."""
    p = Path(path).expanduser()
    if not p.exists():
        return WaveResult(False, TERMINAL, "", f"arquivo não existe: {p}")
    if is_wave():
        ok, out = _exec(["wsh", "view", str(p)])
        return WaveResult(ok, WAVE, f"wsh view {p}", out)
    return _open_native(str(p))


def open_url(url: str) -> WaveResult:
    if is_wave():
        ok, out = _exec(["wsh", "web", "open", url])
        return WaveResult(ok, WAVE, f"wsh web open {url}", out)
    return _open_native(url)


def notify(message: str, *, title: str = "e-mage") -> WaveResult:
    if is_wave():
        ok, out = _exec(["wsh", "notify", "-t", title, "-m", message])
        return WaveResult(ok, WAVE, f"wsh notify -t {title} -m {message}", out)
    return WaveResult(True, TERMINAL, "", f"[{title}] {message}")
