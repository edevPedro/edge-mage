# SPEC — e-mage / Edge ML loop (quiz → spell → ritual)

Documento de produto/engenharia do loop jogável (curso **Edge**). Implementação em `edge_mage/` + `content/`.  
Produto unificado: **e-mage** (Fundamentals · Systems · Edge). Repo GitHub: `edge-mage`.

## Princípio

| Camada | Forma | Recompensa |
|--------|--------|------------|
| 1. Quiz | MCQ / numeric / fill | XP baixo, dopamina rápida, ensina |
| 2. Spell | `type: code` + `code_tests` (sandbox 3s) | “Eu escrevi” — aplica o conceito |
| 3. Ritual | Boss room / artefato em `study-log/artifacts/` | Elite skill, portões, **Edge Mage** |

Ctrl+w (História | Conceito | Desafio | Anim | Tarefas), grimório e animações permanecem a casca UX do curso Edge.

## Ranks

### Curso Edge (interno)
- Ranks intermediários: **só XP** (`ranks.rank_from_xp`), mas o topo é um **teto**.
- **Edge Mage**: `effective_rank(xp, has_on_device_ritual, has_published_artifact)` — exige XP ≥ 2900, ritual `on-device` **e** artefato publicado (`mage publish on-device`).
- Sem o artefato, o título fica em Arquimago mesmo com XP alto.

### Global (e-mage)
- none → **Mago base** (Fundamentals clear) → intermediate → **Mago Supremo**.
- **Teto de XP (Fase 3):** o rank global só passa de Mago base com ≥1 boss aprovado **e** artefato publicado.
- Mago Supremo: systems boss craft + edge on-device + shared math evidence (todos publicados) **ou** rota Neurotech MSc climax.


## Validators

- `validators.validate_task` — mcq / numeric (hint “off by ~…”) / fill / code / ritual.
- Code: tempfile + subprocess, timeout 3s, denylist de imports/I/O; preferir `code_tests` (harness importa `solution`).
- Ritual: lê `study-log/artifacts/<id>.md`. On-device exige campos `latency_ms`, `ram_mb`, `model`, `device`.

## Progressão (`ProgressState` v3)

Campos extras: `unlocked_skills`, `rituals`, `mastery`, `daily_run`, `daily_combo`, `combo_date`, `unlocked_tracks`.

- **Streak mana**: após 3 dias de streak, XP ×1.25; perder o streak zera o multiplicador (volta a 1.0).
- **Combo diário**: até 4 clears no mesmo dia (cerimônia).
- **Mastery**: sala limpa → `M` / opção Mastery; variantes por seed; XP/3; contador 0..3.
- **Gates**: `room.requires_skills` / `track.requires_ritual` / `track.requires_skills`.
- **Boss**: `boss: true` → ao limpar, marca `rituals[room.id]`, pode `elite_skill` e `unlocks_track`.

## Daily Run

- Home `☀ Run de hoje` / `:daily`.
- Seed = hash da data.
- Pacote: (1) review variante de sala limpa, (2) task nova da próxima porta pedagógica.
- Estado em `progress.daily_run`.

## Continuar

- `:continue` / botão Continuar → `curriculum.next_open_room` (ordem `track.order`).
- Uma porta, não oito trilhas.

## Grimório

- `content/grimoire/skills.yaml` — skills por sala + elites de ritual.
- `:grimorio` / `gr` — obtidas vs seladas.
- Statusline `✧n/total`.

## git_journal

- Task 1ª vez → `study-log/completions.jsonl` + commit/push.
- Ritual → `journal_artifact` commita `study-log/artifacts/<boss>.md`.
- `:sync` inclui ledger + artifacts.

## Bosses (`tracks/09-rituais`)

| Boss | Prova | Reward |
|------|--------|--------|
| Codex Matricial | `matmul2` + harness | `elite-codex` |
| Softmax Estável | softmax extremos | `elite-softmax` + libera track `edge-ai` (`requires_ritual: softmax-estavel`) |
| Quant Lab | erro max int8 (+ PTQ) | `elite-quant` |
| On-Device (Edge AI) | checklist markdown + runtime cite | ritual `on-device` → rank Edge Mage |

Pré-requisitos Edge AI (após Softmax ritual): layout → FLOPs → SIMD → AArch64 → **export-runtime** → **cmsis-nn** → on-device.

## Cerimônia

`CeremonyScreen`: banner `+XP`, barra de nível, skill glyph, combo, level-up / rank-up.

## Artefato público (Fase 3)

- `mage publish <boss>` / `:publish <boss>` → `ARTIFACT/<boss>/` (README de uma página + `evidence.json` + gráficos ASCII do evidence log). **Não envia nada**; imprime `git add/commit/push`.
- README: seções **O que medi / O que me surpreendeu / O que faria depois** + Como reproduzir.
- Boss aprovado = ritual passa em `validate_ritual_file`; artefato publicado = README/`evidence.json` válidos (`publish.approved_published_bosses`).
- Sem `ARTIFACT/` publicado, o rank (global e Edge Mage) fica no teto.

## Qualidade (Fase 4)

- `tests/test_runner_sandbox.py`: PASS, FAIL, timeout, compilação quebrada, ruído alto (stdout ≤ 20k chars).
- CI (`.github/workflows/test.yml`): `pytest` + `lint_resources.py` + `scripts/benchmark_smoke.py` em Linux.
- `scripts/lint_resources.py`: resources, teoria curta, prova verificável (não só MCQ), sem segredos.
