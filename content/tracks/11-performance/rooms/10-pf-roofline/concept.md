# Conceito — Modelo Roofline

O Roofline é uma ferramenta visual para diagnosticar se um kernel é **memory-bound** ou **compute-bound**.

## O Gráfico

```
Performance (GFLOPS)
       ↑
       │       ╭─────────────────── Peak Compute (horizontal)
       │      /
       │     /
       │    /
       │   /←── Bandwidth ceiling (diagonal)
       │  /
       │ /
       └────────────────────────────→ Arithmetic Intensity (FLOP/byte)
              Ridge point
```

- **Eixo X:** Intensidade aritmética = FLOPs ÷ bytes transferidos
- **Eixo Y:** Performance atingida (GFLOPS)
- **Diagonal:** Limitado por bandwidth de memória
- **Horizontal:** Limitado por capacidade de compute

## Ridge Point (Ponto de Equilíbrio)

```
Ridge = Peak_FLOPS / Peak_Bandwidth
```

**Exemplo Apple M4 (estimativa):**
- Peak FP32: ~3.5 TFLOPS
- Memory bandwidth: ~100 GB/s
- Ridge point: 3500 / 100 = **35 FLOP/byte**

Kernels com intensidade < 35 são memory-bound; acima são compute-bound.

## Calculando Intensidade Aritmética

### Exemplo 1: SAXPY (y = a*x + y)

```
FLOPs: 2N (1 mul + 1 add por elemento)
Bytes: 3×4×N = 12N (read x, read y, write y, cada float = 4 bytes)

AI = 2N / 12N = 1/6 ≈ 0.17 FLOP/byte
```

**Resultado:** Muito abaixo do ridge point → **memory-bound**

### Exemplo 2: GEMM (C = A×B, N×N)

```
FLOPs: 2N³ (N³ multiplies + N³ adds para N×N output)
Bytes: 3×4×N² = 12N² (read A, read B, write C)

AI = 2N³ / 12N² = N/6 FLOP/byte
```

Para N=512: AI = 512/6 ≈ 85 FLOP/byte → **compute-bound**

## Classificação de Kernels

| Kernel | Intensidade Típica | Classificação |
|--------|-------------------|---------------|
| SAXPY, DAXPY | ~0.17 | Memory-bound |
| SpMV (sparse) | ~0.1-0.5 | Memory-bound |
| GEMM (grande) | N/6 | Compute-bound |
| Convolution | Depende do tile | Variável |
| Stencil (Jacobi) | ~1-2 | Memory-bound |

## Medindo Parâmetros do Sistema

### Peak FLOPS (Teórico)

```
Peak = Cores × (SIMD_width / sizeof(type)) × FMA_factor × Frequency

Exemplo M4 P-core (estimativa):
  = 4 cores × (128/32) × 2 (FMA) × 4 GHz
  = 4 × 4 × 2 × 4 = 128 GFLOPS por P-core cluster
```

### Peak Bandwidth (Medido)

Use STREAM benchmark ou similar:
```bash
# Compilar STREAM
clang -O3 -march=native stream.c -o stream
./stream
```

Ou estime: DDR5 a 6400 MT/s × 8 bytes × canais.

## Otimizações por Região

| Região | Estratégias |
|--------|-------------|
| **Memory-bound** | Melhor layout (SoA), prefetch, tiling, reduzir bytes |
| **Compute-bound** | Mais SIMD, desenrolar loops, FMA, ILP |
| **Ambos** | Provavelmente você mede errado |

## Limitações do Modelo

1. **Peak teórico ≠ sustentado:** Cache misses, branch misses, contenção
2. **Latência ignorada:** Roofline é modelo de throughput
3. **Múltiplas hierarquias:** L1, L2, L3, DRAM têm bandwidths diferentes
4. **Contention:** Múltiplas threads competem por bandwidth

## Roofline Hierárquico

Para análise mais precisa, considere múltiplas linhas de bandwidth:

```
         Peak Compute ─────────
        /
L1 ────/
      /
L2 ──/
    /
L3 /
  /
DRAM
```

O kernel pode ser L2-bound mas L3-compute-bound.

## Ferramentas

| Ferramenta | Uso |
|------------|-----|
| Intel Advisor | Roofline automático (Intel) |
| LIKWID | Linux, funciona em Arm com modificações |
| Manual | Calcule AI + meça FLOPS atingido |
| Instruments (Apple) | Memory bandwidth aproximado |

## Para o Forge F2

1. Calcule AI do seu kernel (mostre a conta)
2. Estime peak FLOPS e bandwidth do seu M4
3. Plote (mentalmente ou graficamente) seu kernel
4. Classifique: memory-bound ou compute-bound?
5. Escolha otimização apropriada para a próxima etapa

