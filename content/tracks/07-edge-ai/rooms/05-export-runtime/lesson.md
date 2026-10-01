# Export & Runtime — treino → device

Esta sala fecha o buraco entre “sei softmax” e “rodo no telefone”.

## PyTorch path (oficial)

1. Treine / congele pesos.
2. `torch.export.export(model, example_inputs)` — grafo estável ([docs](https://pytorch.org/docs/stable/export.html)).
3. Para ONNX: `torch.onnx.export(...)` (exporterador baseado em `torch.export` no PyTorch recente) — [onnx.html](https://pytorch.org/docs/stable/onnx.html).
4. Para edge nativo PyTorch: **ExecuTorch** → artefato `.pte` — [Getting Started](https://pytorch.org/executorch/stable/getting-started.html).

## TensorFlow / LiteRT path

Converter SavedModel/Keras com `tf.lite.TFLiteConverter`; runtime moderno documentado como **LiteRT** — [overview](https://ai.google.dev/edge/litert/overview).

## Quant no meio

PTQ/QAT entram **depois** (ou durante) o export, conforme o backend (ORT, PT2E, TFLite quant). Sem calibração, int8 mentiroso.

## Golden

Compare float vs quantizado / host vs device nos mesmos inputs. Sem isso, o checklist on-device é teatro.
