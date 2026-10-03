# Conceito — Estuda → Sala, mapa do círculo, o que BCI é

## Sequência obrigatória

1. **Estuda** — história + conceito + lição (e animação se ensinar).
2. **Sala** — tasks, emulator, FLAG.

Pular o Estuda produz “trivia com skin de mago”, não competência. XP de Edge **não** autoriza pular o portal Neural.

## BCI (nível portal)

Interface cérebro–computador: medir atividade neural (aqui, sobretudo **EEG de escalpo** ou sintético) → processar → emitir comando ou feedback.

| Modo | Fluxo | O que importa |
|------|-------|----------------|
| **Offline** | grava → processa depois | CV sem leak; métricas (κ); papers |
| **Online** | janela deslizante → decisão | orçamento de latência; underrun; feedback |

MVP: preferir **dados sintéticos** (`synth_eeg_stream`) ou datasets abertos citados. Hardware (ex. OpenBCI Cyton) é **eletivo** documentado — não bloqueia Neuro Mage nem o caminho offline.

## Mapa pedagógico (MSc-prep)

| Bloco | O que destrava |
|-------|----------------|
| F0 Ética | Consentimento, Belmont, dual-use literacy, anti-overclaim |
| F1–F5 Pilares | Math (vetor→eigen), physics (dipolo/LFP/blur), EE (SNR/ref/ADC), neuro (HH→ritmos), CS (ringbuf/numerics) |
| F6–F8 Espinha | Filter-bank → MI → bandpower → stats/CV → decode MVP → CSP/Riemann |
| F9 Online/FW | Stream buffer, MCU host stub ≠ QEMU, latency, closed-loop lite |
| F10–F14 | Neuro Mage → apps → casos (Berlin / Comp IV) → research gates → **Mago Supremo** (rota Neural) |

Rota **Edge** a Mago Supremo permanece intacta. Este círculo é rota **alternativa** (`neuro-supremo`).

## Runas (orientação)

| Rune | Sala típica |
|------|-------------|
| `rune-neuro-acq` | `nt-filter-bank` (cadeia de aquisição) |
| `rune-neuro-decode` | `nt-decode-mvp` |
| `rune-neuro-online` | `nt-online-stub` |
| `rune-neuro-research` | `nt-research-project` |

## Limites (repita até cansar)

Não prometemos: diagnóstico clínico, “ler pensamentos”, implantes DIY, vigilância não consentida, weaponização. Foco: literacia + labs seguros + papers abertos (DOI/PMC).

## Honesty notes (curso inteiro)

- **Synth ≠ ERD real** — o emulador ensina pipeline; não substitui sujeito.
- **MCU host stub ≠ QEMU / silício** — latência didática no host.
- **Casos publicados** — walkthrough de Methods/figuras; **não** reprodução bit-a-bit obrigatória.
- **κ / acurácia** — sem chance level e CV honesto, número é teatro.

## Leitura do SPEC

`docs/SPEC-neurotech-course.md` — horas guiadas **~180–300 h**, phase map (EE foundation→advanced), DOIs core, emulators (`mage emu all`), gates de thesis-prep.
