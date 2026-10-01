# Intro assembly (shared)

Assembly is the readable form of machine code: **registers**, **loads/stores**, and control flow (`call` / `ret`, branches).

You do not need to memorize every opcode. You need to **read** a few lines without panic — then map them to ABI rules ([x86-64 psABI](https://gitlab.com/x86-psABIs/x86-64-ABI) or [AAPCS64](https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst)) and to LLVM IR ([LangRef](https://llvm.org/docs/LangRef.html)). Downstream, `llc` emits the dialect your triple asks for ([llc](https://llvm.org/docs/CommandGuide/llc.html)).

**Outside the grimório:** open [Godbolt](https://godbolt.org/), compile a tiny C function, and note whether your host path looks like x86_64 or AArch64. Next bridge: shared `isa-x86-aarch64` (two Godbolt targets). Edge/LLVM deepen AArch64; Systems keeps x86_64 host/RE. Optional pocket map: `riscv-lite`.

`room_id: intro-asm` — single shared credit.
