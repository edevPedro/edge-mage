# Currículo Edge Mage — mapa pedagógico

Avaliação e caminho de estudo: da trigonometria ao low-level de Edge AI.

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

## Trilhas e salas (após o fix)

| Ordem | Trilha | Unlock | Salas |
|------:|--------|-------:|-------|
| 1 | Fundamentos | 0 | trigonometria, vetores, exponenciais-logs, algebra-linear |
| 2 | Programação | 100 | python-basico, numpy-intuicao, desafios |
| 3 | Física & Sinais | 250 | cinematica, ondas, amostragem |
| 4 | Elétrica Edge | 500 | ohm, divisao-tensao, adc-potencia |
| 5 | Robótica | 800 | transforms-2d, cinematica-robo, sensores |
| 6 | Otimização | 1100 | derivadas, gradiente, loss-lr, batch-epoch |
| 7 | ML Math | 1650 | probabilidade, softmax-ce, matmul-flops, quantizacao |
| 8 | Edge AI | 2300 | memory-layout, flops-bandwidth, simd-latency, on-device |

XP total disponível ≈ **3144**. Rank **Edge Mage** em **2900 XP** (exige atravessar o núcleo Edge AI).

## Princípios pedagógicos aplicados

- **Pré-requisitos**: cada sala só assume o que as anteriores desbloqueiam.
- **Spiral**: trig/matrizes voltam em robótica; matmul/FLOPs voltam em Edge AI; gradiente em código antes da teoria completa de opt.
- **Tasks**: numéricas com tolerância saneada; código reforça a ideia (não só trivia de siglas).
- **Idioma**: lições em português claro e profissional.

## Como completar até Edge Mage

Siga a ordem da tabela (ou a gulosa por menor `unlock_xp`). Não é obrigatório zerar uma trilha antes de olhar a seguinte quando os gates já abriram — mas a ordem acima evita buracos conceituais.
