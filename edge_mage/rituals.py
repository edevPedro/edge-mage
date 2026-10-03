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

NEURO_REQUIRED_FIELDS = (
    "paper_or_project",
    "url",
    "what_reproduced",
    "metrics",
)

NEURO_ONLINE_TEMPLATE = """# Ritual — Neurotech online loop stub

Parallel circle (does NOT gate Mago Supremo).

- paper_or_project: online-stub
- url: https://github.com/edevPedro/edge-mage/blob/main/docs/SPEC-neurotech-course.md
- what_reproduced: 
- metrics: 
- latency_ms: 
- limits: synthetic EEG only

## Notes
- Window / hop / feature / decision:
- Emulator used (`mage emu synth|cortex`):
"""

NEURO_PAPER_TEMPLATE = """# Ritual — Neurotech paper module

- paper_or_project: paper-module
- url: 
- what_reproduced: 
- metrics: 
- limits: 

## Notes
- CP-MI review map or CP-Riemann figure (SPEC §7)
"""

NEURO_PROJECT_TEMPLATE = """# Ritual — Neurotech project slice

- paper_or_project: project-slice
- url: 
- what_reproduced: 
- metrics: 
- latency_ms: 
- limits: 

## Notes
- CP-Filter bank / decoder MVP / firmware driver / OpenBCI chain
- Emulators: `mage emu all`
"""

NEURO_MAGE_TEMPLATE = """# Ritual — Neuro Mage (boss)

Milestone of the Neural circle (3 runes + online + paper|project).
Continue F11–F14 for Mago Supremo via Neurotech.

- paper_or_project: neuro-mage
- url: https://github.com/edevPedro/edge-mage/blob/main/docs/SPEC-neurotech-course.md
- what_reproduced: 
- metrics: 
- latency_ms: 
- limits: educational noninvasive / synthetic by default

## Checklist
- [ ] neuro-online-loop artifact
- [ ] neuro-paper-module OR neuro-project-slice
- [ ] `mage emu all` exercised
"""

NEURO_RESEARCH_PROPOSAL_TEMPLATE = """# Ritual — Neurotech research proposal (MSc)

- paper_or_project: research-proposal
- url: 
- what_reproduced: proposal fields (question/hypothesis/data/metric/ethics)
- metrics: primary_metric planned
- limits: 

## Fields
- question:
- hypothesis:
- data_source:
- primary_metric:
- ethics_note:
- timeline_weeks:
"""

NEURO_THESIS_METHODS_TEMPLATE = """# Ritual — Neurotech thesis Methods module

- paper_or_project: thesis-methods
- url: 
- what_reproduced: Methods sections (acq/preprocess/model/validation)
- metrics: 
- limits: 

## Methods outline
- data:
- preprocessing:
- features_model:
- validation:
- seeds_versions:
"""

NEURO_RESEARCH_PROJECT_TEMPLATE = """# Ritual — Neurotech mini research project

Drops rune-neuro-research. Evidence for Mago Supremo (Neurotech route).

- paper_or_project: research-project
- url: 
- what_reproduced: 
- metrics: 
- latency_ms: 
- limits: educational noninvasive / synthetic or open data

## DoD
- [ ] data_source declared (synth|open URL)
- [ ] pipeline stages
- [ ] primary_metric value + validation
- [ ] limits honest
"""

NEURO_PAPER_MSC_TEMPLATE = """# Ritual — Neurotech paper module (MSc bar)

- paper_or_project: paper-module-msc
- url: 
- what_reproduced: 
- metrics: 
- limits: 

## MSc bar
- doi:
- figure_or_methods_slice:
- critique_notes:
- reproduction_notes:
"""

NEURO_SUPREMO_TEMPLATE = """# Ritual — Mago Supremo via Neurotech

Same global rank as Edge path. Alternate route — does not erase Edge.

- paper_or_project: neuro-supremo
- url: https://github.com/edevPedro/edge-mage/blob/main/docs/SPEC-neurotech-course.md
- what_reproduced: MSc climax evidence pack
- metrics: 
- latency_ms: 
- limits: educational noninvasive BCI; no clinical claims

## Checklist
- [ ] Mago base (Fundamentals)
- [ ] rune-neuro-acq + decode + online
- [ ] Neuro Mage boss
- [ ] rune-neuro-research + paper-module-msc
- [ ] published-case emulation rooms
- [ ] Edge on-device NOT required on this route
"""


def parse_neuro_checklist(text: str) -> tuple[bool, str, dict[str, str]]:
    found = _parse_field_map(text)
    missing = [k for k in NEURO_REQUIRED_FIELDS if k not in found or not found[k]]
    if missing:
        return False, f"Faltam campos: {', '.join(missing)}", found
    if "http" not in found["url"].lower():
        return False, "url deve ser um link http(s) real", found
    if len(found["what_reproduced"]) < 8:
        return False, "what_reproduced: descreva o módulo/fatia", found
    return True, "Artefato Neurotech válido", found


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


def ensure_neuro_templates(repo_root: Path | None = None) -> list[Path]:
    mapping = {
        "neuro-online-loop": NEURO_ONLINE_TEMPLATE,
        "neuro-paper-module": NEURO_PAPER_TEMPLATE,
        "neuro-project-slice": NEURO_PROJECT_TEMPLATE,
        "neuro-mage": NEURO_MAGE_TEMPLATE,
        "neuro-research-proposal": NEURO_RESEARCH_PROPOSAL_TEMPLATE,
        "neuro-thesis-methods": NEURO_THESIS_METHODS_TEMPLATE,
        "neuro-research-project": NEURO_RESEARCH_PROJECT_TEMPLATE,
        "neuro-paper-module-msc": NEURO_PAPER_MSC_TEMPLATE,
        "neuro-supremo": NEURO_SUPREMO_TEMPLATE,
    }
    out: list[Path] = []
    for rid, body in mapping.items():
        path = artifact_path(rid, repo_root)
        if not path.exists():
            path.write_text(body, encoding="utf-8")
        out.append(path)
    return out


def validate_ritual_file(ritual_id: str, repo_root: Path | None = None) -> tuple[bool, str]:
    path = artifact_path(ritual_id, repo_root)
    neuro_ids = {
        "neuro-online-loop",
        "neuro-paper-module",
        "neuro-project-slice",
        "neuro-mage",
        "neuro-research-proposal",
        "neuro-thesis-methods",
        "neuro-research-project",
        "neuro-paper-module-msc",
        "neuro-supremo",
    }
    if not path.exists() and ritual_id in neuro_ids:
        ensure_neuro_templates(repo_root)
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
    if ritual_id in neuro_ids:
        # Templates alone are not enough — require filled fields
        ok, msg, found = parse_neuro_checklist(text)
        if not ok:
            return ok, msg
        if not found.get("what_reproduced") or found["what_reproduced"].strip() == "":
            return False, "Preencha what_reproduced no artefato Neurotech"
        return True, msg
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
