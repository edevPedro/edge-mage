"""Artefato publicável de boss (`ARTIFACT/`) + gate de rank por evidência.

`mage publish <boss>` **não envia nada**: gera um diretório pronto para o GitHub
(README de uma página + dados do evidence log + gráficos) e imprime os próximos
passos (git add/commit/push, PR, portfólio).

Sem código proprietário, protocolo interno ou dado real de empregador/corretora.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from edge_mage.git_journal import LEDGER_PATH, find_repo_root
from edge_mage.rituals import artifact_path, parse_field_map

PUBLISH_DIR_NAME = "ARTIFACT"

# Seções obrigatórias do README de uma página (spec Fase 3).
REQUIRED_SECTIONS: tuple[str, ...] = (
    "O que medi",
    "O que me surpreendeu",
    "O que faria depois",
    "Como reproduzir",
)

# Bosses cuja prova é um artefato markdown em study-log/artifacts/<id>.md.
MARKDOWN_RITUAL_BOSSES: tuple[str, ...] = (
    "on-device",
    "systems-boss-craft",
    "shared-math",
    "neuro-online-loop",
    "neuro-paper-module",
    "neuro-project-slice",
    "neuro-mage",
    "neuro-research-proposal",
    "neuro-thesis-methods",
    "neuro-research-project",
    "neuro-paper-module-msc",
    "neuro-supremo",
)

# Bosses cuja prova é um harness de código (sem markdown de ritual).
CODE_BOSSES: tuple[str, ...] = ("codex-matricial", "softmax-estavel", "quant-lab")

# Bosses legados cujo proof é markdown/harness (sem lab verificável).
STATIC_BOSSES: tuple[str, ...] = MARKDOWN_RITUAL_BOSSES + CODE_BOSSES

# Mantido por compatibilidade; `known_bosses()` acrescenta os labs verificáveis.
KNOWN_BOSSES: tuple[str, ...] = STATIC_BOSSES


def lab_bosses(repo_root: Path | None = None) -> dict[str, str]:
    """Bosses cuja prova é um lab verificável (spec.yaml com `boss:`)."""
    from edge_mage.labs.spec import lab_boss_map

    if repo_root is not None:
        candidate = Path(repo_root) / "content" / "labs"
        if candidate.exists():
            return lab_boss_map(candidate)
    return lab_boss_map()


def known_bosses(repo_root: Path | None = None) -> tuple[str, ...]:
    """Todos os bosses conhecidos: estáticos + labs verificáveis."""
    labs = tuple(sorted(lab_bosses(repo_root).keys()))
    return STATIC_BOSSES + tuple(b for b in labs if b not in STATIC_BOSSES)

# Bosses que destravam rank (global e por curso).
EDGE_GATE_BOSS = "on-device"
SYSTEMS_GATE_BOSS = "systems-boss-craft"
EVIDENCE_GATE_BOSS = "shared-math"
NEURO_GATE_BOSS = "neuro-supremo"
RANK_GATE_BOSSES: tuple[str, ...] = (
    EDGE_GATE_BOSS,
    SYSTEMS_GATE_BOSS,
    EVIDENCE_GATE_BOSS,
    NEURO_GATE_BOSS,
)

_TITLES: dict[str, str] = {
    "on-device": "On-Device (Edge AI)",
    "systems-boss-craft": "Systems boss craft (LLVM)",
    "shared-math": "Shared math evidence",
    "codex-matricial": "Codex Matricial",
    "softmax-estavel": "Softmax Estável",
    "quant-lab": "Quant Lab",
    "neuro-mage": "Neuro Mage",
    "neuro-supremo": "Mago Supremo (Neurotech)",
}


def _safe(boss_id: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_-]+", "-", boss_id).strip("-")
    return safe or "boss"


def boss_title(boss_id: str) -> str:
    if boss_id in _TITLES:
        return _TITLES[boss_id]
    return boss_id.replace("-", " ").title()


def publish_root(repo_root: Path | None = None) -> Path:
    root = repo_root or find_repo_root() or Path.cwd()
    return root / PUBLISH_DIR_NAME


def boss_dir(boss_id: str, repo_root: Path | None = None) -> Path:
    return publish_root(repo_root) / _safe(boss_id)


def read_evidence_log(repo_root: Path | None = None) -> list[dict[str, Any]]:
    """Lê study-log/completions.jsonl (evidence log)."""
    root = repo_root or find_repo_root() or Path.cwd()
    ledger = root / LEDGER_PATH
    if not ledger.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in ledger.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def _day_of(timestamp: str) -> str:
    if not timestamp:
        return ""
    try:
        return datetime.fromisoformat(timestamp).date().isoformat()
    except ValueError:
        return str(timestamp).split("T", 1)[0]


def cumulative_xp_by_day(entries: list[dict[str, Any]]) -> list[tuple[str, int]]:
    """XP acumulado no fim de cada dia, ordenado por data."""
    totals: dict[str, int] = {}
    for row in entries:
        day = _day_of(str(row.get("timestamp") or ""))
        if not day:
            continue
        try:
            xp = int(row.get("xp_awarded") or 0)
        except (TypeError, ValueError):
            xp = 0
        totals[day] = totals.get(day, 0) + xp
    running = 0
    out: list[tuple[str, int]] = []
    for day in sorted(totals):
        running += totals[day]
        out.append((day, running))
    return out


def counts_by_track(entries: list[dict[str, Any]]) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for row in entries:
        track = str(row.get("track_id") or "?")
        counts[track] = counts.get(track, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def bar_chart(pairs: list[tuple[str, int]], *, width: int = 36, unit: str = "") -> str:
    """Gráfico de barras Unicode a partir de (label, valor) — sem dependências."""
    if not pairs:
        return "_(sem dados no evidence log ainda)_"
    label_w = max(len(str(label)) for label, _ in pairs)
    label_w = min(label_w, 24)
    max_val = max((abs(v) for _, v in pairs), default=0)
    lines: list[str] = []
    for label, value in pairs:
        label_s = str(label)
        if len(label_s) > label_w:
            label_s = label_s[: label_w - 1] + "…"
        filled = 0
        if max_val > 0:
            filled = max(1 if value else 0, round(width * abs(value) / max_val))
        bar = "█" * filled
        lines.append(f"{label_s:<{label_w}} │{bar} {value}{unit}")
    return "\n".join(lines)


def read_artifact_fields(boss_id: str, repo_root: Path | None = None) -> dict[str, str]:
    path = artifact_path(boss_id, repo_root)
    if not path.is_file():
        return {}
    return parse_field_map(path.read_text(encoding="utf-8"))


def read_lab_evidence(lab_id: str) -> dict[str, Any] | None:
    """Última evidência verificável de um lab (``~/.mage/evidence/<lab>/latest.json``)."""
    from edge_mage.labs.evidence import read_latest

    return read_latest(lab_id)


def _fmt_num(value: Any) -> str:
    try:
        num = float(value)
    except (TypeError, ValueError):
        return str(value)
    if num != num:  # NaN
        return "—"
    if num == 0:
        return "0"
    if abs(num) >= 1e6 or abs(num) < 1e-3:
        return f"{num:.3e}"
    return f"{num:,.1f}".replace(",", " ")


def _lab_measure_section(record: dict[str, Any], lab_id: str) -> str:
    if not record:
        return (
            f"_Sem evidência do lab `{lab_id}`. Rode `mage lab run {lab_id}` "
            "para gerar uma medição reproduzível._"
        )
    compiler = record.get("compiler") or {}
    host = record.get("host") or {}
    flags = " ".join(str(f) for f in (record.get("flags") or []))
    status = str(record.get("status") or "?")
    lines = [
        f"Lab: `{lab_id}` · status **{status}** · "
        f"{record.get('valid_runs', 0)} execuções · código `{str(record.get('code_hash', ''))[:12]}`",
        "",
        f"- Compilador: {compiler.get('version', '?')} (`{record.get('std', '?')}` · `{flags}`)",
        f"- CPU: {host.get('cpu_model', '?')} ({host.get('cores', '?')} cores)",
        f"- Consulta: {record.get('timestamp', '?')}",
        "",
    ]
    metrics = record.get("metrics") or {}
    if metrics:
        lines += [
            "| métrica | mediana | p50 | p99 | cv | n |",
            "|---------|--------:|----:|----:|---:|---:|",
        ]
        for name in sorted(metrics):
            m = metrics[name] or {}
            lines.append(
                f"| `{name}` | {_fmt_num(m.get('median'))} | {_fmt_num(m.get('p50'))} "
                f"| {_fmt_num(m.get('p99'))} | {_fmt_num(m.get('cv'))} | {m.get('samples', '?')} |"
            )
        lines.append("")
    requirements = record.get("requirements") or []
    if requirements:
        lines.append("Requisitos (mediana):")
        for req in requirements:
            mark = "ok" if req.get("ok") else "FALHOU"
            lines.append(
                f"- [{mark}] `{req.get('metric')}` {req.get('op')} {_fmt_num(req.get('value'))} "
                f"(atual {_fmt_num(req.get('actual'))})"
            )
        lines.append("")
    if record.get("noisy"):
        noisy = ", ".join(record.get("noisy_metrics") or [])
        lines.append(f"> Ruído detectado em: {noisy}. Rode novamente numa máquina ociosa.")
    return "\n".join(lines).rstrip()


def _evidence_summary(entries: list[dict[str, Any]]) -> dict[str, Any]:
    days = [d for d, _ in cumulative_xp_by_day(entries)]
    total_xp = 0
    for row in entries:
        try:
            total_xp += int(row.get("xp_awarded") or 0)
        except (TypeError, ValueError):
            pass
    return {
        "entries": len(entries),
        "total_xp": total_xp,
        "first_day": days[0] if days else None,
        "last_day": days[-1] if days else None,
        "active_days": len(days),
    }


def _measure_table(fields: dict[str, str]) -> str:
    if not fields:
        return "_Sem campos de ritual markdown — prova registrada pelo harness de código._"
    rows = ["| campo | valor |", "|-------|-------|"]
    for key in sorted(fields):
        value = fields[key].replace("|", "\\|")
        rows.append(f"| `{key}` | {value} |")
    return "\n".join(rows)


def _surprises(fields: dict[str, str], summary: dict[str, Any], xp_days: list[tuple[str, int]]) -> str:
    notes: list[str] = []
    if xp_days:
        peak = max(xp_days, key=lambda kv: kv[1])
        notes.append(
            f"- Dia de maior XP acumulado: **{peak[0]}** ({peak[1]} XP)."
        )
    if summary.get("active_days"):
        notes.append(f"- **{summary['active_days']}** dia(s) ativos no evidence log.")
    if "latency_ms" in fields and "ram_mb" in fields:
        notes.append(
            f"- Orçamento on-device medido: **{fields['latency_ms']} ms**, "
            f"**{fields['ram_mb']} MB**."
        )
    if not notes:
        notes.append("- _Escreva aqui o que te surpreendeu (um número que não esperava)._")
    notes.append(
        "- Escreva aqui **uma** surpresa concreta: um número que desafiou sua intuição."
    )
    return "\n".join(notes)


def _next_actions() -> str:
    return (
        "- Próximo experimento (com critério de sucesso mensurável).\n"
        "- Uma variação de arquitetura/quantização/runtime para comparar.\n"
        "- O que você faria diferente se rodasse de novo amanhã."
    )


def render_readme(
    boss_id: str,
    *,
    fields: dict[str, str],
    entries: list[dict[str, Any]],
    lab_record: dict[str, Any] | None = None,
    lab_id: str = "",
    generated_at: str | None = None,
) -> str:
    when = generated_at or datetime.now(timezone.utc).isoformat()
    title = boss_title(boss_id)
    summary = _evidence_summary(entries)
    xp_days = cumulative_xp_by_day(entries)
    tracks = counts_by_track(entries)
    xp_chart = bar_chart(xp_days[-14:], unit=" XP")
    track_chart = bar_chart(tracks[:10])
    ritual_rel = f"study-log/artifacts/{_safe(boss_id)}.md"

    lab_block = ""
    if lab_id:
        lab_block = (
            "\n### Medição verificável (lab)\n\n"
            + _lab_measure_section(lab_record or {}, lab_id)
            + "\n"
        )

    lab_repro = ""
    if lab_id:
        lab_repro = f"mage lab run {lab_id}   # compila, testa, mede e grava evidência\n"

    return f"""# {title} — artefato de boss

Boss: `{boss_id}` · gerado por `mage publish {boss_id}` em {when}.

Evidência reproduzível e offline. **Sem** código proprietário, protocolo interno
ou dado real de empregador/corretora.

## O que medi

{_measure_table(fields)}

- Tarefas registradas no evidence log: **{summary['entries']}**
- XP total registrado: **{summary['total_xp']}**
- Janela: {summary['first_day'] or "—"} → {summary['last_day'] or "—"} ({summary['active_days']} dia(s))
{lab_block}
## O que me surpreendeu

{_surprises(fields, summary, xp_days)}

## O que faria depois

{_next_actions()}

## Evidência (evidence log)

XP acumulado por dia (últimos 14 dias):

```
{xp_chart}
```

Conclusões por trilha:

```
{track_chart}
```

Prova original: [`{ritual_rel}`](../../{ritual_rel}) · dados brutos: `evidence.json`.

## Como reproduzir

```bash
{lab_repro}# 1) loop do curso (gera study-log/completions.jsonl)
mage --course edge

# 2) preencha o ritual: study-log/artifacts/{_safe(boss_id)}.md
#    (no TUI: :room {boss_id})

# 3) gerar este artefato (idempotente)
mage publish {boss_id}
```

## Notas de honestidade

- Números sintéticos/estimados estão marcados como tal nos campos do ritual.
- Este artefato é didático; não é uma avaliação clínica, financeira ou de produção.
"""


@dataclass
class PublishResult:
    ok: bool
    boss_id: str
    directory: Path | None = None
    files: list[Path] = field(default_factory=list)
    message: str = ""
    next_steps: list[str] = field(default_factory=list)


def generate_boss_artifact(
    boss_id: str,
    *,
    repo_root: Path | None = None,
    generated_at: str | None = None,
) -> PublishResult:
    """Gera ARTIFACT/<boss>/{README.md,evidence.json}. Não envia nada."""
    root = repo_root or find_repo_root() or Path.cwd()
    fields = read_artifact_fields(boss_id, root)
    entries = read_evidence_log(root)
    lab_id = lab_bosses(root).get(boss_id, "")
    lab_record = read_lab_evidence(lab_id) if lab_id else None
    out_dir = boss_dir(boss_id, root)
    out_dir.mkdir(parents=True, exist_ok=True)

    readme = render_readme(
        boss_id,
        fields=fields,
        entries=entries,
        lab_record=lab_record,
        lab_id=lab_id,
        generated_at=generated_at,
    )
    readme_path = out_dir / "README.md"
    readme_path.write_text(readme, encoding="utf-8")

    data = {
        "boss_id": boss_id,
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "ritual_fields": fields,
        "lab_id": lab_id or None,
        "lab_evidence": lab_record,
        "evidence_summary": _evidence_summary(entries),
        "cumulative_xp_by_day": cumulative_xp_by_day(entries),
        "counts_by_track": counts_by_track(entries),
    }
    data_path = out_dir / "evidence.json"
    data_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    return PublishResult(
        ok=True,
        boss_id=boss_id,
        directory=out_dir,
        files=[readme_path, data_path],
        message=f"artefato gerado em {out_dir}",
        next_steps=next_steps(boss_id, root),
    )


def validate_published_boss(
    boss_id: str, repo_root: Path | None = None
) -> tuple[bool, str]:
    root = repo_root or find_repo_root() or Path.cwd()
    out_dir = boss_dir(boss_id, root)
    readme = out_dir / "README.md"
    if not readme.is_file():
        return False, f"README ausente: {readme}"
    text = readme.read_text(encoding="utf-8")
    missing = [s for s in REQUIRED_SECTIONS if s not in text]
    if missing:
        return False, f"README sem seções: {', '.join(missing)}"
    data = out_dir / "evidence.json"
    if not data.is_file():
        return False, f"evidence.json ausente: {data}"
    try:
        json.loads(data.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False, "evidence.json inválido"
    return True, "artefato publicado válido"


def approved_published_bosses(repo_root: Path | None = None) -> set[str]:
    """
    Bosses com prova aprovada **e** artefato publicado válido.
    Somente estes destravam rank (Fase 3).

    - Bosses legados: ritual markdown válido (`study-log/artifacts/<id>.md`).
    - Bosses de lab: evidência verificável PASS (`~/.mage/evidence/<lab>/latest.json`).
    """
    from edge_mage.rituals import validate_ritual_file

    root = repo_root or find_repo_root() or Path.cwd()
    approved: set[str] = set()
    for boss_id in MARKDOWN_RITUAL_BOSSES:
        path = artifact_path(boss_id, root)
        if not path.is_file():
            continue
        ok_ritual, _ = validate_ritual_file(boss_id, root)
        if not ok_ritual:
            continue
        ok_pub, _ = validate_published_boss(boss_id, root)
        if ok_pub:
            approved.add(boss_id)

    for boss_id, lab_id in lab_bosses(root).items():
        record = read_lab_evidence(lab_id)
        if not record or str(record.get("status")) != "PASS":
            continue
        ok_pub, _ = validate_published_boss(boss_id, root)
        if ok_pub:
            approved.add(boss_id)
    return approved


def next_steps(boss_id: str, repo_root: Path | None = None) -> list[str]:
    root = repo_root or find_repo_root() or Path.cwd()
    safe = _safe(boss_id)
    artifact_md = f"study-log/artifacts/{safe}.md"
    return [
        f"Revisar {PUBLISH_DIR_NAME}/{safe}/README.md (seções O que medi / O que me surpreendeu / O que faria depois).",
        f"git add {PUBLISH_DIR_NAME}/{safe} {artifact_md}",
        f'git commit -m "study: publish {boss_id} artifact"',
        "git push   # ou abra um Pull Request",
        f"(opcional) copie {PUBLISH_DIR_NAME}/{safe}/ para o seu repo-portfólio",
        "nada foi enviado automaticamente.",
    ]


def publish_boss(
    boss_id: str,
    *,
    repo_root: Path | None = None,
    require_ritual: bool = True,
) -> PublishResult:
    """
    Prepara o diretório do artefato. Não envia nada.
    Para bosses de ritual markdown, exige que o artefato passe no verificador.
    """
    root = repo_root or find_repo_root() or Path.cwd()
    labs = lab_bosses(root)
    if boss_id not in known_bosses(root):
        return PublishResult(
            ok=False,
            boss_id=boss_id,
            message=(
                f"boss desconhecido: {boss_id}. "
                f"Conhecidos: {', '.join(known_bosses(root))}"
            ),
        )

    if boss_id in labs:
        lab_id = labs[boss_id]
        record = read_lab_evidence(lab_id)
        if not record or str(record.get("status")) != "PASS":
            return PublishResult(
                ok=False,
                boss_id=boss_id,
                message=(
                    f"boss ainda não aprovado — lab `{lab_id}` sem evidência PASS "
                    "(ou máquina ruidosa)."
                ),
                next_steps=[
                    f"Rode `mage lab init {lab_id}` e implemente a solução",
                    f"Depois: mage lab run {lab_id}   # grava evidência em ~/.mage/evidence/",
                    f"Quando passar: mage publish {boss_id}",
                ],
            )

    if require_ritual and boss_id in MARKDOWN_RITUAL_BOSSES:
        from edge_mage.rituals import validate_ritual_file

        ok, msg = validate_ritual_file(boss_id, root)
        if not ok:
            return PublishResult(
                ok=False,
                boss_id=boss_id,
                message=f"boss ainda não aprovado — {msg}",
                next_steps=[
                    f"Preencha study-log/artifacts/{_safe(boss_id)}.md",
                    f"Rode o ritual da sala do boss `{boss_id}` e confirme",
                    f"Depois: mage publish {boss_id}",
                ],
            )

    return generate_boss_artifact(boss_id, repo_root=root)


def status_report(repo_root: Path | None = None) -> str:
    """Lista bosses, prova aprovada e artefato publicado."""
    root = repo_root or find_repo_root() or Path.cwd()
    from edge_mage.rituals import validate_ritual_file

    labs = lab_bosses(root)
    lines = ["BOSS                       PROVA    PUBLICADO"]
    for boss_id in known_bosses(root):
        if boss_id in labs:
            record = read_lab_evidence(labs[boss_id])
            proof_ok = bool(record) and str(record.get("status")) == "PASS"
        elif boss_id in MARKDOWN_RITUAL_BOSSES:
            proof_ok = artifact_path(boss_id, root).is_file() and validate_ritual_file(
                boss_id, root
            )[0]
        else:
            proof_ok = True  # code-harness boss
        pub_ok = validate_published_boss(boss_id, root)[0]
        lines.append(
            f"{boss_id:<26} {'✓' if proof_ok else '·':^7} "
            f"{'✓' if pub_ok else '·':^9}"
        )
    return "\n".join(lines)
