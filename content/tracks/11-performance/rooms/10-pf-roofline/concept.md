# Conceito — Roofline

Eixo X: intensidade aritmética (flops/byte). Eixo Y: performance (flops/s). Dois tetos: **bandwidth** (diagonal) e **peak compute** (horizontal).

## Como usar

1. Estime flops e bytes do kernel.
2. Meça performance atingida.
3. Classifique memory-bound vs compute-bound.
4. Escolha otimização coerente (tiling vs mais ILP/SIMD).

## Honestidade

Peak teórico ≠ peak sustentado. Anote chip e precisão (f32/f16).

