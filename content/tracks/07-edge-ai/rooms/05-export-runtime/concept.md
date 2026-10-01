# Conceito — Export & Runtime

## Pipeline (bar mínimo)
`treino (PyTorch/TF) → export (torch.export / SavedModel) → quant (PTQ/QAT) → runtime (ExecuTorch / LiteRT / ORT) → golden no device`

## Formatos
- **ONNX**: grafo intermediário portátil (`torch.onnx.export`, hoje baseado em `torch.export`).
- **ExecuTorch `.pte`**: runtime PyTorch para mobile/embarcado.
- **LiteRT** (ex-TFLite): runtime Google AI Edge; converter via `TFLiteConverter` / fluxos AI Edge.

## Não pule
`model.eval()` + shapes de exemplo estáveis. Ops sem kernel no acelerador → **fallback CPU**.
