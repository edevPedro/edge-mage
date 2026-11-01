# Conceito · Forge F0 — Baseline Escalar e Harness

Antes de "otimizar", você precisa de um **referente correto** e mensurável.

## O que esta etapa ensina

1. **Golden reference** — implementação escalar simples o bastante para auditar à mão
2. **Test harness** — entrada fixa, checagem de correção contra golden
3. **Benchmark harness** — repetição, warm-up, estatísticas
4. **Contrato de evidência** — máquina, flags, N, mediana/p95

## Escolha de Projeto

Veja `docs/SPEC-forge.md` para opções. Recomendações:

| Projeto | Quando Escolher |
|---------|-----------------|
| **GEMM** | Foco em HPC, compute-bound, álgebra linear |
| **FIR Filter** | Foco em DSP, signals, edge, memory-bound típico |
| **Jacobi/Heat** | Foco em PDE, simulação, stencil |

## Estrutura de Código Sugerida

```
forge/
├── CMakeLists.txt
├── src/
│   ├── gemm_scalar.cpp    # Implementação baseline
│   └── gemm_scalar.hpp    # Header com assinatura
├── tests/
│   ├── test_golden.cpp    # Testes de correção
│   └── golden/            # Arquivos de referência
└── bench/
    └── benchmark.cpp       # Medição de performance
```

## Exemplo: GEMM Escalar

```cpp
// gemm_scalar.hpp
void gemm_scalar(const float* A, const float* B, float* C, int N);

// gemm_scalar.cpp
void gemm_scalar(const float* A, const float* B, float* C, int N) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            float sum = 0.0f;
            for (int k = 0; k < N; k++) {
                sum += A[i*N + k] * B[k*N + j];
            }
            C[i*N + j] = sum;
        }
    }
}
```

## Harness de Teste

```cpp
// test_golden.cpp
#include <cmath>
#include <vector>
#include "gemm_scalar.hpp"

bool check_golden(const float* C, const float* golden, int N, float tol) {
    for (int i = 0; i < N*N; i++) {
        if (std::fabs(C[i] - golden[i]) > tol) return false;
    }
    return true;
}

int main() {
    const int N = 4;
    std::vector<float> A(N*N), B(N*N), C(N*N), golden(N*N);
    // Inicializa com valores conhecidos e verifica contra golden
    gemm_scalar(A.data(), B.data(), C.data(), N);
    if (!check_golden(C.data(), golden.data(), N*N, 1e-5f)) {
        return 1;  // FAIL
    }
    return 0;  // PASS
}
```

## Harness de Benchmark

```cpp
// benchmark.cpp
#include <chrono>
#include <vector>
#include <algorithm>
#include "gemm_scalar.hpp"

int main() {
    const int N = 512;
    const int WARMUP = 5;
    const int RUNS = 30;
    
    std::vector<float> A(N*N), B(N*N), C(N*N);
    
    // Warm-up
    for (int i = 0; i < WARMUP; i++) {
        gemm_scalar(A.data(), B.data(), C.data(), N);
    }
    
    // Medições
    std::vector<double> times;
    for (int i = 0; i < RUNS; i++) {
        auto start = std::chrono::high_resolution_clock::now();
        gemm_scalar(A.data(), B.data(), C.data(), N);
        auto end = std::chrono::high_resolution_clock::now();
        double ms = std::chrono::duration<double, std::milli>(end-start).count();
        times.push_back(ms);
    }
    
    std::sort(times.begin(), times.end());
    double median = times[RUNS/2];
    double p95 = times[(int)(RUNS * 0.95)];
    
    printf("N=%d, median=%.2f ms, p95=%.2f ms\n", N, median, p95);
    return 0;
}
```

## Critérios de Aprovação F0

- [ ] Código compila com `-Wall -Wextra` sem warnings
- [ ] Teste de correção passa (golden comparison)
- [ ] Benchmark documenta: máquina, compilador, flags, N
- [ ] Benchmark reporta: mediana, p95, número de runs
- [ ] Artefato em `study-log/artifacts/forge-f0-scalar.md`
- [ ] Commit no git com mensagem descritiva

## Por que vem antes de NEON/Metal/inferência

SIMD e GPU só fazem sentido se você sabe *o que* está acelerando e *como* provar que não quebrou a matemática. F0 é essa âncora.

## M4 / offline

Tudo roda no host ARM64 com compilador local (clang/gcc). Sem rede. Sem SVE.
