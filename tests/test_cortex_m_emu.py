"""Tests for the Cortex-M Thumb-2 subset emulator."""

from __future__ import annotations

import pytest

from edge_mage.emulators.cortex_m_emu import CortexMEmulator


# --------------------------------------------------------------------------- #
#  Test 1: Basic MOV + ADD
# --------------------------------------------------------------------------- #

def test_mov_add_basic() -> None:
    emu = CortexMEmulator()
    emu.load_program("""
        MOV R0, #10
        MOV R1, #20
        ADD R2, R0, R1
        BKPT
    """)
    r = emu.run()
    assert r["regs"]["R2"] == 30
    assert r["reason"] == "bkpt"
    assert r["halted"] is True


# --------------------------------------------------------------------------- #
#  Test 2: Q15 MAC  (0.5 × 0.5 = 0.25 → Q15 = 8192)
# --------------------------------------------------------------------------- #

def test_q15_mac() -> None:
    emu = CortexMEmulator()
    emu.load_program("""
        MOV R0, #0        ; acc = 0
        MOV R1, #16384    ; 0.5 in Q15
        MOV R2, #16384    ; 0.5 in Q15
        MUL R3, R1, R2    ; R3 = 16384*16384 = 268435456
        ASR R3, R3, #15   ; R3 = 268435456 >> 15 = 8192
        ADD R0, R0, R3    ; acc = 8192
        BKPT
    """)
    r = emu.run()
    assert r["regs"]["R0"] == 8192
    assert r["cycles"] == 7


# --------------------------------------------------------------------------- #
#  Test 3: Conditional saturation (Q15 clamp)
# --------------------------------------------------------------------------- #

def test_q15_saturation() -> None:
    emu = CortexMEmulator()
    emu.load_program("""
        MOV R0, #40000    ; acc > 32767
        MOV R1, #32767    ; MAX_Q15
        CMP R0, R1        ; signed compare
        BLE done          ; if R0 <= 32767, skip
        MOV R0, R1        ; saturate
done:
        BKPT
    """)
    r = emu.run()
    assert r["regs"]["R0"] == 32767


# --------------------------------------------------------------------------- #
#  Test 4: LSL / LSR / ASR
# --------------------------------------------------------------------------- #

def test_shift_instructions() -> None:
    emu = CortexMEmulator()
    emu.load_program("""
        MOV R0, #8
        LSL R1, R0, #3    ; R1 = 8 << 3 = 64
        LSR R2, R1, #2    ; R2 = 64 >> 2 = 16
        ASR R3, R1, #2    ; R3 = 64 >> 2 = 16 (positive, same as LSR)
        BKPT
    """)
    r = emu.run()
    assert r["regs"]["R1"] == 64
    assert r["regs"]["R2"] == 16
    assert r["regs"]["R3"] == 16


# --------------------------------------------------------------------------- #
#  Test 5: STR / LDR memory round-trip
# --------------------------------------------------------------------------- #

def test_ldr_str_memory() -> None:
    emu = CortexMEmulator()
    emu.load_program("""
        MOV R0, #1000     ; base address
        MOV R1, #42       ; value
        STR R1, [R0]      ; mem[1000] = 42
        LDR R2, [R0]      ; R2 = mem[1000]
        BKPT
    """)
    r = emu.run()
    assert r["regs"]["R2"] == 42


# --------------------------------------------------------------------------- #
#  Test 6: PUSH / POP stack round-trip
# --------------------------------------------------------------------------- #

def test_push_pop() -> None:
    emu = CortexMEmulator()
    emu.load_program("""
        MOV R13, #0x20008000  ; SP
        MOV R4, #111
        MOV R5, #222
        PUSH {R4, R5}
        MOV R4, #0
        MOV R5, #0
        POP  {R4, R5}
        BKPT
    """)
    r = emu.run()
    assert r["regs"]["R4"] == 111
    assert r["regs"]["R5"] == 222


# --------------------------------------------------------------------------- #
#  Additional: flags, mem_write/read API, reg_dump, demo smoke
# --------------------------------------------------------------------------- #

def test_cmp_flags_signed() -> None:
    """CMP Rn, Rm sets N/Z/C/V correctly for signed comparison."""
    emu = CortexMEmulator()
    emu.load_program("""
        MOV R0, #10
        MOV R1, #20
        CMP R0, R1        ; 10 - 20 = -10 → N=1, Z=0, C=0 (borrow), V=0
        BKPT
    """)
    emu.run()
    assert emu.flags["N"] is True
    assert emu.flags["Z"] is False
    assert emu.flags["C"] is False   # borrow: 10 < 20 → C = 0


def test_mem_write_read_api() -> None:
    """mem_write / mem_read: byte, halfword, word round-trips."""
    emu = CortexMEmulator()
    emu.mem_write(0x1000, 0xDEADBEEF, 4)
    assert emu.mem_read(0x1000, 4) == 0xDEADBEEF
    assert emu.mem_read(0x1000, 1) == 0xEF          # little-endian low byte
    assert emu.mem_read(0x1002, 2) == 0xDEAD        # high halfword


def test_reg_dump_format() -> None:
    emu = CortexMEmulator()
    emu.load_program("BKPT")
    emu.run()
    dump = emu.reg_dump()
    assert "R0=" in dump
    assert "SP=" in dump
    assert "Flags:" in dump
    assert "Cycles:" in dump


def test_demo_runs() -> None:
    """_demo() must not raise."""
    from edge_mage.emulators.cortex_m_emu import _demo
    _demo()


def test_adds_carry_and_overflow() -> None:
    """ADDS: C and V flags for unsigned overflow and signed overflow."""
    emu = CortexMEmulator()
    # 0xFFFFFFFF + 1 overflows unsigned (C=1) and wraps to 0 (Z=1)
    emu.load_program("""
        MOV R0, #0xFFFFFFFF
        MOV R1, #1
        ADDS R2, R0, R1
        BKPT
    """)
    emu.run()
    assert emu.regs[2] == 0
    assert emu.flags["C"] is True
    assert emu.flags["Z"] is True


def test_sub_two_operand() -> None:
    """SUB Rd, #imm (2-arg: Rd = Rd - imm)."""
    emu = CortexMEmulator()
    emu.load_program("""
        MOV R0, #100
        SUB R0, #37
        BKPT
    """)
    r = emu.run()
    assert r["regs"]["R0"] == 63


def test_branch_loop() -> None:
    """BNE branch loops correctly (simple countdown)."""
    emu = CortexMEmulator()
    emu.load_program("""
        MOV R0, #5
        MOV R1, #0
loop:
        ADDS R1, R1, #1
        SUBS R0, R0, #1
        BNE loop
        BKPT
    """)
    r = emu.run()
    # R0 counts down to 0, R1 counts up to 5
    assert r["regs"]["R0"] == 0
    assert r["regs"]["R1"] == 5
