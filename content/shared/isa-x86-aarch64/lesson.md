# x86_64 vs AArch64 (shared bridge)

One C function → two asm stories. This is the **0–1 strengthen** for x86_64 host literacy and the **bridge** into AArch64 depth — not a third ISA track.

| | **x86_64** | **AArch64** |
|--|------------|-------------|
| Role here | Host PC / many RE samples | Phones, Arm Macs, edge path |
| ABI taste | SysV (Linux): early args `rdi`, `rsi`, … | AAPCS64: early args `x0`… |
| Return (int) | Often `rax` | Often `w0` / `x0` |

**Outside:** Godbolt → same `int add(int a,int b){return a+b;}` → switch target **x86_64** then **aarch64**. Note dialect change; do not chase opcode trivia.

Deep path after this: Systems SysV / `sys-asm-read` (x86 host) · LLVM + Edge `aarch64-abi` (AArch64).

`room_id: isa-x86-aarch64` — shared credit after `intro-asm`.
