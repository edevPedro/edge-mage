# SIMD & Latência

**SIMD** (Single Instruction Multiple Data) aplica a mesma op a vários lanes (NEON, AVX, CMSIS-DSP).

## Quando ajuda

Kernels regulares (dot, matmul tiles, ativações elementwise) ganham com vetorização e alinhamento.

## Quando não basta

Se o kernel é memory-bound, SIMD acelera o compute mas a banda limita.
Quantização int8 reduz bytes — muitas vezes o ganho real de latência/energia.

## Tradeoff

Reduzir latência com quantização/poda pode custar um pouco de acurácia. Meça no device: p50/p99, mA·s, temperatura térmica.
