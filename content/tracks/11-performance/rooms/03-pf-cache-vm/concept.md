# Conceito — Hierarquia de Memória e Cache

## O Muro da Memória

CPUs são rápidas; DRAM é lenta. A hierarquia de cache esconde essa latência:

```
Registradores  ~0 cycles    ~KB
       ↓
L1 Cache      ~4 cycles    32-64 KB
       ↓
L2 Cache      ~12 cycles   256 KB - 1 MB
       ↓
L3/LLC        ~40 cycles   8-32 MB (shared)
       ↓
DRAM          ~100+ cycles  GB-TB
```

**Apple M4:** L1 ~192KB (P-cores), L2 ~16MB shared. Unified memory muda o modelo de GPU — dados não "copiam" para VRAM separada.

## Organização do Cache

### Cache Line

- Unidade de transferência: **64 bytes** (típico)
- Acesso a 1 byte carrega toda a linha
- Implicação: stride-1 access aproveita toda a linha; stride-64+ não

### Associatividade

| Tipo | Descrição | Trade-off |
|------|-----------|-----------|
| Direct-mapped | 1 slot por endereço | Rápido, mais conflitos |
| N-way set-associative | N slots por set | Balanceado |
| Fully associative | Qualquer slot | Lento, menos conflitos |

### Tipos de Miss

| Miss | Causa | Solução |
|------|-------|---------|
| **Compulsory** | Primeiro acesso | Prefetch |
| **Capacity** | Cache cheio | Working set menor / tiling |
| **Conflict** | Associatividade esgotada | Padding, layout diferente |

## Localidade

### Temporal
Reusar o mesmo dado em pouco tempo. **Boa:** loop que acessa array várias vezes.

### Espacial
Acessar dados próximos em memória. **Boa:** stride-1 em array. **Ruim:** stride grande, linked list.

### Exemplo: Stride e Cache

```c
// Bom: stride-1 (acessa bytes consecutivos)
for (int i = 0; i < N; i++) sum += arr[i];

// Ruim: stride grande (cada acesso = novo cache line)
for (int i = 0; i < N; i += 64) sum += arr[i];

// Péssimo: acesso aleatório
for (int i = 0; i < N; i++) sum += arr[random_idx[i]];
```

## False Sharing

Em sistemas multi-core, threads diferentes escrevendo na **mesma cache line** (mas endereços diferentes) causam invalidações ping-pong:

```c
// False sharing: contadores em mesma linha
struct { int count_thread0; int count_thread1; } shared;

// Solução: padding para linhas separadas
struct { int count_thread0; char pad[60]; int count_thread1; } shared;
```

## Virtual Memory e TLB

### Tradução de Endereços

```
Virtual Address → Page Table Walk → Physical Address
                       ↓
                 TLB (cache de traduções)
```

**TLB miss:** Page table walk (~100-1000 cycles). Páginas pequenas (4KB) com working set grande = muitos TLB misses.

### Huge Pages

| Tamanho | Entradas TLB (ex.) | Cobertura |
|---------|-------------------|-----------|
| 4 KB | 1024 | 4 MB |
| 2 MB | 1024 | 2 GB |
| 1 GB | 1024 | 1 TB |

**Trade-off:** Huge pages reduzem TLB misses mas podem desperdiçar memória (fragmentação interna).

## Prefetching

### Hardware Prefetch
- CPU detecta padrões de acesso (stride regular)
- Carrega linhas antes de serem pedidas
- Funciona bem para streams lineares

### Software Prefetch
- Instrução explícita: `__builtin_prefetch(ptr)`
- Use com cuidado: pode poluir cache se mal posicionado
- Meça sempre; não assuma benefício

## Ligação com Performance

O modelo Roofline (P4) classifica kernels:

- **Memory-bound:** Espera por dados; otimize layout, tiling, prefetch
- **Compute-bound:** Espera por ALU; otimize ILP, SIMD

Sem entender cache, você não sabe **qual** otimizar. NEON não ajuda se cada instrução espera DRAM.

