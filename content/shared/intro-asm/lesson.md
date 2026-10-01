# Intro assembly (shared)

Assembly is the readable form of machine code: **registers**, **loads/stores**, and control flow (`call` / `ret`, branches).

You do not need to memorize every opcode. You need to **read** a few lines without panic — then map them to an ABI and (later) to LLVM IR ([LangRef](https://llvm.org/docs/LangRef.html)). Downstream, `llc` emits the dialect your triple asks for ([llc](https://llvm.org/docs/CommandGuide/llc.html)).

## Primary path (e-mage)

**AArch64** is the deep track for Edge ML / BCI / on-device: learn the *ideas* here, then deepen with [AAPCS64](https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst) and Edge `aarch64-abi` (plus Arm [A64 overview](https://developer.arm.com/documentation/102374/0101/Overview) · [DDI0487](https://developer.arm.com/documentation/ddi0487/latest)).

## Literacy only (do not go deep here)

- **x86_64** — common host / RE dialect; [x86-64 psABI](https://gitlab.com/x86-psABIs/x86-64-ABI). One glance room: `isa-x86-aarch64`.
- **RISC-V** — open-ISA pocket map; elective `riscv-lite` (optional).

Systems Mage keeps x86_64 for host/RE labs. It is **not** a multi-ISA tour equal to ARM depth.

**Outside the grimório:** open [Godbolt](https://godbolt.org/), compile a tiny C function. Prefer reading an **aarch64** target if you can; note x86_64 only so host dumps are not alien.

`room_id: intro-asm` — single shared credit.
