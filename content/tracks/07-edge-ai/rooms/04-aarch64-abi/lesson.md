# AArch64 ABI on the edge

On-device ML kernels live on **AArch64** calling conventions and often **NEON** SIMD.

## Why this room exists

Systems Mage covers AAPCS64 in the LLVM track. Edge still needs a **device-facing** pass: return registers, 16-byte stack alignment, and int8 lane math for quantized matmul.

## Outside the grimório

1. Read [AAPCS64](https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst) — integer/pointer args in `x0`–`x7`, result in `x0`/`w0`; FP/SIMD args in `v0`–`v7`; SP 16-byte aligned at call boundaries.
2. Skim Arm Neon intrinsics for `int8x16_t` style types ([Arm Neon Intrinsics Reference](https://developer.arm.com/architectures/instruction-sets/intrinsics/)).
3. Write one sentence in your study log linking ABI choice → why int8 kernels care about lane count.
