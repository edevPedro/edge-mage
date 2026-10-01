# RISC-V at a glance (lite elective)

Open-ISA **literacy** — **not** a second LLVM track, **not** equal depth to AArch64.

## Teach (minimum)

1. **Load/store** — ALU stays in registers; memory via `lw`/`sw` (and friends). Same mental model as AArch64.
2. **`x0` = zero** — hardwired; dumps look weird until you know this.
3. **ABI taste** — psABI: integer args in `a0`–`a7` (`x10`–`x17`), return in `a0`. Contrast with AAPCS64 (`x0`–`x7` / `x0`) — same *idea*, different *names*.

## Do not teach here

- Privileged / supervisor / hypervisor manuals  
- Vector (`V`) / crypto / full extension zoo  
- Building a core, Chisel, or FPGA bring-up  
- Memorizing both ABIs cold — **deep path stays AArch64 (Edge / BCI)**

## Outside the grimório

1. Skim [Unprivileged ISA](https://docs.riscv.org/reference/isa/v20260120/unpriv/unpriv-index.html) overview (registers + load/store).  
2. Peek [psABI](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/) § integer register convention.  
3. Godbolt **rv64** *or* [RARS](https://github.com/TheThirdOne/rars) on a leaf `add`.  
4. Return to **AArch64** for frames / NEON / CMSIS-NN / on-device.

`room_id: riscv-lite` — elective; **not** required for Mago base or Edge Mage.
