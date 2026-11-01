# Conceito — NEON (Advanced SIMD)

NEON (também chamado Advanced SIMD ou ASIMD) é a extensão SIMD do AArch64. Opera em registradores vetoriais de **128 bits** com lanes tipadas.

## Registradores e Tipos

```
V0-V31: 32 registradores de 128 bits

Visualização de V0:
┌───────┬───────┬───────┬───────┐
│ f32[0]│ f32[1]│ f32[2]│ f32[3]│  float32x4_t (4 lanes)
└───────┴───────┴───────┴───────┘

┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ i8│ i8│ i8│ i8│ i8│ i8│ i8│ i8│ i8│ i8│ i8│ i8│ i8│ i8│ i8│ i8│  int8x16_t (16 lanes)
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
```

### Tipos Comuns

| Tipo C | Lanes | Uso Típico |
|--------|-------|------------|
| `float32x4_t` | 4 | Math, gráficos |
| `float16x8_t` | 8 | ML inference |
| `int32x4_t` | 4 | Índices, acumuladores |
| `int8x16_t` | 16 | Quantização, pixels |

## Intrinsics Essenciais

### Load/Store

```c
#include <arm_neon.h>

float32x4_t a = vld1q_f32(ptr);      // Load 4 floats
vst1q_f32(ptr, a);                    // Store 4 floats

// Versão não-alinhada é o default em NEON
// Alinhamento ajuda mas não é obrigatório
```

### Aritmética

```c
float32x4_t c = vaddq_f32(a, b);      // a + b (4 floats)
float32x4_t c = vmulq_f32(a, b);      // a * b
float32x4_t c = vfmaq_f32(c, a, b);   // c + a*b (FMA)
```

### Broadcast

```c
float32x4_t s = vdupq_n_f32(3.14f);   // [3.14, 3.14, 3.14, 3.14]
```

### Redução

```c
float32x4_t v = ...;
float sum = vaddvq_f32(v);            // Soma horizontal dos 4 lanes
```

## Padrão: SAXPY

```c
// y = a*x + y
void saxpy_neon(float a, const float* x, float* y, int n) {
    float32x4_t va = vdupq_n_f32(a);
    
    int i = 0;
    for (; i + 4 <= n; i += 4) {
        float32x4_t vx = vld1q_f32(&x[i]);
        float32x4_t vy = vld1q_f32(&y[i]);
        vy = vfmaq_f32(vy, va, vx);  // FMA: y = a*x + y
        vst1q_f32(&y[i], vy);
    }
    // Cleanup escalar
    for (; i < n; i++) y[i] = a * x[i] + y[i];
}
```

## Intrinsics vs Auto-vectorização

| Abordagem | Prós | Contras |
|-----------|------|---------|
| **Autovec** (`-O3`) | Código limpo, manutenível | Frágil: aliasing, deps, padrões irregulares |
| **Intrinsics** | Controle preciso | Mais código, menos portável |
| **Assembly** | Máximo controle | Custo de manutenção muito alto |

### Verificando Auto-vectorização

```bash
# Clang: -Rpass=loop-vectorize -Rpass-missed=loop-vectorize
clang++ -O3 -Rpass=loop-vectorize code.cpp

# GCC: -fopt-info-vec-all
g++ -O3 -fopt-info-vec-all code.cpp

# Compiler Explorer: veja o assembly gerado
```

**Por que autovec falha:**
1. Aliasing: compilador não pode provar que arrays não se sobrepõem
2. Loop-carried dependency: cada iteração depende da anterior
3. Controle de fluxo: branches dentro do loop
4. Acesso não-contíguo: scatter/gather

## M4 Caveat (Obrigatório)

| Aspecto | Apple M4 | Cortex-A (ex.) |
|---------|----------|----------------|
| NEON/ASIMD | ✓ Sim | ✓ Sim |
| SVE/SVE2 | ✗ Não | Alguns (server Arm) |
| Vector width | 128-bit | 128-bit (NEON), 128-2048 (SVE) |

**Apple Silicon M4 não tem SVE.** Labs práticos são NEON apenas.
SVE com largura predicada é literacy para servidores Arm (Graviton, etc.), não lab no Mac.

## Antes de Vetorizar

Pergunte com Roofline/contadores:

1. **O loop é memory-bound?** → Otimize layout/tiling primeiro
2. **Há dependências loop-carried?** → SIMD não ajuda diretamente
3. **Acesso é contíguo?** → Scatter/gather é lento

NEON sem dados no cache só acelera a espera por memória.
