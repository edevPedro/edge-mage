# Memory Layout

Tensores precisam de ordem em memória. Duas convenções comuns em visão:

- **NCHW**: batch, canal, altura, largura (comum em treino GPU)
- **NHWC**: batch, altura, largura, canal (comum em alguns kernels CPU/edge)

## Row-major

Em row-major, o **último** índice varia mais rápido no endereço. Localidade ruim ⇒ cache miss ⇒ latência.

## Arena estática

Em MCU, evita-se `malloc` no hot path. Um **memory arena** pré-alocado guarda ativações intermediárias com lifetime planejado (memory planner).

Fragmentação e pico de RAM ditam se o modelo cabe.
