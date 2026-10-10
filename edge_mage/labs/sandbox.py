"""Execução em sandbox simples: timeout, rlimits, env limpo e tmpdir.

Honestidade: sem root/privilégios não há isolamento forte de rede/CPU. Este
módulo faz o possível no espaço de usuário (rlimits, env mínimo, cwd dedicado,
sem shell) e documenta os limites. `unshare`/`taskset` ficam para o harness de
latência (Fase 2), com degradação avisada.
"""

from __future__ import annotations

import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

try:  # POSIX only
    import resource as _resource
except ImportError:  # pragma: no cover - non-POSIX
    _resource = None  # type: ignore[assignment]

_HAS_RLIMIT = _resource is not None


@dataclass(frozen=True)
class Limits:
    """Limites de recurso aplicados ao processo filho (best-effort)."""

    cpu_seconds: int = 20
    memory_mb: int = 1024
    file_mb: int = 64
    open_files: int = 256


@dataclass
class RunResult:
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool
    duration_s: float

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and not self.timed_out

    def tail(self, max_lines: int = 8) -> str:
        text = (self.stderr or self.stdout or "").strip()
        if not text:
            return ""
        lines = text.splitlines()
        return "\n".join(lines[-max_lines:])


def clean_env(tmp: Path, *, extra: dict[str, str] | None = None) -> dict[str, str]:
    """Ambiente mínimo — sem segredos, sem rede, home/tmp confinados."""
    env = {
        "PATH": "/usr/bin:/bin:/usr/local/bin",
        "HOME": str(tmp),
        "TMPDIR": str(tmp),
        "TMP": str(tmp),
        "TEMP": str(tmp),
        "LC_ALL": "C",
        "LANG": "C",
        "MAGE_SANDBOX": "1",
    }
    if extra:
        env.update(extra)
    return env


def _rlimit_preexec(limits: Limits):
    def _apply() -> None:  # pragma: no cover - runs in child
        assert _resource is not None
        try:
            _resource.setrlimit(
                _resource.RLIMIT_CPU,
                (limits.cpu_seconds, limits.cpu_seconds + 5),
            )
        except (ValueError, OSError):
            pass
        try:
            hard = limits.memory_mb * 1024 * 1024
            if hard > 0:
                _resource.setrlimit(_resource.RLIMIT_AS, (hard, hard))
        except (ValueError, OSError):
            pass
        try:
            fsize = limits.file_mb * 1024 * 1024
            _resource.setrlimit(_resource.RLIMIT_FSIZE, (fsize, fsize))
        except (ValueError, OSError):
            pass
        try:
            _resource.setrlimit(
                _resource.RLIMIT_NOFILE, (limits.open_files, limits.open_files)
            )
        except (ValueError, OSError):
            pass

    return _apply


def run_process(
    argv: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    limits: Limits | None = None,
    timeout_s: float = 15.0,
) -> RunResult:
    """Executa argv sem shell, com timeout e rlimits (POSIX)."""
    lim = limits or Limits()
    preexec = _rlimit_preexec(lim) if _HAS_RLIMIT else None
    start = time.monotonic()
    try:
        proc = subprocess.run(
            argv,
            cwd=str(cwd),
            env=env if env is not None else clean_env(cwd),
            capture_output=True,
            text=True,
            timeout=timeout_s,
            preexec_fn=preexec,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        duration = time.monotonic() - start
        return RunResult(
            returncode=-1,
            stdout=(exc.stdout or "") if isinstance(exc.stdout, str) else "",
            stderr=(exc.stderr or "") if isinstance(exc.stderr, str) else "",
            timed_out=True,
            duration_s=duration,
        )
    except (OSError, ValueError) as exc:
        return RunResult(
            returncode=-1,
            stdout="",
            stderr=str(exc),
            timed_out=False,
            duration_s=time.monotonic() - start,
        )
    return RunResult(
        returncode=proc.returncode,
        stdout=proc.stdout or "",
        stderr=proc.stderr or "",
        timed_out=False,
        duration_s=time.monotonic() - start,
    )


def environ_has_network() -> bool:
    """Metadado honesto: não bloqueamos rede sem privilégios."""
    return not os.environ.get("MAGE_SANDBOX_NO_NET")
