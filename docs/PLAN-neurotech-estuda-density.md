# PLAN — Neurotech Estuda density (thicken vs stub/lite)

**Status:** implementing / done (2026-10-02) — **user override ativo**.  
**Audit disk (pré-upgrade):** 2026-10-02 · 68 rooms · `content/tracks/10-neurotech/`  
**Métrica:** palavras em `lesson.md` + `concept.md` + `story.md`.

## User override (obrigatório)

O plano original sugeria recalibrar horas **para baixo** (~75–110 h) e deixar Batch C como lite/stub permanente. O utilizador rejeitou isso:

1. **Implementar tudo** (Batches A+B+C) — pilares reais com Estuda substancial.
2. **Não baixar horas** — claim guiado sobe para banda MSc-prep crédível **≥120–200 h**, tipicamente **180–300 h** após foundation→advanced (+ EE rooms).
3. Eletivos também recebem conteúdo real; `stub: true` só se ainda houver Estuda útil (preferir conteúdo real).
4. Depth targets: `full` espinha/ética/casos/research; `standard`/`full` em **todos** os pilares required.

As secções abaixo preservam a auditoria e a estrutura de batches como *mapa de trabalho*; **ignorar** qualquer orientação de “recalibrar DOWN” ou “Batch C lite forever”.

---

## 1. Auditoria pré-upgrade (baseline)

| Bucket | Rooms | Total words Estuda | Notas |
|--------|------:|-------------------:|-------|
| Relativamente melhores (âncoras) | 4 | 235–265 | `nt-portal`, `nt-rhythms`, `nt-decode-mvp`, `nt-filter-bank` |
| Resto | 64 | 37–217 | efetivamente stub-lite |
| `stub:` em YAML | 0 | — | campo ainda não existia |

Conclusão histórica: o SPEC prometia **~120–200 h** mas o Estuda não sustentava. Pós-upgrade: Estuda engrossado + salas foundation→advanced + horas **180–300 h**.

---

## 2. Profundidade alvo (pós-override)

| Tag | Palavras L+C+S | h guiadas/sala | Uso |
|-----|----------------|----------------|-----|
| `full` | ≥800–1500+ | 2,5–3,8 | espinha + ética + casos + research gates |
| `standard` | ≥500–1000+ | 1,8–2,8 | **todos** os pilares foundations + apps/FW/CS |
| `lite` | evitar em required | — | só se verdadeiramente residual |
| `stub` | checklist + ponteiro | — | eletivos opcionais *com* Estuda útil; preferir real |

---

## 3. Batches (mapa de implementação)

### Batch A — P0 (espinha + ética + casos + math/elec core)

`nt-ethics-consent`, `nt-portal`, `nt-rhythms` → `nt-filter-bank` → `nt-mi-paradigm` → `nt-features-bandpower` → `nt-decode-mvp` → `nt-cv-leakage` → `nt-stats-bci`, casos Berlin/Comp IV, vectors/matrices/eigen, electrode/ground/ADC.

### Batch B — P1 (online + rubricas + DSP)

stream/online/latency, Welch/artifacts/trial/CSP, hypothesis/IRB, paper critique/proposal, dipole/spike, metrics-offline.

### Batch C — pilares restantes (OVERRIDE: engrossar, não lite forever)

math probability/estimation/gd, physics RC/field/volume, EE opamp/antialias, neuro HH/synapse/maps/plasticity, CS×4, FW×4, filter-design, Riemann, ML, closed-loop, apps×3, rituals, eletivos com Estuda real.

---

## 4. Horas (SPEC) — só para cima

| Estado | Required guided |
|--------|----------------:|
| Pré-upgrade (conteúdo real) | ~35–55 h (honesty audit) |
| Claim antigo SPEC | 120–200 h |
| **Pós-upgrade (alvo)** | **180–300 h** |
| Electives | +10–18 h |

Atualizar SPEC / README / `edevs/.../export.json` em conjunto. Nunca reduzir a faixa enquanto o catálogo engrossa.

---

## 5. Definition of done (override full catalog)

- [x] SPEC §4 horas **≥120–200**, tipicamente **180–300 h**, com phase hours honestas para cima  
- [x] README + export sincronizados  
- [x] Tasks não-trivia: 65 laboratórios de código Python com testes automatizados aplicados em todas as salas técnicas  
- [x] `tests/test_neurotech.py` verde (22 testes passando, incluindo cobertura de código para todas as salas não-rituais)  
- [x] Edge / `mago_supremo` Edge path preservado (sem alteração da rota Edge)

---

## Referência rápida — ordem canônica (tests)

`nt-portal` → ethics → math×6 → physics×5 → elec×5 → neuro×5 → cs×4 → filter-bank → welch → filter-design → artifacts → MI → bandpower → trial → stats → power → cv → decode-mvp → csp → riemann → metrics → ml → stream → irq → mcu → q15 → aarch64 → latency → online → closed-loop → checkpoints → neuro-mage → apps×3 → cases×2 → research×6 → mago-supremo → eletivos×3.
