# Conceito — On-device checklist

## Itens típicos
- **export** validado (`.pte` / `.tflite` / ONNX → runtime)
- footprint pós-quant + arena
- kernels (CMSIS-NN / NPU) sem surpresa de fallback
- golden float vs int8 no hardware
- latência p50/p99 + orçamento mW
- caminho de degradação (CPU fallback)

## Rank
Completar esta sala = competência real de inferência embarcada — não só XP.
