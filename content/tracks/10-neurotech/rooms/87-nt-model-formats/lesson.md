# Desafio — Contagem de bytes e escolha do runtime

## 1. Objetivo do Desafio
Interiorizar as duas decisões que vêm antes de qualquer kernel: quantos bytes o
modelo ocupa, e qual runtime/serviço combina com o alvo.

## 2. Especificação Técnica e Formulação
- `bytes_for_params(n_params, bits=8)` → `n_params * bits // 8`.
- `suggest_runtime(ram_mb, has_int8_accel, is_llm)`:
  - `"litert"` se `has_int8_accel` (edge com acelerador int8);
  - `"gguf"` se `is_llm` e não tem accel (LLM em CPU local);
  - `"onnx"` caso contrário (servidor genérico).

## 3. Critérios de Validação e Armadilhas
- Busque inteiro (bytes): `bits//8` quando `n_params*bits` for múltiplo de 8.
- A regra de prioridade testa `accel` antes de `is_llm` (uma LLM com NPU int8 →
  LiteRT na prática, carga em NPU).
- Lembre: `bytes = n_params × (bits/8)` — é o mesmo número que decide RAM/VRAM.