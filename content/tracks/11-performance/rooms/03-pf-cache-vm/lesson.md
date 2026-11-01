# Lição — Cache na Prática

## Exercício: Bytes por Iteração

Para um loop simples:

```c
for (int i = 0; i < N; i++) {
    C[i] = A[i] + B[i];  // 3 arrays de float
}
```

**Análise:**
- Lê: 2 × 4 bytes (A[i], B[i]) = 8 bytes
- Escreve: 1 × 4 bytes (C[i]) = 4 bytes
- Total: **12 bytes/iteração**

Se L1 bandwidth é 200 GB/s e operação é 2 FLOP (load+add):
- Intensidade aritmética: 2 / 12 ≈ 0.17 FLOP/byte
- Este código é **memory-bound** (muito abaixo do ponto de equilíbrio Roofline)

## Experimento: Detectando Tamanho de Cache

```c
// Mede latência média de acesso em função do working set
for (size_t size = 1024; size <= 64*1024*1024; size *= 2) {
    // Acesso sequencial ou chase-pointer
    // Observe: latência salta em L1→L2, L2→L3, L3→DRAM
}
```

No Apple M4, espere ver transições em ~192KB (L1), ~16MB (L2).

## Checklist de Diagnóstico

1. **Calcule working set:** Todos os dados ativos cabem em qual nível?
2. **Analise stride:** Acesso é contíguo? Qual fração da cache line é útil?
3. **Conte bytes:** Bytes lidos + escritos por FLOP → intensidade aritmética
4. **Verifique TLB:** Working set > (entradas TLB × page size)?

## Cache Miss vs TLB Miss

| Sintoma | Cache Miss | TLB Miss |
|---------|------------|----------|
| Causa típica | Working set > cache | Working set spans muitas páginas |
| Solução | Tiling, melhor layout | Huge pages, reduzir footprint |
| Ferramenta | Instruments / perf cache-misses | Instruments / dTLB-load-misses |

## Reflexão

Para seu kernel Forge:
- Qual é o working set? Cabe em L1? L2?
- Qual é o stride de acesso? 
- O gargalo é capacity miss, conflict miss, ou TLB miss?

Essas respostas guiam se você precisa de tiling, mudança de layout, ou outras otimizações.

