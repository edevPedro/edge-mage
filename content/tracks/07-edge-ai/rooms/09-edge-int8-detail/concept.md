# Conceito — Requantização

## int32 → int8
`q_out = round(q_acc · s_out)` + **clamp** em [−128, 127].

## Per-channel
Escala por canal de saída (mais precisa para pesos com faixas diferentes).

## Viés
Bias é int32 adicionado antes da requantização — nunca int16.