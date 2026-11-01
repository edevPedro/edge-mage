# Conceito — Formatos de modelo: do checkpoint ao artefato de produção

Depois de treinar, o modelo precisa deixar o ecossistema de treino e virar um
**artefato executável**: grafo + pesos, em um formato que um *runtime* consiga
carregar e rodar no alvo certo.

## 1. Por que não basta o checkpoint do PyTorch
- Checkpoints guardam estado de treino (otimizador, épocas, hooks) — overhead e
  dependência de biblioteca.
- Um formato de inferência (ONNX/GGUF/LiteRT) é **schema de grafo + pesos**,
  otimizado para executar forward, com kernels para o device.

## 2. Escolha por target
| Alvo | Pilha típica | Por quê |
|------|--------------|---------|
| Servidor GPU | ONNX Runtime / TensorRT / vLLM | batch, fp16/fp8, kernels CUDA |
| Edge CPU/NPU | LiteRT (TFLite), ExecuTorch, CoreML | kernels int8, delegates NPU |
| MCU (kB RAM) | TFLite-Micro | quantizado, estático, sem OS |
| LLM local/CPU | GGUF + llama.cpp | mmap, quantização estado-da-arte, sem GPU |
- A pergunta de design: `bytes ~ n_params × bits / 8` — decidida antes do
  runtime pelo orçamento de RAM/to flash.

## 3. Converter e validar A/B
- Sempre reavalie o artefato **pós-conversão** com as mesmas métricas do lab
  (`nt-inf-metrics`) — variações de layout/kernel podem custar pontos de
  acurácia ou acelerar 2×. Documente os dois.

## O que a próxima sala assume
`nt-serving-batching`: dado o formato+runtime escolhido, o problema do servidor
vira *como socar o máximo de tokens/s agregado* — batching contínuo.

## Leituras recomendadas
- [ONNX Runtime docs](https://onnxruntime.ai/docs/)
- [llama.cpp (GGUF)](https://github.com/ggml-org/llama.cpp)
- [ExecuTorch](https://pytorch.org/executorch/)
- [LiteRT](https://ai.google.dev/edge/litert)