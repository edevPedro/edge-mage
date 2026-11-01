# Conceito — Pipeline, ILP e Execução Moderna

Um processador moderno sobrepõe estágios (fetch → decode → execute → memory → writeback). O custo de um *stall* aparece como CPI efetivo > ideal.

## Pipeline Clássico (5 Estágios)

```
Fetch (IF) → Decode (ID) → Execute (EX) → Memory (MEM) → Writeback (WB)
```

**Ideal:** 1 instrução completa por ciclo (CPI = 1) após pipeline cheio.
**Real:** Hazards inserem bolhas (stalls) que elevam o CPI.

## Hazards

| Tipo | Causa | Exemplo | Mitigação |
|------|-------|---------|-----------|
| **Structural** | Recurso compartilhado | 1 porta de memória para IF e MEM | Duplicar unidades |
| **Data (RAW)** | Resultado não pronto | `add r1, r2, r3; sub r4, r1, r5` | Forwarding |
| **Data (WAW/WAR)** | Nome de registrador | Mais comum em OoO | Register renaming |
| **Control** | Branch não resolvido | `beq` ainda em decode | Predição de branch |

### Forwarding (Bypassing)

```
EX/MEM.Result ──→ ALU.Input (evita esperar WB)
```

Forwarding elimina 1-2 ciclos de stall em RAW simples, mas não resolve todas as dependências (ex.: load-use ainda requer stall).

## Superscalar e Out-of-Order

Processadores modernos (incluindo Apple M-series e Cortex-A) são **superscalares** e **out-of-order**:

- **Superscalar:** Múltiplas instruções por ciclo (2-wide, 4-wide, 8-wide)
- **Out-of-Order (OoO):** Instruções executam quando operandos estão prontos, não na ordem do programa
- **Register Renaming:** Elimina WAW/WAR mapeando registradores arquiteturais para pool físico
- **Reorder Buffer (ROB):** Mantém ordem de commit para exceções precisas

### Pipeline Simplificado OoO

```
Fetch → Decode → Rename → Issue → Execute → Complete → Commit
           ↓                    ↑
    Instruction Queue ──────────┘ (fora de ordem)
```

## Instruction-Level Parallelism (ILP)

ILP é a quantidade de instruções independentes que podem executar em paralelo. Limitantes:

1. **True dependencies (RAW):** Limite fundamental
2. **Tamanho da janela:** Quantas instruções o processador "vê" de uma vez
3. **Unidades funcionais:** Quantas ALUs, load/store units disponíveis
4. **Latência de memória:** Stalls esperando cache/DRAM

### Exemplo: Identificando ILP

```c
// Baixo ILP - cadeia de dependências
a = b + c;    // i1
d = a + e;    // i2 depende de i1
f = d + g;    // i3 depende de i2

// Alto ILP - operações independentes  
a = b + c;    // i1
d = e + f;    // i2 independente de i1
g = h + i;    // i3 independente de i1, i2
```

## Branch Prediction

Branches são ~20% das instruções. Sem predição, o pipeline esvazia a cada branch.

| Técnica | Como Funciona |
|---------|---------------|
| **Static** | Always taken / forward not-taken |
| **BTB** | Branch Target Buffer guarda endereço alvo |
| **BHT** | Branch History Table (2-bit saturating counter) |
| **Pattern History** | Correlação com branches anteriores |

**Custo de miss:** Flush do pipeline (penalidade proporcional à profundidade).

## Apple Silicon vs Cortex-A (Caveat)

| Aspecto | Apple M-series | Cortex-A (e.g., A78) |
|---------|----------------|----------------------|
| Largura decode | 8+ | 4-5 |
| ROB entries | ~600+ | ~200-300 |
| PMU access | Limitado (Instruments) | Direto (perf, Streamline) |

**Não transfira benchmarks cegamente** entre Apple Silicon e Cortex-A.

## O Que Medir

Antes de otimizar com NEON, pergunte:

1. **Latency-bound?** CPI alto, muitos stalls → pipeline é o gargalo
2. **Bandwidth-bound?** Cache misses dominam → memória é o gargalo
3. **ILP-bound?** Dependências limitam paralelismo → reestruture o código

Use contadores (próximas salas) e Roofline para classificar, não intuição.

