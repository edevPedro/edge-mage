"""Rituais / bosses — artefatos em study-log/artifacts/."""

from __future__ import annotations

import re
from pathlib import Path

from edge_mage.git_journal import find_repo_root, journal_artifact

ARTIFACT_DIR = Path("study-log/artifacts")

ON_DEVICE_REQUIRED_FIELDS = (
    "latency_ms",
    "ram_mb",
    "model",
    "device",
)

# Systems boss craft — verifiable LLVM artifact (not MCQ farm)
SYSTEMS_BOSS_REQUIRED_FIELDS = (
    "pass_name",
    "ir_before",
    "ir_after",
    "langref_cite",
)

# Shared math evidence toward Mago Supremo
SHARED_MATH_REQUIRED_FIELDS = (
    "concept",  # vectors | grad | fft
    "applied_to",  # systems or edge axis note
    "source_cite",  # free doc/paper URL or title
)


def artifacts_root(repo_root: Path | None = None) -> Path:
    root = repo_root or find_repo_root() or Path.cwd()
    path = root / ARTIFACT_DIR
    path.mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(ritual_id: str, repo_root: Path | None = None) -> Path:
    safe = re.sub(r"[^a-zA-Z0-9_-]+", "-", ritual_id).strip("-") or "ritual"
    return artifacts_root(repo_root) / f"{safe}.md"


def write_artifact(
    ritual_id: str,
    body: str,
    *,
    repo_root: Path | None = None,
) -> Path:
    path = artifact_path(ritual_id, repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.strip() + "\n", encoding="utf-8")
    return path


def _parse_field_map(text: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for line in text.splitlines():
        m = re.match(r"^\s*[-*]?\s*(\w+)\s*[:=]\s*(.+?)\s*$", line)
        if not m:
            continue
        key = m.group(1).lower()
        found[key] = m.group(2).strip()
    return found


def parse_on_device_checklist(text: str) -> tuple[bool, str, dict[str, str]]:
    """Valida markdown com campos latency_ms / ram_mb / model / device."""
    found = _parse_field_map(text)
    missing = [k for k in ON_DEVICE_REQUIRED_FIELDS if k not in found or not found[k]]
    if missing:
        return False, f"Faltam campos: {', '.join(missing)}", found
    # valores numéricos básicos
    try:
        float(found["latency_ms"].replace("ms", "").strip())
        float(found["ram_mb"].replace("mb", "").replace("MB", "").strip())
    except ValueError:
        return False, "latency_ms e ram_mb devem ser numéricos", found
    if len(found["model"]) < 2 or len(found["device"]) < 2:
        return False, "model e device devem ser preenchidos", found
    # prefer a free primary cite in notes when present
    return True, "Checklist on-device válido", found


def parse_systems_boss_checklist(text: str) -> tuple[bool, str, dict[str, str]]:
    """Valida artefato de craft LLVM (pass + LangRef), não stub MCQ."""
    found = _parse_field_map(text)
    missing = [k for k in SYSTEMS_BOSS_REQUIRED_FIELDS if k not in found or not found[k]]
    if missing:
        return False, f"Faltam campos: {', '.join(missing)}", found
    if len(found["ir_before"]) < 8 or len(found["ir_after"]) < 8:
        return False, "ir_before / ir_after devem mostrar IR real (trecho curto ok)", found
    if len(found["langref_cite"]) < 4:
        return False, "langref_cite deve citar instrução/tipo LangRef", found
    if len(found["pass_name"]) < 2:
        return False, "pass_name obrigatório", found
    return True, "Systems boss craft válido", found


def parse_shared_math_checklist(text: str) -> tuple[bool, str, dict[str, str]]:
    """Evidência de math shared aplicada num eixo Systems ou Edge."""
    found = _parse_field_map(text)
    missing = [k for k in SHARED_MATH_REQUIRED_FIELDS if k not in found or not found[k]]
    if missing:
        return False, f"Faltam campos: {', '.join(missing)}", found
    concept = found["concept"].lower()
    if not any(c in concept for c in ("vector", "vetor", "grad", "fft", "dot", "norm")):
        return False, "concept deve ser vectors/grad/FFT (ou afim)", found
    if len(found["applied_to"]) < 8:
        return False, "applied_to: diga onde aplicou (Systems ou Edge + lab)", found
    if len(found["source_cite"]) < 8:
        return False, "source_cite: link/título de fonte gratuita", found
    return True, "Shared math evidence válido", found


ON_DEVICE_TEMPLATE = """# Ritual On-Device — Edge Mage

Preencha com números reais do seu alvo (mesmo que estimado com honestidade).

- latency_ms: 
- ram_mb: 
- model: 
- device: 

## Notas
- Quantização usada:
- Bottleneck (compute/memory):
- Fallback:
- Primary source (Arm docs / arXiv / TFLite):
"""

SYSTEMS_BOSS_TEMPLATE = """# Systems boss craft — Mago Supremo (Systems axis)

Evidence from a real LLVM pipeline (opt / New PM pass / clang -emit-llvm). Not a quiz.

- pass_name: 
- ir_before: 
- ir_after: 
- langref_cite: 

## Notes
- Command used (clang/opt/llc):
- Optional RE/lift note:
"""

SHARED_MATH_TEMPLATE = """# Shared math evidence — Mago Supremo

Apply vectors / gradient / FFT from the shared core on a Systems or Edge lab.

- concept: 
- applied_to: 
- source_cite: 

## Notes
- What number / plot / IR did the math unlock?
"""


def ensure_on_device_template(repo_root: Path | None = None) -> Path:
    path = artifact_path("on-device", repo_root)
    if not path.exists():
        path.write_text(ON_DEVICE_TEMPLATE, encoding="utf-8")
    return path


def ensure_systems_boss_template(repo_root: Path | None = None) -> Path:
    path = artifact_path("systems-boss-craft", repo_root)
    if not path.exists():
        path.write_text(SYSTEMS_BOSS_TEMPLATE, encoding="utf-8")
    return path


def ensure_shared_math_template(repo_root: Path | None = None) -> Path:
    path = artifact_path("shared-math", repo_root)
    if not path.exists():
        path.write_text(SHARED_MATH_TEMPLATE, encoding="utf-8")
    return path


def validate_ritual_file(ritual_id: str, repo_root: Path | None = None) -> tuple[bool, str]:
    path = artifact_path(ritual_id, repo_root)
    if not path.exists():
        return False, f"Crie o artefato em {path}"
    text = path.read_text(encoding="utf-8")
    if ritual_id in {"on-device", "on_device"}:
        ok, msg, _ = parse_on_device_checklist(text)
        return ok, msg
    if ritual_id in {"systems-boss-craft", "systems_boss_craft"}:
        ok, msg, _ = parse_systems_boss_checklist(text)
        return ok, msg
    if ritual_id in {"shared-math", "shared_math"}:
        ok, msg, _ = parse_shared_math_checklist(text)
        return ok, msg
    if len(text.strip()) < 40:
        return False, "Artefato muito curto — documente o ritual."
    return True, "Artefato aceito"


def complete_and_journal_ritual(
    ritual_id: str,
    *,
    store,
    repo_root: Path | None = None,
) -> tuple[bool, str]:
    ok, msg = validate_ritual_file(ritual_id, repo_root)
    if not ok:
        return False, msg
    newly = store.complete_ritual(ritual_id)
    journal_artifact(ritual_id, repo_root=repo_root)
    if newly:
        return True, f"Ritual `{ritual_id}` selado."
    return True, f"Ritual `{ritual_id}` já estava selado."
