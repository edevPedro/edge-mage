# Memory Layout

Tensores precisam de ordem em memória. Duas convenções comuns em visão:

- **NCHW**: batch, canal, altura, largura (comum em treino GPU)
- **NHWC**: batch, altura, largura, canal (comum em alguns kernels CPU/edge)

## Row-major

Em row-major, o **último** índice varia mais rápido no endereço. Localidade ruim ⇒ cache miss ⇒ latência.

## Tensor arena (fonte oficial)

Em MCU, evita-se `malloc` no hot path. [TFLM Memory Management](https://github.com/tensorflow/tflite-micro/blob/main/tensorflow/lite/micro/docs/memory_management.md) descreve um **tensor arena** compartilhado com seções:

- **Head** — tensores não-persistentes (planner ganancioso reutiliza)
- **Temporary** — alocações de escopo curto
- **Tail** — alocações persistentes

[LiteRT Micro get started](https://developers.google.com/edge/litert/microcontrollers/get_started) mostra o `uint8_t tensor_arena[...]` passado ao interpreter. Fragmentação e pico de RAM ditam se o modelo cabe; alinhe (muitas vezes 16 bytes) para SIMD.
