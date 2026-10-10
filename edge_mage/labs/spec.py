"""Carrega specs de labs de content/labs/<id>/spec.yaml."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from edge_mage.labs.errors import LabNotFound, LabSpecError
from edge_mage.labs.sandbox import Limits

DEFAULT_STD = "c++20"
DEFAULT_FLAGS = ("-O2", "-pthread")
DEFAULT_SOLUTION_GLOBS = ("*.cpp", "*.cc", "*.cxx")


def labs_root() -> Path:
    override = os.environ.get("MAGE_LABS_ROOT", "").strip()
    if override:
        return Path(override).expanduser()
    from edge_mage.content import content_root

    return content_root() / "labs"


def available_labs() -> list[str]:
    root = labs_root()
    if not root.exists():
        return []
    out: list[str] = []
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        if (d / "spec.yaml").exists():
            out.append(d.name)
    return out


def lab_boss_map(root: Path | None = None) -> dict[str, str]:
    """Mapa boss_id → lab_id para labs marcados como `boss` no spec.yaml."""
    base = root or labs_root()
    out: dict[str, str] = {}
    if not base.exists():
        return out
    for d in sorted(p for p in base.iterdir() if p.is_dir()):
        spec_path = d / "spec.yaml"
        if not spec_path.exists():
            continue
        try:
            raw = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if not isinstance(raw, dict):
            continue
        boss = raw.get("boss")
        if boss is True:
            out[str(raw.get("id") or d.name)] = d.name
        elif isinstance(boss, str) and boss.strip():
            out[boss.strip()] = d.name
    return out


@dataclass
class LabSpec:
    id: str
    title: str
    dir: Path
    summary: str = ""
    std: str = DEFAULT_STD
    flags: list[str] = field(default_factory=lambda: list(DEFAULT_FLAGS))
    solution_globs: list[str] = field(default_factory=lambda: list(DEFAULT_SOLUTION_GLOBS))
    test_sources: list[str] = field(default_factory=list)
    bench_source: str = ""
    include_dirs: list[str] = field(default_factory=lambda: ["include"])
    use_common_include: bool = True
    bench_reps: int = 7
    bench_warmup: int = 2
    timeout_build_s: float = 30.0
    timeout_run_s: float = 15.0
    noise_cv: float = 0.15
    requires_zero_allocs: bool = False
    limits: Limits = field(default_factory=Limits)
    requirements: list[dict] = field(default_factory=list)
    boss_id: str = ""  # != "" quando o lab é a prova de um boss publicável

    # --- resolução de arquivos --------------------------------------------
    def solution_files(self, work_dir: Path) -> list[Path]:
        files: list[Path] = []
        for pattern in self.solution_globs:
            files.extend(sorted(work_dir.glob(pattern)))
        # dedupe preservando ordem
        seen: set[Path] = set()
        out: list[Path] = []
        for f in files:
            if f.is_file() and f not in seen:
                seen.add(f)
                out.append(f)
        return out

    def test_files(self) -> list[Path]:
        return [self.dir / "tests" / name for name in self.test_sources]

    def bench_file(self) -> Path | None:
        return (self.dir / "bench" / self.bench_source) if self.bench_source else None

    def resolved_include_dirs(self, work_dir: Path) -> list[Path]:
        dirs = [work_dir]
        for rel in self.include_dirs:
            p = self.dir / rel
            if p.exists():
                dirs.append(p)
        if self.use_common_include:
            common = labs_root() / "_common"
            if common.exists():
                dirs.append(common)
        return dirs


def _as_list(raw) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        return [raw]
    return [str(x) for x in raw]


def load_spec(lab_id: str, *, root: Path | None = None) -> LabSpec:
    base = root or labs_root()
    lab_dir = base / lab_id
    spec_path = lab_dir / "spec.yaml"
    if not spec_path.exists():
        raise LabNotFound(
            f"lab '{lab_id}' não encontrado em {lab_dir} (esperado spec.yaml)"
        )
    raw = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise LabSpecError(f"{spec_path}: conteúdo YAML inválido")

    limits_raw = raw.get("limits") or {}
    limits = Limits(
        cpu_seconds=int(limits_raw.get("cpu_seconds", 20)),
        memory_mb=int(limits_raw.get("memory_mb", 1024)),
        file_mb=int(limits_raw.get("file_mb", 64)),
        open_files=int(limits_raw.get("open_files", 256)),
    )
    timeout_raw = raw.get("timeout") or {}

    boss_raw = raw.get("boss")
    if boss_raw is True:
        boss_id = str(raw.get("id") or lab_id)
    elif isinstance(boss_raw, str) and boss_raw.strip():
        boss_id = boss_raw.strip()
    else:
        boss_id = ""

    solution = raw.get("solution")
    if "solution" in raw:
        solution_globs = _as_list(solution)
    else:
        solution_globs = list(DEFAULT_SOLUTION_GLOBS)

    spec = LabSpec(
        id=str(raw.get("id") or lab_id),
        title=str(raw.get("title") or lab_id),
        dir=lab_dir,
        summary=str(raw.get("summary") or ""),
        std=str(raw.get("std") or DEFAULT_STD),
        flags=[str(f) for f in (raw.get("flags") or DEFAULT_FLAGS)],
        solution_globs=solution_globs,
        test_sources=_as_list(raw.get("test_sources")),
        bench_source=str(raw.get("bench_source") or ""),
        include_dirs=_as_list(raw.get("include_dirs")) or ["include"],
        use_common_include=bool(raw.get("use_common_include", True)),
        bench_reps=int(raw.get("bench_reps", 7)),
        bench_warmup=int(raw.get("bench_warmup", 2)),
        timeout_build_s=float(timeout_raw.get("build_s", 30)),
        timeout_run_s=float(timeout_raw.get("run_s", 15)),
        noise_cv=float(raw.get("noise_cv", 0.15)),
        requires_zero_allocs=bool(raw.get("requires_zero_allocs", False)),
        limits=limits,
        requirements=[r for r in (raw.get("requirements") or []) if isinstance(r, dict)],
        boss_id=boss_id,
    )
    if not spec.test_sources and not spec.bench_source:
        raise LabSpecError(f"{spec_path}: lab precisa de test_sources e/ou bench_source")
    return spec
