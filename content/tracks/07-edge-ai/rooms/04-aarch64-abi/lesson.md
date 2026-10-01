# AArch64 ABI on the edge

On-device ML kernels live on **AArch64** calling conventions and often **Advanced SIMD (NEON)** — or, on Cortex-M, the sibling story of DSP/MVE + CMSIS-NN.

## Why this room exists

Systems / LLVM tracks deepen frames, MIR, and `llc`. Edge still needs a **device-facing** pass: which registers the ABI promises, why stack alignment matters for arena buffers, and why **16 int8 lanes** show up in kernel design.

## AAPCS64 — what you must own

Primary source: [AAPCS64 (`aapcs64.rst` in abi-aa)](https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst).

| Topic | Rule of thumb |
|-------|----------------|
| Integer / pointer args | `x0`…`x7`, then stack |
| Integer result | `x0` / `w0` |
| Indirect result | address in `x8` |
| Stack | **16-byte** aligned at public interfaces |
| Callee-saved GPR | `x19`–`x28` (preserve across calls) |
| Frame / link | `x29` FP, `x30` LR when used as such |

If you smash a callee-saved register in a hand-written NEON stub without saving it, you corrupt the caller — golden tests become ghost hunts.

## Advanced SIMD lanes

A 128-bit vector Q register holds **16×int8**. That is why int8 matmul tiles talk about 16-wide packs. Intrinsics live in the [Arm Neon Intrinsics Reference](https://developer.arm.com/architectures/instruction-sets/intrinsics/). Instruction semantics: [Arm Architecture Reference Manual (DDI0487)](https://developer.arm.com/documentation/ddi0487/latest).

## Toolchain adjacency (do not duplicate Systems)

LLVM’s [CodeGenerator](https://llvm.org/docs/CodeGenerator.html) is how compilers emit prologues that obey AAPCS64. Edge Mage does **not** re-teach TableGen — it demands you recognize the ABI the compiler already assumed.

## Outside the grimório

1. Open AAPCS64 — confirm callee-saved set and `x8` indirect result.
2. Godbolt `aarch64-linux-gnu`: tiny C function with 9 integer args — find the 9th on the stack.
3. One study-log sentence: ABI register pressure → why int8 kernels care about lane count and saved regs.
