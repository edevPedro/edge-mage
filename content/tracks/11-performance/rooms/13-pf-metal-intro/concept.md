# Conceito — Metal first no Apple Silicon

No ecossistema Apple, **Metal** é o caminho nativo para compute e gráficos. O modelo mental mínimo:

1. **MTLDevice** — a GPU lógica.
2. **Command queue** — submissão ordenada de command buffers.
3. **Pipeline state** — shader/função compilada + configuração.
4. **Buffers / textures** — memória do device (e, quando preciso, shared).
5. **Threadgroups** — granularidade de dispatch no grid.

## Por que Metal antes de CUDA aqui

O alvo pedagógico deste curso, no Mac, é **fechar o loop de evidência** no hardware que o aluno já tem. CUDA continua como **eletiva de literacy** (papers, bases NVIDIA, vocabulário SM/warp) — não como substituto do lab M-series.

## Metal ≠ CUDA (detalhes que importam)

| Tema | Metal | CUDA (típico) |
|------|-------|----------------|
| Tooling | Xcode, Metal System Trace / Instruments | nvcc, Nsight |
| Memória | buffers/heaps tipados Metal; unified memory nos M-series muda o jogo | device/host/unified com semântica NVIDIA |
| Linguagem de kernel | MSL | CUDA C++ |
| Ocupação | threadgroup size + device limits | blocks/warps/SMs |

Transferências CPU↔GPU ainda podem dominar kernels pequenos — o boss exige medir **com** e **sem** pretender que copy é grátis.

## Ligação com Performance Boss

O boss Metal Compute Engine pede referência CPU + kernel Metal + golden. Esta sala só abre o vocabulário; a próxima aprofunda padrões de kernel.
