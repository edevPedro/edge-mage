# Intro assembly (shared)

Assembly is the readable form of machine code: **registers**, **loads/stores**, and control flow (`call` / `ret`, branches).

You do not need to memorize every opcode. You need to **read** a few lines without panic — then map them to ABI rules (SysV x86_64 or AAPCS64) and to LLVM IR.

**Outside the grimório:** open [Godbolt](https://godbolt.org/), compile a tiny C function, and note whether your host path looks like x86_64 or AArch64. Edge ML deepens AArch64/NEON later; Systems deepens LLVM IR ↔ asm.

`room_id: intro-asm` — single shared credit.
