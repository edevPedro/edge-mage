"""
ARM Cortex-M Thumb-2 subset emulator for Neurotech BCI firmware labs.

Pedagogical, not QEMU — models the ISA subset used in STM32/nRF/OpenBCI firmware
for Q15 fixed-point DSP, ISR scaffolding, and ring-buffer labs.  Not cycle-accurate.
"""

from __future__ import annotations

import argparse
import ctypes
import re

_MASK32 = 0xFFFF_FFFF
_REG_ALIAS = {"SP": 13, "LR": 14, "PC": 15}
_BRANCHES = {"B", "BEQ", "BNE", "BLT", "BGE", "BGT", "BLE",
             "BCS", "BCC", "BHI", "BLS", "BMI", "BPL", "BL"}


# --------------------------------------------------------------------------- #
#  Helpers
# --------------------------------------------------------------------------- #

def _u32(v: int) -> int:
    return v & _MASK32


def _s32(v: int) -> int:
    return ctypes.c_int32(v & _MASK32).value


def _parse_reg(s: str) -> int:
    s = s.strip().upper()
    if s in _REG_ALIAS:
        return _REG_ALIAS[s]
    m = re.fullmatch(r"R(\d+)", s)
    if m:
        n = int(m.group(1))
        if 0 <= n <= 15:
            return n
    raise ValueError(f"Unknown register: {s!r}")


def _parse_imm(s: str) -> int:
    return int(s.strip().lstrip("#"), 0)


def _parse_reglist(raw: str) -> list[int]:
    raw = raw.strip().strip("{}")
    regs: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        m = re.match(r"(\w+)\s*-\s*(\w+)", part)
        if m:
            regs.extend(range(_parse_reg(m.group(1)), _parse_reg(m.group(2)) + 1))
        else:
            regs.append(_parse_reg(part))
    return sorted(set(regs))


def _split_args(s: str) -> list[str]:
    """Split on commas, skipping commas inside [ ]."""
    args: list[str] = []
    cur = ""
    depth = 0
    for ch in s:
        if ch == "[":
            depth += 1
            cur += ch
        elif ch == "]":
            depth -= 1
            cur += ch
        elif ch == "," and depth == 0:
            args.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        args.append(cur.strip())
    return args


def _parse_mem(args: list[str]) -> tuple[int, int, int | None]:
    """Parse [Rn], [Rn,#imm], [Rn,Rm] → (rn, imm, rm|None)."""
    raw = " ".join(args)
    m = re.match(r"\[\s*(\w+)\s*(?:,\s*([^\]]+))?\s*\]", raw)
    if not m:
        raise ValueError(f"Bad memory operand: {raw!r}")
    rn = _parse_reg(m.group(1))
    if not m.group(2):
        return rn, 0, None
    off = m.group(2).strip()
    if off.startswith("#"):
        return rn, _parse_imm(off), None
    return rn, 0, _parse_reg(off)


# --------------------------------------------------------------------------- #
#  Emulator
# --------------------------------------------------------------------------- #

class CortexMEmulator:
    """
    Cortex-M Thumb-2 subset emulator for BCI firmware labs.

    Registers: R0–R12 (general), R13=SP, R14=LR, R15=PC
    Flags: N, Z, C, V in APSR
    Memory: sparse byte-addressable dict (32-bit aligned recommended)
    NOT a complete ARMv7-M — pedagogical subset for ISR/filter/Q15 labs.
    """

    def __init__(self) -> None:
        self.regs: list[int] = [0] * 16
        self.flags: dict[str, bool] = {"N": False, "Z": False, "C": False, "V": False}
        self.memory: dict[int, int] = {}
        self.halted: bool = False
        self.cycles: int = 0
        self.trace: list[str] = []
        self.pc: int = 0
        self.instructions: list[dict] = []
        self._labels: dict[str, int] = {}

    def reset(self) -> None:
        """Zero registers, flags, pc, cycles. Keeps memory and instructions."""
        self.regs = [0] * 16
        self.flags = {"N": False, "Z": False, "C": False, "V": False}
        self.halted = False
        self.cycles = 0
        self.trace = []
        self.pc = 0

    def load_program(self, asm_text: str) -> None:
        """Parse assembly text, populate self.instructions, reset emulator."""
        instructions: list[dict] = []
        labels: dict[str, int] = {}
        for raw in asm_text.splitlines():
            line = raw.strip()
            if not line or line.startswith(";"):
                continue
            if ";" in line:
                line = line[: line.index(";")].strip()
            if not line:
                continue
            # Inline "label: INSTR"
            lm = re.match(r"^(\w+):\s+(.*)", line)
            if lm:
                labels[lm.group(1).lower()] = len(instructions)
                line = lm.group(2).strip()
            elif line.endswith(":"):
                labels[line[:-1].strip().lower()] = len(instructions)
                continue
            if line:
                instructions.append(self._parse_line(line))
        # Resolve branch labels
        for instr in instructions:
            lbl = instr.get("label")
            if lbl is not None:
                key = lbl.lower()
                if key not in labels:
                    raise ValueError(f"Undefined label: {lbl!r}")
                instr["label_idx"] = labels[key]
        self.instructions = instructions
        self._labels = labels
        self.reset()

    def _parse_line(self, line: str) -> dict:  # noqa: C901
        parts = line.split(None, 1)
        op = parts[0].upper()
        rest = parts[1].strip() if len(parts) > 1 else ""

        if op in ("NOP", "BKPT"):
            return {"op": op}

        if op in _BRANCHES:
            return {"op": op, "label": rest.strip(), "label_idx": None}

        if op == "BX":
            return {"op": op, "rn": _parse_reg(rest.strip())}

        if op in ("PUSH", "POP"):
            m = re.search(r"\{([^}]+)\}", rest)
            if not m:
                raise ValueError(f"Bad reglist: {rest!r}")
            return {"op": op, "regs": _parse_reglist(m.group(0))}

        args = _split_args(rest)

        if op in ("CMP", "CMN", "TST"):
            rn = _parse_reg(args[0])
            if len(args) > 1 and args[1].lstrip().startswith("#"):
                return {"op": op, "rn": rn, "rm": None, "imm": _parse_imm(args[1])}
            return {"op": op, "rn": rn, "rm": _parse_reg(args[1]), "imm": None}

        if op == "SMULL":
            return {"op": op, "rd": _parse_reg(args[0]), "rm": _parse_reg(args[1]),
                    "rn": _parse_reg(args[2]), "rs": _parse_reg(args[3])}

        if op in {"LDR", "STR", "LDRH", "STRH", "LDRB", "STRB", "LDRSH"}:
            rd = _parse_reg(args[0])
            rn, imm, rm = _parse_mem(args[1:])
            return {"op": op, "rd": rd, "rn": rn, "imm": imm, "rm": rm}

        if op in ("LSL", "LSR", "ASR"):
            rd, rn = _parse_reg(args[0]), _parse_reg(args[1])
            if args[2].lstrip().startswith("#"):
                return {"op": op, "rd": rd, "rn": rn, "imm": _parse_imm(args[2]), "rm": None}
            return {"op": op, "rd": rd, "rn": rn, "imm": None, "rm": _parse_reg(args[2])}

        if op in ("SXTH", "SXTB", "UXTH", "UXTB"):
            return {"op": op, "rd": _parse_reg(args[0]), "rn": _parse_reg(args[1])}

        # MOV/MOVS/MVN: source stored in rm for uniform b-operand lookup
        if op in ("MOV", "MOVS", "MVN"):
            rd = _parse_reg(args[0])
            if args[1].lstrip().startswith("#"):
                return {"op": op, "rd": rd, "rn": None, "rm": None, "imm": _parse_imm(args[1])}
            return {"op": op, "rd": rd, "rn": None, "rm": _parse_reg(args[1]), "imm": None}

        if op == "RSBS":
            return {"op": op, "rd": _parse_reg(args[0]),
                    "rn": _parse_reg(args[1]), "imm": _parse_imm(args[2])}

        if op in ("ADD", "ADDS", "SUB", "SUBS"):
            rd = _parse_reg(args[0])
            rn, src = (rd, args[1]) if len(args) == 2 else (_parse_reg(args[1]), args[2])
            if src.lstrip().startswith("#"):
                return {"op": op, "rd": rd, "rn": rn, "rm": None, "imm": _parse_imm(src)}
            return {"op": op, "rd": rd, "rn": rn, "rm": _parse_reg(src), "imm": None}

        if op == "MUL":
            return {"op": op, "rd": _parse_reg(args[0]),
                    "rn": _parse_reg(args[1]), "rm": _parse_reg(args[2]), "imm": None}

        if op in ("AND", "ORR", "EOR", "BIC"):
            rd, rn = _parse_reg(args[0]), _parse_reg(args[1])
            if len(args) > 2:
                return {"op": op, "rd": rd, "rn": rn, "rm": _parse_reg(args[2]), "imm": None}
            return {"op": op, "rd": rd, "rn": rd, "rm": rn, "imm": None}

        raise ValueError(f"Unknown instruction: {op!r}")

    # ------------------------------------------------------------------ flags

    def _nz(self, v: int) -> None:
        v32 = _u32(v)
        self.flags["N"] = bool(v32 >> 31)
        self.flags["Z"] = v32 == 0

    def _add_flags(self, a: int, b: int, res: int) -> None:
        r32 = _u32(res)
        self.flags["N"] = bool(r32 >> 31)
        self.flags["Z"] = r32 == 0
        self.flags["C"] = (a + b) > _MASK32
        self.flags["V"] = bool((_u32(a) ^ r32) & (_u32(b) ^ r32) & 0x8000_0000)

    def _sub_flags(self, a: int, b: int, res: int) -> None:
        r32 = _u32(res)
        self.flags["N"] = bool(r32 >> 31)
        self.flags["Z"] = r32 == 0
        self.flags["C"] = _u32(a) >= _u32(b)   # C = NOT borrow
        self.flags["V"] = bool((_u32(a) ^ _u32(b)) & (_u32(a) ^ r32) & 0x8000_0000)

    # ------------------------------------------------------------------ step

    def step(self) -> bool:
        """Execute one instruction. Returns True if not halted."""
        if self.halted or self.pc >= len(self.instructions):
            return False
        instr = self.instructions[self.pc]
        self.pc += 1
        self.cycles += 1
        try:
            self._exec(instr)
        except Exception as exc:
            self.halted = True
            self._log(f"ERROR @{self.pc - 1}: {exc}")
        return not self.halted

    def _exec(self, i: dict) -> None:  # noqa: C901
        op = i["op"]
        R = self.regs
        F = self.flags
        rd = i.get("rd")
        rn = i.get("rn")
        rm = i.get("rm")
        imm = i.get("imm")

        def rv(n: int | None) -> int:
            return R[n] if n is not None else 0

        # Precompute operands for data-processing instructions
        a = rv(rn)
        b = rv(rm) if rm is not None else (imm if imm is not None else 0)

        self._log(f"[{self.pc - 1:3d}] {op}")

        match op:
            case "MOV":
                R[rd] = _u32(b)
            case "MOVS":
                R[rd] = _u32(b)
                self._nz(b)
            case "MVN":
                R[rd] = _u32(~b)
            case "ADD":
                R[rd] = _u32(a + b)
            case "ADDS":
                res = a + b
                R[rd] = _u32(res)
                self._add_flags(a, b, res)
            case "SUB":
                R[rd] = _u32(a - b)
            case "SUBS":
                res = a - b
                R[rd] = _u32(res)
                self._sub_flags(a, b, res)
            case "RSBS":
                res = imm - a
                R[rd] = _u32(res)
                self._sub_flags(imm, a, res)
            case "MUL":
                R[rd] = _u32(_s32(a) * _s32(b))
            case "SMULL":
                prod = _s32(a) * _s32(rv(i["rs"]))
                R[rd] = _u32(prod)
                R[rm] = _u32(prod >> 32)
            case "AND":
                R[rd] = _u32(a & b)
            case "ORR":
                R[rd] = _u32(a | b)
            case "EOR":
                R[rd] = _u32(a ^ b)
            case "BIC":
                R[rd] = _u32(a & ~b)
            case "LSL":
                R[rd] = _u32(a << b) if b < 32 else 0
            case "LSR":
                R[rd] = (a >> b) if b < 32 else 0
            case "ASR":
                R[rd] = _u32(_s32(a) >> min(b, 31))
            case "CMP":
                self._sub_flags(a, b, a - b)
            case "CMN":
                self._add_flags(a, b, a + b)
            case "TST":
                r32 = _u32(a & b)
                F["N"] = bool(r32 >> 31)
                F["Z"] = r32 == 0
            case "SXTH":
                R[rd] = _u32(ctypes.c_int16(rv(rn) & 0xFFFF).value)
            case "SXTB":
                R[rd] = _u32(ctypes.c_int8(rv(rn) & 0xFF).value)
            case "UXTH":
                R[rd] = rv(rn) & 0xFFFF
            case "UXTB":
                R[rd] = rv(rn) & 0xFF
            case "LDR":
                R[rd] = self.mem_read(_u32(a + b), 4)
            case "STR":
                self.mem_write(_u32(a + b), R[rd], 4)
            case "LDRH":
                R[rd] = self.mem_read(_u32(a + b), 2)
            case "STRH":
                self.mem_write(_u32(a + b), R[rd], 2)
            case "LDRB":
                R[rd] = self.mem_read(_u32(a + b), 1)
            case "STRB":
                self.mem_write(_u32(a + b), R[rd], 1)
            case "LDRSH":
                R[rd] = _u32(ctypes.c_int16(self.mem_read(_u32(a + b), 2) & 0xFFFF).value)
            case "B":
                self.pc = i["label_idx"]
            case "BEQ":
                if F["Z"]: self.pc = i["label_idx"]
            case "BNE":
                if not F["Z"]: self.pc = i["label_idx"]
            case "BLT":
                if F["N"] != F["V"]: self.pc = i["label_idx"]
            case "BGE":
                if F["N"] == F["V"]: self.pc = i["label_idx"]
            case "BGT":
                if not F["Z"] and F["N"] == F["V"]: self.pc = i["label_idx"]
            case "BLE":
                if F["Z"] or F["N"] != F["V"]: self.pc = i["label_idx"]
            case "BCS":
                if F["C"]: self.pc = i["label_idx"]
            case "BCC":
                if not F["C"]: self.pc = i["label_idx"]
            case "BHI":
                if F["C"] and not F["Z"]: self.pc = i["label_idx"]
            case "BLS":
                if not F["C"] or F["Z"]: self.pc = i["label_idx"]
            case "BMI":
                if F["N"]: self.pc = i["label_idx"]
            case "BPL":
                if not F["N"]: self.pc = i["label_idx"]
            case "BL":
                R[14] = self.pc   # LR = return address (next instruction index)
                self.pc = i["label_idx"]
            case "BX":
                self.pc = R[i["rn"]]   # symbolic: treat reg value as instruction index
            case "PUSH":
                regs = i["regs"]
                R[13] = _u32(R[13] - 4 * len(regs))
                for idx, reg in enumerate(regs):   # lowest-numbered reg at lowest address
                    self.mem_write(_u32(R[13] + 4 * idx), R[reg], 4)
            case "POP":
                regs = i["regs"]
                for idx, reg in enumerate(regs):
                    R[reg] = self.mem_read(_u32(R[13] + 4 * idx), 4)
                R[13] = _u32(R[13] + 4 * len(regs))
            case "NOP":
                pass
            case "BKPT":
                self.halted = True
            case _:
                raise ValueError(f"Unimplemented instruction: {op!r}")

    def _log(self, msg: str) -> None:
        self.trace.append(msg)
        if len(self.trace) > 64:
            self.trace.pop(0)

    # ---------------------------------------------------------------- run/io

    def run(self, max_cycles: int = 500) -> dict:
        """Execute until BKPT/halt or max_cycles. Returns result dict."""
        reason = "max_cycles"
        while self.cycles < max_cycles:
            if not self.step():
                reason = "bkpt" if self.halted else "error"
                break
        return {
            "cycles": self.cycles,
            "halted": self.halted,
            "regs": {**{f"R{i}": self.regs[i] for i in range(13)},
                     "SP": self.regs[13], "LR": self.regs[14], "PC": self.pc},
            "flags": dict(self.flags),
            "trace": list(self.trace),
            "reason": reason,
        }

    def reg_dump(self) -> str:
        """Human-readable register and flag state."""
        R = self.regs
        F = self.flags
        row0 = "  ".join(f"R{i}=0x{R[i]:08X}" for i in range(4))
        row1 = "  ".join(f"R{i}=0x{R[i]:08X}" for i in range(4, 8))
        row2 = f"SP=0x{R[13]:08X}  LR=0x{R[14]:08X}  PC={self.pc}"
        nzvc = " ".join(f"{k}={int(v)}" for k, v in F.items())
        return "\n".join([row0, row1, row2, f"Flags: {nzvc}   Cycles: {self.cycles}"])

    def mem_write(self, addr: int, value: int, size: int = 4) -> None:
        """Write 1/2/4 bytes little-endian to sparse memory."""
        for i in range(size):
            self.memory[addr + i] = (value >> (8 * i)) & 0xFF

    def mem_read(self, addr: int, size: int = 4, signed: bool = False) -> int:
        """Read 1/2/4 bytes little-endian from sparse memory."""
        v = 0
        for i in range(size):
            v |= self.memory.get(addr + i, 0) << (8 * i)
        if signed:
            if size == 4:
                v = _s32(v)
            elif size == 2:
                v = ctypes.c_int16(v & 0xFFFF).value
            elif size == 1:
                v = ctypes.c_int8(v & 0xFF).value
        return v


# --------------------------------------------------------------------------- #
#  Demo / CLI
# --------------------------------------------------------------------------- #

def _demo() -> None:
    print("cortex_m_emu demo (Cortex-M Thumb-2 subset — pedagogical, not QEMU)")
    print("  ISA: ARM Thumb-2 subset (~30 instructions) | target: Cortex-M0/M3/M4 class")
    print()

    # ---- Demo 1: Q15 MAC (0.5 * 0.5 = 0.25 → Q15 = 8192) ----
    print("[Demo 1: Q15 MAC]")
    emu = CortexMEmulator()
    emu.load_program("""
        MOV R0, #0        ; acc = 0
        MOV R1, #16384    ; 0.5 in Q15
        MOV R2, #16384    ; 0.5 in Q15
        MUL R3, R1, R2    ; R3 = 268435456
        ASR R3, R3, #15   ; R3 = 8192  (Q15 shift)
        ADD R0, R0, R3    ; acc = 8192
        BKPT
    """)
    r = emu.run()
    prog = "MOV R0,#0 | MOV R1,#16384 | MOV R2,#16384 | MUL R3,R1,R2 | ASR R3,R3,#15 | ADD R0,R0,R3 | BKPT"
    print(f"  Program: {prog}")
    print(f"  Result: R0={r['regs']['R0']} (= 0.25 in Q15 = 0.5*0.5 \u2713)")
    for line in emu.reg_dump().splitlines():
        print(f"  {line}")
    print()

    # ---- Demo 2: Q15 Conditional Saturation ----
    print("[Demo 2: Q15 Conditional Saturation]")
    emu2 = CortexMEmulator()
    emu2.load_program("""
        MOV R0, #40000    ; acc > 32767
        MOV R1, #32767    ; MAX_Q15
        CMP R0, R1        ; compare signed
        BLE done          ; skip if already <= max
        MOV R0, R1        ; saturate
done:
        BKPT
    """)
    r2 = emu2.run()
    print(f"  R0={r2['regs']['R0']} (saturated \u2713)   Cycles: {r2['cycles']}")
    print()

    # ---- Demo 3: Ring buffer STR + LDR ----
    print("[Demo 3: Ring buffer write (STR) + read (LDR)]")
    emu3 = CortexMEmulator()
    emu3.load_program("""
        MOV R0, #0x200    ; base address
        MOV R1, #99       ; value to store
        STR R1, [R0]      ; mem[0x200] = 99
        LDR R2, [R0]      ; R2 = mem[0x200]
        BKPT
    """)
    r3 = emu3.run()
    print(f"  mem[0x200] = 99 \u2192 LDR \u2192 R2={r3['regs']['R2']} \u2713   Cycles: {r3['cycles']}")
    print()

    print("Note: AArch64 (64-bit) is for edge ML hosts (RPi 4, Apple Silicon).")
    print("      Real BCI acquisition firmware runs on Cortex-M (this emulator's target).")
    print("      Bridge to AArch64: see nt-fw-aarch64-bridge and Edge ML track.")


def main(argv: list[str] | None = None) -> None:
    """CLI: mage emu cortex-m"""
    argparse.ArgumentParser(
        description="Cortex-M Thumb-2 subset emulator (pedagogical, not QEMU)"
    ).parse_args(argv)
    _demo()


if __name__ == "__main__":
    main()
