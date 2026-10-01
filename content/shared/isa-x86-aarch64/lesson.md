# Other ISAs at a glance — x86_64 vs AArch64

**One comparison room.** Literacy for the desktop host dialect — **not** a second deep track.

| | **x86_64** (literacy) | **AArch64** (deep path) |
|--|----------------------|-------------------------|
| Role here | PC host / many RE samples | Phones, Arm Macs, edge / BCI |
| ABI taste | SysV (Linux): early args `rdi`, `rsi`, … | AAPCS64: early args `x0`…`x7` |
| Return (int) | Often `rax` | Often `w0` / `x0` |
| Why edge often ≠ desktop | Fat OoO cores, huge caches, power budget of a wall outlet | Power / area / thermal → fixed-point, NEON lanes, CMSIS-NN |

**Outside:** Godbolt → same `int add(int a,int b){return a+b;}` → switch target **x86_64** then **aarch64**. Spot register-name change; stop. No opcode farm.

Primaries: [x86-64 psABI](https://gitlab.com/x86-psABIs/x86-64-ABI) · [Intel SDM](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) (overview only) · [AAPCS64](https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst) · [DDI0487](https://developer.arm.com/documentation/ddi0487/latest).

After this: Systems SysV / `sys-asm-read` (x86 host work) · **Edge `aarch64-abi` + CMSIS-NN** (real depth). Optional pocket map: `riscv-lite`.

`room_id: isa-x86-aarch64` — shared credit after `intro-asm`.
