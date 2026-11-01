# Benchmark & profiling edge

"Rápido o suficiente" só existe depois de medir no hardware real — microbenchmarks em segundos de parede mentem. A disciplina de um Edge Mage:

## Ciclos, não stopwatch

No MCU, o relógio do DWT/contador de ciclos é a fonte de verdade. Comparar kernels em **ciclos** e **bytes** (arena) separa custo de instrução do custo de memória.

```
ms = ciclos / (freq_MHz · 1000)
```

## Tokens/s e energia

Para inferência de texto/multimodal:

```
token/s   = n_tokens / tempo_total
E (mJ)    = P (W) · t (s) · 1000
```

O TFLM mantém um [benchmark tool](https://github.com/tensorflow/tflite-micro/blob/main/tensorflow/lite/micro/README.md) oficial; usá-lo dá número comparável entre boards.

## Percentis: o pior caso importa

Média esconde o caso que estoura o SLA. O P95/P99 por índice `round(p/100 · (len − 1))` é o número que você declara no orçamento da pipeline. O código desta sala implementa `cycles_to_ms`, `tokens_per_second`, `energy_mj` e `p95` — as quatro unidades que você usa em toda decisão edge.