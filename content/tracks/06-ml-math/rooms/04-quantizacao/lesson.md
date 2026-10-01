# Quantização e ponto fixo

## Ideia

Mapear float → inteiro para caber em menos bits:

`q = round(x / scale) + zero_point` (afim clássico)
ou simétrico: `q = round(x / scale)` com range centrado em 0.

float32 → int8: **4×** menos memória de pesos (1 byte vs 4).

## Scale

`scale ≈ (x_max − x_min) / (q_max − q_min)`.
Para int8 signed típico, q ∈ [−128, 127].

## Ponto fixo (fixed-point)

Sem FPU, MCU pode usar Q-format: interpretar inteiro como real com fator `2⁻ⁿ` implícito.
É primo da quantização: mesma tensão entre **range**, **resolução** e **overflow**.

## Tradeoff

Menos memória/banda/latência ↔ possível perda de acurácia.
Sempre meça no hardware alvo (golden tests).
