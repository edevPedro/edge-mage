# SIMD & Latência

**SIMD** (Single Instruction Multiple Data) aplica a mesma op a vários lanes.

## Arm sources

- **A-profile Advanced SIMD (NEON):** [Neon Intrinsics](https://developer.arm.com/architectures/instruction-sets/intrinsics/) + instruction truth in [DDI0487](https://developer.arm.com/documentation/ddi0487/latest).
- **M-profile Helium (MVE) / DSP:** kernel selection in [CMSIS-NN](https://arm-software.github.io/CMSIS-NN/latest/).
- **Microarch throughput hints (Neoverse example):** [Software Optimization Guide](https://developer.arm.com/documentation/swog01195/latest).

128-bit NEON → **16×int8** lanes — o número que aparece em tiles de matmul quantizado.

## Quando ajuda

Kernels regulares (dot, matmul tiles, elementwise) ganham com vetorização e alinhamento.

## Quando não basta

Memory-bound: SIMD acelera compute mas a banda limita. Quantização int8 reduz bytes — muitas vezes o ganho real.

## Tradeoff

Latência/energia ↔ acurácia. Meça no device: p50/p99, mA·s, térmica.
