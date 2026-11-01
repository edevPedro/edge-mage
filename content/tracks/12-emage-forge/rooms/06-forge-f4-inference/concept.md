# Conceito · Forge F4 — foundation before “rodar o modelo”

## Pré-requisitos

- P6 math: loss/grad/quant literacia (trilhas otimização / ml-math)
- Export/runtime e on-device checklist (`export-runtime`, `on-device` ou ao menos `pf-inference-bridge`)
- F3: mesmo motivo computacional já existe em CPU/GPU

## O que esta etapa ensina

Inferência otimizada não começa no runtime API. Começa em: **o que foi quantizado**, qual o erro aceitável vs golden, e como medir latency/RAM no device/host sem mentir o setup.

CMSIS-NN / LiteRT / ORT são ferramentas; a fundação é layout + numerics + evidência.
