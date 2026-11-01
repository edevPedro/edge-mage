# Pipeline de DL até o device

Uma room só é "edge" quando o modelo percorre o caminho completo com métricas.

## O caminho

1. **Export** — TFLite/ONNX do treino (float) → formato graph de runtime.
2. **Quantização/otimização** — int8 + arena (TFLM [memory management](https://github.com/tensorflow/tflite-micro/blob/main/tensorflow/lite/micro/docs/memory_management.md)).
3. **Runtime/delegate** — [LiteRT Micro](https://developers.google.com/edge/litert/microcontrollers/get_started) com núcleos CMSIS-NN; em A-class, ONNX Runtime mobile.
4. **Golden test** — comparar saída do runtime embarcado contra a referência *float*; sem golden, qualquer regressão de requantização passa despercebida.

## Orçamento de latência

A pipeline tem estágios (acquire de sensor, pré-processamento, inferência, pós):

```
deadline ≥ Σ estágios       → pipeline_ok
headroom = deadline − Σ      → sobra amortece jitter (P99!)
utilização = Σ / deadline    → próximo de 1 = cerrado demais
```

`headroom` é o guarda-chuva do P99: se o P99 da inferência cresce, é ele que absorve o estouro. Os helpers `pipeline_ok`, `headroom_ms` e `utilization` do código codificam exatamente essa conta.

## Golden na prática

"Igual à referência" no int8 significa *dentro da tolerância de requantização* — e é por isso que `utilization` alto (≥0.9) pede re-benchmark antes de subir firmware.