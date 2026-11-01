# Conceito — Fazer o dado caber

SIMD sem tiling é teatro se cada lane espera DRAM.

## Tiling / blocking

Processe blocos que cabem em L1/L2. Em GEMM, tiling é o coração do desempenho (próximo pilar).

## Prefetch

Hardware prefetch ajuda streams regulares; software prefetch é arma de dois gumes — meça.

## Layout

SoA favorece loads alinhados para SIMD; AoS é conveniente semanticamente. Escolha com harness, não dogma.

