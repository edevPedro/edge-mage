# Trilha 10 — Neurotech (`neurotech`)

Círculo paralelo ao **Edge ML Mage**. SPEC: [`docs/SPEC-neurotech-course.md`](../../../docs/SPEC-neurotech-course.md).

## Pedagogia

```text
Estuda (lição + história + animação/conceito) → Sala (lab / FLAG / emulator)
```

Checkpoints = módulo de paper **ou** fatia de projeto real (caminhos paralelos; boss pede evidência de **um** + online stub).

Gates TUI: campo `requires_rooms` (+ `requires_rooms_any` no boss). Ordem de lista = `order` no YAML (pastas `NN-` alinhadas).

## Como abrir

```bash
# TUI
mage --course neurotech
# ou launcher → Neurotech

# Emuladores (sem hardware)
mage emu all          # synth + artifacts + cortex + latency + online
mage emu synth
mage emu artifact
mage emu cortex
python -m edge_mage.emulators latency
python -m edge_mage.emulators online
```

Web (edevs Estudo): `/estudo/cursos/neurotech` (export + CTA terminal).

## Agentes

| Domínio | Skill |
|---------|--------|
| Pedagogia | `agent-pedagogo` |
| BCI | `agent-bci` |
| Neuroeng | `agent-neuroeng` |
| Elétrica | `agent-eletrica` |
| Física | `agent-fisica` |
| Neurociência | `agent-neurociencia` |

## Salas (F0→F6) — ordem pedagógica

| # | id | Fase | Título |
|--:|----|------|--------|
| 1 | `nt-portal` | F0 | Portal do círculo Neural |
| 2 | `nt-ethics-consent` | F0 | Ética, consentimento, dual-use |
| 3 | `nt-dipole-scalp` | F1 | Dipolo → potencial de escalpo |
| 4 | `nt-spike-lfp` | F1 | Spike → LFP |
| 5 | `nt-volume-blur` | F1 | Condução de volume |
| 6 | `nt-electrode-snr` | F2 | Eletrodo, impedância, SNR |
| 7 | `nt-ground-ref` | F2 | Terra, referência, 50/60 Hz |
| 8 | `nt-adc-bio` | F2 | ADC e escala µV |
| 9 | `nt-rhythms` | F3 | Ritmos α/β/γ/µ (antes do filter) |
| 10 | `nt-filter-bank` | F2 | Banco de filtros EEG |
| 11 | `nt-mi-paradigm` | F3 | Imagética motora (ERD↓/ERS↑) |
| 12 | `nt-artifacts` | F3 | Artefatos |
| 13 | `nt-features-bandpower` | F4 | Potência de banda |
| 14 | `nt-decode-mvp` | F4 | Decode MVP (LDA → κ) |
| 15 | `nt-riemann-primer` | F4 | Primer Riemanniano |
| 16 | `nt-metrics-offline` | F4 | Métricas / vazamento |
| 17 | `nt-stream-buffer` | F5 | Stream + ring buffer |
| 18 | `nt-mcu-filter` | F5 | MCU stub MA/FIR (≠ FBCSP) |
| 19 | `nt-latency-budget` | F5 | Orçamento sense/decide/act |
| 20 | `nt-online-stub` | F6 | Loop online simulado |
| 21 | `nt-checkpoint-paper` | F6 | Ritual módulo de paper (∥ projeto) |
| 22 | `nt-checkpoint-project` | F6 | Ritual fatia de projeto (∥ paper) |
| 23 | `nt-neuro-mage` | F6 | Boss Neuro Mage |

**Cadeia F2:** eletrodo → terra/ref → ADC → ritmos → filter-bank → MI…

**Casos neurológicos clínicos inventados:** não incluídos. SSVEP / CSP profundo = eletivos (SPEC).

## Duração (±)

Ver SPEC §8 — trilha completa ~35–55 h.
