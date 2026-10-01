# CMSIS-NN & integer kernels

On Cortex-M, “quantized model” only helps if kernels exist that match the **integer contract** of the runtime (LiteRT / TFLM). **CMSIS-NN** is Arm’s maintained library of those kernels.

## What the official docs claim

From the [CMSIS-NN user manual](https://arm-software.github.io/CMSIS-NN/latest/):

- Efficient NN kernels for **Cortex-M**, with implementations selected by features: no-SIMD, **DSP**, **MVE (Helium)**.
- Integer path follows **int8 / int16** as specified for **TensorFlow Lite for Microcontrollers** (LiteRT Micro family).
- Categories include convolution, fully-connected, pooling, softmax, LSTM, elementwise, …

For **Cortex-A / AArch64** phones and SBCs, the same docs steer you away from treating CMSIS-NN float as the A-class solution — prefer **Arm Compute Library** / **XNNPACK**-class stacks. Edge Mage still needs the Cortex-M contract: most MCU deployments wire TFLM → CMSIS-NN.

## Quant contract (LiteRT 8-bit)

Primary product spec: [LiteRT 8-bit quantization specification](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec).

Affine dequant: `real = (q − zero_point) · scale`.

Typical constraints you must not hand-wave:

- Activations / many tensors: int8 in **[−128, 127]**
- Weights for several CONV/FC ops: int8 in **[−127, 127]** with **zero_point = 0** (symmetric weights)
- Bias often **int32** with scale ≈ `input_scale * weight_scale`

Jacob et al. (arXiv:1712.05877) is the academic ancestor; the LiteRT spec is what silicon/kernels implement today.

## Link to AArch64 / NEON

`aarch64-abi` taught **16×int8** in a 128-bit NEON vector. CMSIS-NN / Helium use the same idea on M-profile: lane math + requantization after wide accumulators. Without matching scales/zero-points, golden tests fail even if FLOPs look fine.

## Outside the grimório

1. Skim CMSIS-NN “Quantization Specification” + one convolution API page.
2. Skim LiteRT 8-bit spec for CONV_2D / FULLY_CONNECTED.
3. Note one sentence in your study log: *which* runtime (TFLM + CMSIS-NN vs ACL) fits your target CPU class.
