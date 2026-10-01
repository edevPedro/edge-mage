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

## Ordem de estudo recomendada

```text
Fundamentos
  trig → vetores → exp/log → álgebra linear (normas, matmul)
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
  derivadas/cadeia → gradiente → loss/LR → batch/epoch
       ↓
ML Math
  probabilidade → softmax/CE (+ código estável) → matmul/FLOPs → quantização/fixed-point
       ↓
Edge AI Low-Level
  memory layout → FLOPs/banda → SIMD/latência → checklist on-device
```

## Trilhas e salas

| Ordem | Trilha | Unlock | Salas | Skills (grimório) |
|------:|--------|-------:|-------|-------------------|
| 1 | Fundamentos | 0 | trigonometria, vetores, exponenciais-logs, algebra-linear | Trigonometria Arcana → Feitiço Matricial |
| 2 | Programação | 100 | python-basico, numpy-intuicao, desafios | Runas de Python → Codex |
| 3 | Física & Sinais | 250 | cinematica, ondas, amostragem | Movimento → Nyquist |
| 4 | Elétrica Edge | 500 | ohm, divisao-tensao, adc-potencia | Ohm → Escada ADC |
| 5 | Robótica | 800 | transforms-2d, cinematica-robo, sensores | Portal 2D → Percepção |
| 6 | Otimização | 1100 | derivadas, gradiente, loss-lr, batch-epoch | Tangente → Epoch Ritual |
| 7 | ML Math | 1650 | probabilidade, softmax-ce, matmul-flops, quantizacao | Oráculo → Int8 |
| 8 | Edge AI | 2300 | memory-layout, flops-bandwidth, simd-latency, on-device | Layout → **Edge Mage** |

XP total disponível ≈ **3144+** (bosses). Rank **Edge Mage** = **2900 XP + ritual on-device** (artefato em `study-log/artifacts/on-device.md`). **31 skills** no grimório.

Track **Edge AI** exige ritual `softmax-estavel` (boss Softmax Estável), além do unlock de XP.

## Bosses / rituais (`09-rituais`)

| Boss | Prova | Gate / reward |
|------|--------|----------------|
| Codex Matricial | `matmul2` + harness | elite-codex |
| Softmax Estável | softmax extremos | abre Edge AI |
| Quant Lab | erro max int8 | elite-quant |
| On-Device | checklist latency/RAM/model/device | **Edge Mage** |

Ver [`SPEC-edge-mage-loop.md`](../SPEC-edge-mage-loop.md).

## Conteúdo por sala

| Arquivo | Papel |
|---------|--------|
| `story.md` | História hipotética — resolver a math = resolver o conflito |
| `concept.md` | Conceitos necessários (estilo editorial LeetCode) |
| `lesson.md` | Desafio / lição operacional + contexto das tasks |
| `room.yaml` | Meta, tasks, `animation:` |

## Princípios pedagógicos aplicados

- **Pré-requisitos**: cada sala só assume o que as anteriores desbloqueiam.
- **Spiral**: trig/matrizes voltam em robótica; matmul/FLOPs voltam em Edge AI; gradiente em código antes da teoria completa de opt.
- **Narrativa**: a história motiva o cálculo; o conceito ensina; as tasks comprovam.
- **Grimório**: skills nomeadas amarram conhecimento a progresso persistente.
- **Idioma**: português claro e profissional.

## Como completar até Edge Mage

Siga a ordem da tabela (ou a gulosa por menor `unlock_xp`). O título **Edge Mage** / skill final `on-device` exige competência real de inferência embarcada — não só XP acumulado cedo.
