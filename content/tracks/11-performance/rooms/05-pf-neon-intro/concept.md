# Conceito — NEON (Advanced SIMD)

NEON opera em registradores vetoriais (tipicamente **128-bit**) com lanes tipadas (`f32`, `f16`, `i8`, `u16`, …). É a ferramenta certa para map/reduce densos, stencils pequenos, DSP e kernels de math que cabem em ASIMD.

## Intrinsics vs autovec

| Abordagem | Prós | Contras |
|-----------|------|---------|
| **Autovec** (`-O3`, pragmas) | Pouco código | Quebra com aliasing, dependências de loop, padrões irregulares |
| **Intrinsics** | Controle de lanes/loads | Exige harness e prova de correção |
| **Asm hand-written** | Máximo controle | Custo de manutenção alto — só com evidência |

## M4 caveat (obrigatório)

Apple Silicon **M4 não oferece SVE** como lab nativo. Larguras predicadas SVE são literacy para servidores Arm / docs comparativos. Aqui o profundo é **NEON/ASIMD**.

## Antes de vetorizar

Pergunte com Roofline/contadores: o loop é memory-bound? Se sim, tiling/layout primeiro; NEON sem alimento de cache só acelera a espera.
