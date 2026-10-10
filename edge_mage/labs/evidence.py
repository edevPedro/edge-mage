"""Evidence log reprodutível: ~/.mage/evidence/<lab_id>/<run>.json.

Cada run guarda hash do código, versão do compilador, modelo de CPU, flags e
métricas — para o resultado ser reproduzível e auditável.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from edge_mage.labs.toolchain import Compiler
from edge_mage.paths import evidence_dir

SOURCE_SUFFIXES = {".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx"}

EVIDENCE_SCHEMA = 1


@dataclass(frozen=True)
class HostInfo:
    cpu_model: str
    machine: str
    system: str
    cores: int
    python: str


def iter_source_files(work_dir: Path) -> list[Path]:
    files: list[Path] = []
    if not work_dir.exists():
        return files
    for path in sorted(work_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES:
            files.append(path)
    return files


def code_hash(work_dir: Path) -> str:
    """sha256 determinístico sobre (caminho relativo, conteúdo) das fontes."""
    digest = hashlib.sha256()
    for path in iter_source_files(work_dir):
        rel = path.relative_to(work_dir).as_posix()
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _cpu_model() -> str:
    if sys.platform == "darwin":
        try:
            out = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()
            if out:
                return out
        except (OSError, subprocess.SubprocessError):
            pass
    if sys.platform.startswith("linux"):
        try:
            for line in Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines():
                if line.lower().startswith("model name"):
                    return line.split(":", 1)[1].strip()
        except OSError:
            pass
    return platform.processor() or platform.machine() or "unknown"


def host_info() -> HostInfo:
    return HostInfo(
        cpu_model=_cpu_model(),
        machine=platform.machine(),
        system=platform.system(),
        cores=_cpu_count(),
        python=sys.version.split()[0],
    )


def _cpu_count() -> int:
    try:
        import os

        return os.cpu_count() or 0
    except Exception:  # pragma: no cover
        return 0


def build_record(
    *,
    lab_id: str,
    status: str,
    code_hash_value: str,
    compiler: Compiler,
    std: str,
    flags: list[str],
    metrics: dict,
    tests_ok: bool,
    noisy: bool,
    noisy_metrics: list[str],
    valid_runs: int,
    detail: str = "",
    requirements: list[dict] | None = None,
    requirements_ok: bool = True,
) -> dict:
    host = host_info()
    return {
        "schema": EVIDENCE_SCHEMA,
        "lab_id": lab_id,
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "code_hash": code_hash_value,
        "tests_ok": tests_ok,
        "noisy": noisy,
        "noisy_metrics": noisy_metrics,
        "valid_runs": valid_runs,
        "compiler": {
            "kind": compiler.kind,
            "path": compiler.path,
            "version": compiler.version,
        },
        "std": std,
        "flags": list(flags),
        "host": {
            "cpu_model": host.cpu_model,
            "machine": host.machine,
            "system": host.system,
            "cores": host.cores,
            "python": host.python,
        },
        "metrics": metrics,
        "requirements": requirements or [],
        "requirements_ok": requirements_ok,
        "detail": detail[-2000:],
    }


def write_evidence(lab_id: str, record: dict, *, root: Path | None = None) -> Path:
    base = (root or evidence_dir()) / lab_id
    base.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    short = str(record.get("code_hash", ""))[:8] or "nohash"
    path = base / f"{stamp}-{short}.json"
    payload = json.dumps(record, indent=2, ensure_ascii=False) + "\n"
    path.write_text(payload, encoding="utf-8")
    (base / "latest.json").write_text(payload, encoding="utf-8")
    return path


def read_latest(lab_id: str, *, root: Path | None = None) -> dict | None:
    path = (root or evidence_dir()) / lab_id / "latest.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
