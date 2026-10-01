# Currículo Edge Mage — mapa pedagógico

Avaliação e caminho de estudo: da trigonometria ao low-level de Edge AI.

Cada sala agora tem **História** (cenário narrativo), **Conceito** (editorial pedagógico) e **Desafio** (lição + tasks), com animação TUI quando faz sentido. Completar uma sala concede skills ao **Grimório**.

## O que estava errado (antes do ajuste)

1. **Saltos de pré-requisito**: softmax/CE e desafios de código com softmax apareciam sem exp/log, probabilidade nem intuição de derivada.
2. **Ponte Fundamentos → Otimização → ML fraca**: não havia salas de logs, derivadas/cadeia nem probabilidade.
3. **Programação fora de ordem**: trilha `order: 8` com unlock cedo; softmax em código antes da trilha ML.
4. **Cobertura Edge incompleta**: pouco sobre FLOPs, banda/memory-bound, fixed-point; matmul/FLOPs e quantização rasos.
5. **Lições finas**: várias salas com 5–8 linhas e só 2 tasks (trivia em vez de entendimento).
6. **Rank Edge Mage cedo demais**: 2000 XP antes do checklist on-device — título sem competência plena.
7. **(2026-04 audit ML)** Faltava **autograd**, **export→runtime** (torch.export / ONNX / ExecuTorch / LiteRT) e quant com docs oficiais (PTQ vs QAT) — bar de applicant de mestrado Edge ML.

## Assembly e ISAs — ARM primeiro (Edge / BCI)

**Foco real = AArch64.** Edge ML Mage (e o alvo BCI / on-device) aprofunda **AAPCS64 · DDI0487 · NEON · CMSIS-NN · LiteRT Micro**.  
**Outras ISAs = alfabetização só** — o aluno não fica cego no host/docs alheios, mas **não** há trilha multi-ISA nem profundidade igual.

Não diluir as salas ARM (`aarch64-abi`, `cmsis-nn`, on-device). Systems Mage **não** vira tour de ISAs: x86_64 fica host/RE; RISC-V fica eletiva de 1 sala.

| Sala | Papel | Profundidade |
|------|--------|--------------|
| `intro-asm` | Ler registradores / mov / call-ret + Godbolt | Núcleo shared (crédito único) |
| `isa-x86-aarch64` | **Outras ISAs de relance** — mesmo C, dialetos x86_64 vs AArch64; por que edge ≠ desktop | 1 sala · literacy |
| `riscv-lite` | Eletiva — load/store + `a0`–`a7` vs AAPCS64 | 1 sala · literacy · **não** gate Mago |
| Edge `aarch64-abi` → `cmsis-nn` → on-device (+ LLVM F2) | **Trilha profunda ARM** | Frames, NEON int8, kernels Cortex-M, checklist |

**Fontes oficiais (primárias):** [AAPCS64](https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst) · [DDI0487](https://developer.arm.com/documentation/ddi0487/latest) · [x86-64 psABI](https://gitlab.com/x86-psABIs/x86-64-ABI) / [Intel SDM](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) (breve) · [RISC-V Unpriv](https://docs.riscv.org/reference/isa/v20260120/unpriv/unpriv-index.html) / [psABI](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/) se fizer a eletiva.

RISC-V **não** ensina privileged ISA, Vector `V`, nem core design. x86_64 **não** vira farm de opcodes.

## Ordem de estudo recomendada

```text
Fundamentos
  trig → vetores → exp/log → álgebra linear (normas, matmul)
  (+ shared: bits → intro-asm → isa-x86-aarch64 [glance]; opcional riscv-lite)
       ↓
Programação (espiral da math)
  hypot/dot → argmax/scale → grad_step + matmul2
       ↓
Física & Sinais
  cinemática → ondas → amostragem/Nyquist
       ↓
Elétrica Edge
  Ohm → divisor → ADC/potência
       ↓
Robótica (reusa trig + matrizes)
  transforms 2D → cinemática → sensores
       ↓
Otimização
  derivadas/cadeia → gradiente → loss/LR → batch/epoch → autograd/no_grad
       ↓
ML Math
  probabilidade → softmax/CE (+ código estável) → matmul/FLOPs → quantização (PTQ/QAT)
       ↓
Edge AI Low-Level  ← ARM profundo (edge / BCI)
  memory layout → FLOPs/banda → SIMD → AArch64 ABI
  → export/runtime (torch.export / ONNX / ExecuTorch / LiteRT)
  → CMSIS-NN kernels → checklist on-device
```

## Trilhas e salas

| Ordem | Trilha | Unlock | Salas | Skills (grimório) |
|------:|--------|-------:|-------|-------------------|
| 1 | Fundamentos | 0 | trigonometria, vetores, exponenciais-logs, algebra-linear | Trigonometria Arcana → Feitiço Matricial |
| 2 | Programação | 100 | python-basico, numpy-intuicao, desafios | Runas de Python → Codex |
| 3 | Física & Sinais | 250 | cinematica, ondas, amostragem | Movimento → Nyquist |
| 4 | Elétrica Edge | 500 | ohm, divisao-tensao, adc-potencia | Ohm → Escada ADC |
| 5 | Robótica | 800 | transforms-2d, cinematica-robo, sensores | Portal 2D → Percepção |
| 6 | Otimização | 1100 | derivadas, gradiente, loss-lr, batch-epoch, **autograd** | Tangente → Tape Autograd |
| 7 | ML Math | 1650 | probabilidade, softmax-ce, matmul-flops, quantizacao | Oráculo → Int8 |
| 8 | Edge AI | 2300 | memory-layout, flops-bandwidth, simd-latency, aarch64-abi, **export-runtime**, **cmsis-nn**, on-device | Layout → Export → CMSIS → **Edge Mage** |

XP total disponível ≈ **3300+** (bosses). Rank **Edge Mage** = **2900 XP + ritual on-device** (artefato em `study-log/artifacts/on-device.md`). Skills no grimório crescem com as salas novas.

Track **Edge AI** exige ritual `softmax-estavel` (boss Softmax Estável), além do unlock de XP.

## Bosses / rituais (`09-rituais`)

| Boss | Prova | Gate / reward |
|------|--------|----------------|
| Codex Matricial | `matmul2` + harness | elite-codex |
| Softmax Estável | softmax extremos | abre Edge AI |
| Quant Lab | erro max int8 + PTQ intuição | elite-quant |
| On-Device | checklist latency/RAM/model/device (+ runtime cite) | **Edge Mage** |

Ver [`SPEC-edge-mage-loop.md`](../SPEC-edge-mage-loop.md).

## Conteúdo por sala

| Arquivo | Papel |
|---------|--------|
| `story.md` | História hipotética — resolver a math = resolver o conflito |
| `concept.md` | Conceitos necessários (estilo editorial LeetCode) |
| `lesson.md` | Desafio / lição operacional + contexto das tasks |
| `room.yaml` | Meta, tasks, `animation:` — **resources preferem docs oficiais** (PyTorch / LiteRT / Arm / ONNX) |

## Princípios pedagógicos aplicados

- **Pré-requisitos**: cada sala só assume o que as anteriores desbloqueiam.
- **Spiral**: trig/matrizes voltam em robótica; matmul/FLOPs voltam em Edge AI; gradiente → autograd → export.
- **Narrativa**: a história motiva o cálculo; o conceito ensina; as tasks comprovam.
- **Grimório**: skills nomeadas amarram conhecimento a progresso persistente.
- **Idioma**: português claro e profissional.
- **Fontes**: preferir guias oficiais de framework; papers (arXiv) só quando amarrados a lab.
- **ISA**: profundidade **só** em AArch64 no caminho Edge/BCI; x86_64 e RISC-V = literacia de relance.

## Como completar até Edge Mage

Siga a ordem da tabela (ou a gulosa por menor `unlock_xp`). O título **Edge Mage** / skill final `on-device` exige competência real de inferência embarcada — **treino → export → quant → runtime → golden** — não só XP acumulado cedo.
