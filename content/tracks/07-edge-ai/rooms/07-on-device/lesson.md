# On-Device Checklist

Antes de chamar a si mesmo Edge Mage, o binário precisa sobreviver ao mundo real — com fontes oficiais no banco, não marketing.

## Orçamento

RAM, flash, potência (mW), latência (ms), térmica. Sem orçamento, não há deploy — só demo.

## Runtime (escolheu na sala Export)

| Caminho | Docs oficiais |
|---------|----------------|
| PyTorch → ExecuTorch | https://pytorch.org/executorch/stable/getting-started.html |
| TF / AI Edge → LiteRT Micro | https://developers.google.com/edge/litert/microcontrollers/get_started |
| ONNX → ORT Mobile | https://onnxruntime.ai/docs/tutorials/mobile/ |
| Kernels Arm int8 | https://arm-software.github.io/CMSIS-NN/latest/ |

## Arena (MCU)

[TFLM memory management](https://github.com/tensorflow/tflite-micro/blob/main/tensorflow/lite/micro/docs/memory_management.md): **tensor arena** (head / temporary / tail) no lugar de malloc no hot path.

## Ops, CMSIS-NN, Ethos-U

Unsupported ops → **CPU fallback**. Cortex-M: [CMSIS-NN](https://arm-software.github.io/CMSIS-NN/latest/) + [ML Dev Guide 109267](https://developer.arm.com/documentation/109267/latest/).

## Golden tests

Compare float vs int8 / host vs device on fixed inputs. Regressão silenciosa é o boss final.

## Pipeline

Sensor → pré → inferência → pós → ato. O modelo é só o miolo.
