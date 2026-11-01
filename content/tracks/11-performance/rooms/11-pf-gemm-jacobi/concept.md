# Conceito — Kernels canônicos

**GEMM** \(C := AB + C\): intensidade alta com tiling → candidato a compute-bound em chips largos.

**Jacobi / heat diffusion**: stencils — muitas vezes memory-bound; tiling e blocking temporal importam.

Use estes como veículos do próximo boss.

