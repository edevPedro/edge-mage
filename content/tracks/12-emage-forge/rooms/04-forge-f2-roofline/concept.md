# Conceito · Forge F2 — foundation before “mais rápido”

## Pré-requisitos

- IEEE754 honesty + erro (`pf-nla-ieee`)
- Modelo Roofline: teto de memória vs teto de flops (`pf-roofline`)
- Boss de física / GEMM-tiling com correção (`pf-boss-physics`)

## O que esta etapa ensina

Antes de mais intrinsics ou Metal: classifique o kernel Forge como **memory-bound** ou **compute-bound** no seu M4, com um esboço Roofline e uma variante tiled/blocked do *mesmo* golden.

Sem essa fundação, “otimizar” é chute.
