"""Evidence log append-only em ~/.mage/evidence/<namespace>/ (§7).

Cada execução vira um arquivo `<goal>-<ts>.json` com `schema_version` e os campos
mínimos: challenge_id, goal_id, timestamp, git_commit, code_hash, compiler
(+versão+flags), cpu_model, os_kernel, runs, warmup, métricas (mediana e
percentis), noise_flag e explanation.

`latest.json` continua existindo como cópia da execução mais recente
(back-compat). Nada é sobrescrito: o histórico é a fonte do painel semanal e da
curva de p99 no tempo.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from edge_mage.paths import evidence_dir

SCHEMA_VERSION = 2

_SOURCE_SUFFIXES = {
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx",
    ".py", ".rs", ".go", ".js", ".ts", ".sh", ".mk", ".md", ".yaml", ".yml", ".toml",
}
_SKIP_DIRS = {".git", ".hg", ".svn", "build", "dist", "target", "node_modules", ".venv", "venv", "__pycache__"}


@dataclass
class Evidence:
    schema_version: int = SCHEMA_VERSION
    challenge_id: str = ""
    goal_id: str = ""
    timestamp: str = ""
    status: str = "FAIL"  # PASS | FAIL | NOISE
    ok: bool = False
    stage: str = ""
    git_commit: str = ""
    code_hash: str = ""
    compiler: str = ""
    compiler_version: str = ""
    flags: list[str] = field(default_factory=list)
    cpu_model: str = ""
    os_kernel: str = ""
    runs: int = 0
    warmup: int = 0
    metrics: dict = field(default_factory=dict)
    noise_flag: bool = False
    noisy_metrics: list[str] = field(default_factory=list)
    degraded: bool = False
    degraded_reason: str = ""
    explanation: str = ""
    detail: str = ""
    verification_cmd: str = ""
    invocations: int = 0
    duration_s: float = 0.0
    legacy: bool = False

    def to_dict(self) -> dict:
        d = asdict(self)
        d.pop("legacy", None)
        d["schema_version"] = self.schema_version or SCHEMA_VERSION
        return d

    @classmethod
    def from_dict(cls, raw: dict) -> "Evidence":
        data = dict(raw)
        legacy = "schema_version" not in data
        data.setdefault("schema_version", 1)
        known = {f for f in cls.__dataclass_fields__}
        clean = {k: v for k, v in data.items() if k in known}
        clean["legacy"] = legacy
        return cls(**clean)

    @property
    def is_pass(self) -> bool:
        return self.ok and not self.noise_flag


def _cpu_model() -> str:
    if sys.platform == "darwin":
        try:
            out = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True, text=True, timeout=5,
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


def os_kernel() -> str:
    return platform.release() or platform.version() or "unknown"


def cpu_model() -> str:
    return _cpu_model()


def git_commit(work_dir: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(work_dir), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        if out.returncode == 0:
            return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return ""


def code_hash(work_dir: Path) -> str:
    """sha256 determinístico das fontes do work dir (ignora build/.git)."""
    digest = hashlib.sha256()
    if not work_dir.exists():
        return digest.hexdigest()
    for path in sorted(work_dir.rglob("*")):
        if not path.is_file():
            continue
        if any(part in _SKIP_DIRS for part in path.relative_to(work_dir).parts):
            continue
        if path.suffix.lower() not in _SOURCE_SUFFIXES and path.name not in ("Makefile", "CMakeLists.txt"):
            continue
        rel = path.relative_to(work_dir).as_posix()
        try:
            data = path.read_bytes()
        except OSError:
            continue
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(data)
        digest.update(b"\0")
    return digest.hexdigest()


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")


def namespace_dir(namespace: str, *, root: Path | None = None) -> Path:
    return (root or evidence_dir()) / namespace


def write(record: Evidence, *, root: Path | None = None) -> Path:
    """Grava <ns>/<goal>-<ts>-<hash>.json e atualiza latest.json (append-only)."""
    base = namespace_dir(record.challenge_id, root=root)
    base.mkdir(parents=True, exist_ok=True)
    goal = record.goal_id or "goal"
    short = (record.code_hash or "nohash")[:8]
    path = base / f"{goal}-{_stamp()}-{short}.json"
    n = 1
    while path.exists():
        path = base / f"{goal}-{_stamp()}-{short}-{n}.json"
        n += 1
    payload = json.dumps(record.to_dict(), indent=2, ensure_ascii=False) + "\n"
    path.write_text(payload, encoding="utf-8")
    (base / "latest.json").write_text(payload, encoding="utf-8")
    return path


def read_file(path: Path) -> Evidence | None:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(raw, dict):
        return None
    return Evidence.from_dict(raw)


def attach_explanation(
    namespace: str,
    goal_id: str,
    explanation: str,
    *,
    root: Path | None = None,
) -> Path | None:
    """Anexa a explicação (§2/§7) à execução mais recente da meta.

    Reescreve apenas o registro daquela execução (mesmo timestamp); o histórico
    das demais permanece intacto.
    """
    base = namespace_dir(namespace, root=root)
    if not base.exists():
        return None
    candidates: list[Path] = []
    for path in sorted(base.glob(f"{goal_id}-*.json")):
        if path.name == "latest.json":
            continue
        candidates.append(path)
    if not candidates:
        return None
    target = candidates[-1]
    rec = read_file(target)
    if rec is None:
        return None
    rec.explanation = explanation
    payload = json.dumps(rec.to_dict(), indent=2, ensure_ascii=False) + "\n"
    target.write_text(payload, encoding="utf-8")
    (base / "latest.json").write_text(payload, encoding="utf-8")
    return target


def read_latest(namespace: str, *, root: Path | None = None) -> Evidence | None:
    path = namespace_dir(namespace, root=root) / "latest.json"
    if not path.exists():
        return None
    return read_file(path)


def iter_namespace(namespace: str, *, root: Path | None = None) -> list[Evidence]:
    base = namespace_dir(namespace, root=root)
    if not base.exists():
        return []
    out: list[Evidence] = []
    for path in sorted(base.glob("*.json")):
        if path.name == "latest.json":
            continue
        rec = read_file(path)
        if rec is not None:
            out.append(rec)
    return out


def iter_all(*, root: Path | None = None) -> list[Evidence]:
    base = root or evidence_dir()
    if not base.exists():
        return []
    out: list[Evidence] = []
    for d in sorted(p for p in base.iterdir() if p.is_dir()):
        out.extend(iter_namespace(d.name, root=base))
    out.sort(key=lambda r: r.timestamp)
    return out
