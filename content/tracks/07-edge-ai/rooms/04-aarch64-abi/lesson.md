# AArch64 ABI on the edge

On-device ML kernels live on **AArch64** calling conventions and often **NEON** SIMD.

## Why this room exists

Systems Mage covers AAPCS64 in the LLVM track. Edge still needs a **device-facing** pass: return registers, 16-byte stack alignment, and int8 lane math for quantized matmul.

## Outside the grimório

1. Skim [AAPCS64](https://github.com/ARM-software/abi-aa/releases) — focus on argument / result registers.
2. Glance at Neon intrinsics for `int8x16_t` style types.
3. Write one sentence in your study log linking ABI choice → why int8 kernels care about lane count.
