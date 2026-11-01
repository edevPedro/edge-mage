# AUDIT — e-mage Deep Curriculum Engineering

**Date:** 2026-11-01  
**Scope:** Full audit of e-mage single-track journey per SPEC-emage-single-track.md  
**Purpose:** Room-by-room quality assessment, gap identification, and improvement prioritization for Performance Engineering & Hardware Acceleration specialization.

---

## Executive Summary

The e-mage repository implements a single continuous journey (P0–P7 + Forge + Neurotech branch) with 157 room.yaml files across 12 tracks. The architecture is sound, but content depth varies significantly. Key findings:

| Metric | Count | Notes |
|--------|-------|-------|
| Total rooms | 157 | Across all tracks |
| Performance track | 20 | P2–P7 spine |
| Edge AI track | 13 | P6 inference |
| Forge track | 7 | Cumulative project |
| Neurotech track | 89 | Optional branch |
| Systems pack | 82 | P1 FLAG rooms |
| Shared/Fundamentals | ~10 | P0 core |

**Overall Assessment:** Solid architecture with real pedagogical progression. Many rooms have adequate concept.md but need deeper lesson.md and practical exercises. The Forge project exists as scaffold but lacks concrete implementation guidance.

---

## 1. Phase-by-Phase Audit

### P0 — Fundamentals

**Tracks:** `content/courses/fundamentals/`, `content/shared/`

| Room ID | Status | Concept | Lesson | Exercises | Notes |
|---------|--------|---------|--------|-----------|-------|
| `vectors` | Sólida | ✓ Magnitude/dot/ortho | ✓ Short | ✓ Numeric + code | Good foundation, links to 3B1B |
| `bits` | Sólida | ✓ Two's complement | ✓ Short | ✓ Basic | Good LLVM IR connection |
| `trig-waves` | Precisa aprofundamento | ✓ Basic | — | — | Missing implementation exercises |
| `intro-asm` | Sólida | ✓ Deep path = AArch64 | ✓ Godbolt | — | Good ISA scoping |
| `isa-x86-aarch64` | Sólida | ✓ Literacy focus | ✓ Compare | — | Appropriate glance room |
| `riscv-lite` | Sólida | ✓ Load/store + psABI | — | — | Optional, well-scoped |
| `fundamentals-clear` | Sólida | — | ✓ Gate | ✓ MCQ | Proper Mago base gate |

**Gap Analysis P0:**
- Missing: Data representation (IEEE 754 intro before P4 depth)
- Missing: Development toolchain room (make, cmake, compiler flags)
- Weak: `trig-waves` needs code exercises for DSP foundation

**Recommendation:** Keep P0 light since target audience has C++ experience. Add placement quiz to fast-track appropriately.

---

### P1 — Systems Craft

**Source:** `content/packs/systems.json` (82 rooms across systems/llvm/math tracks)

| Phase | Rooms | Focus | Status |
|-------|-------|-------|--------|
| s0 | 3 | Memory (stack/heap/data) | Sólida — FLAG labs |
| s1 | 4 | Pointers, arrays, aliasing | Sólida |
| s2 | 6 | ABI, calling conventions | Sólida |
| f0 | 10 | LLVM IR fundamentals | Sólida — real IR exercises |
| f1 | 12 | Optimization passes | Sólida |
| f2 | 13 | Code generation | Precisa aprofundamento |
| f3 | 6 | Advanced IR | Sólida |
| f4 | 8 | Analysis passes | Sólida |
| f5 | 18 | Advanced topics | Scaffold |
| f6 | 2 | Capstone | Scaffold |

**Strengths:**
- FLAG lab format with `FLAG{...}` checkpoints provides real engagement
- LLVM IR literacy is deep and practical
- Links to official LLVM documentation

**Gap Analysis P1:**
- Missing: Explicit undefined behavior (UB) room with examples
- Missing: C++ object lifetime and move semantics depth
- Missing: ELF structure deep dive (nm, objdump, readelf labs)
- Missing: Linker/loader mechanics
- Weak: Concurrency and atomics (memory_order, acquire/release)
- Weak: Compiler pipeline visualization

**Priority Improvements:**
1. Add `sys-ub-lifetime` room: UB categories, lifetime, aliasing rules
2. Add `sys-elf-deep` room: ELF sections, symbols, relocations
3. Add `sys-linker-loader` room: Static/dynamic linking, PLT/GOT
4. Add `sys-atomics` room: Memory ordering, lock-free patterns

---

### P2 — CPU Architecture & Memory

**Track:** `content/tracks/11-performance/` (rooms 01-04)

| Room ID | Status | Concept Depth | Exercises | Missing |
|---------|--------|---------------|-----------|---------|
| `pf-portal` | Sólida | ✓ Map + M4 caveats | ✓ MCQ | — |
| `pf-pipeline` | Precisa aprofundamento | ✓ Hazards basic | ✓ MCQ | OoO execution, superscalar |
| `pf-cache-vm` | Precisa aprofundamento | ✓ Hierarchy basic | ✓ MCQ | TLB details, prefetch |
| `pf-aarch64-perf` | Precisa aprofundamento | ✓ Load/store bound | ✓ MCQ | Apple µarch specifics |

**Gap Analysis P2:**
- Missing: CPU pipeline deep dive (fetch/decode/execute/memory/writeback)
- Missing: Superscalar and out-of-order execution mechanics
- Missing: Branch prediction (BTB, pattern history)
- Missing: Instruction-level parallelism analysis
- Missing: Cache line experiments (false sharing lab)
- Missing: TLB and huge pages practical
- Missing: Memory bandwidth measurement lab
- Missing: Apple Silicon M-series specific characteristics

**Priority Improvements:**
1. Expand `pf-pipeline`: Add OoO execution, register renaming, ROB
2. Add `pf-cache-lab` room: Empirical cache measurement experiments
3. Add `pf-branch-pred` room: Branch prediction patterns
4. Add `pf-m4-microarch` room: Apple Silicon specifics vs Cortex-A

---

### P3 — SIMD / ARM Performance

**Track:** `content/tracks/11-performance/` (rooms 05-08)

| Room ID | Status | Concept Depth | Exercises | Missing |
|---------|--------|---------------|-----------|---------|
| `pf-neon-intro` | Sólida | ✓ NEON vs autovec | ✓ MCQ | Code exercises |
| `pf-simd-tiling` | Precisa aprofundamento | ✓ SoA/AoS basic | ✓ MCQ | Practical tiling |
| `pf-counters` | Sólida | ✓ Measurement ritual | ✓ MCQ | Instruments lab |
| `pf-boss-arm-math` | Precisa reestruturação | ✓ Boss template | ✓ MCQ | Harness code |

**Gap Analysis P3:**
- Missing: NEON intrinsics practical guide (vld1q, vmulq, vaddq patterns)
- Missing: Auto-vectorization analysis (checking compiler output)
- Missing: Loop unrolling mechanics and when to apply
- Missing: Data alignment requirements and impact
- Missing: LLVM vectorizer behavior and pragmas
- Missing: Hardware counter usage on macOS (Instruments tutorial)
- Missing: Benchmarking methodology (warm-up, noise, statistical analysis)

**Priority Improvements:**
1. Add `pf-neon-intrinsics` room: Practical intrinsics patterns
2. Add `pf-autovec-check` room: Analyzing vectorizer decisions
3. Expand `pf-boss-arm-math`: Provide starter harness repo structure

---

### P4 — Numerical Computing / HPC

**Track:** `content/tracks/11-performance/` (rooms 09-12)

| Room ID | Status | Concept Depth | Exercises | Missing |
|---------|--------|---------------|-----------|---------|
| `pf-nla-ieee` | Precisa aprofundamento | ✓ IEEE754 basic | ✓ MCQ | Error analysis |
| `pf-roofline` | Precisa aprofundamento | ✓ Model basic | ✓ MCQ | Practical plotting |
| `pf-gemm-jacobi` | Precisa aprofundamento | ✓ Kernels named | ✓ MCQ | Implementation |
| `pf-boss-physics` | Precisa reestruturação | ✓ Boss template | ✓ MCQ | Harness code |

**Gap Analysis P4:**
- Missing: IEEE 754 deep dive (denormals, rounding modes, error propagation)
- Missing: Numerical stability analysis techniques
- Missing: Error accumulation in iterative algorithms
- Missing: GEMM tiling implementation guide
- Missing: Jacobi/heat equation practical implementation
- Missing: Roofline model construction lab (measure peak FLOPS/bandwidth)
- Missing: OpenMP basics for CPU parallelization
- Missing: Compute-bound vs memory-bound classification exercises

**Priority Improvements:**
1. Expand `pf-nla-ieee`: Add error analysis, numerical stability
2. Add `pf-roofline-lab` room: Build actual Roofline plot for M4
3. Add `pf-gemm-impl` room: Step-by-step tiled GEMM
4. Add `pf-openmp-intro` room: Basic parallel patterns

---

### P5 — GPU (Metal)

**Track:** `content/tracks/11-performance/` (rooms 13-16)

| Room ID | Status | Concept Depth | Exercises | Missing |
|---------|--------|---------------|-----------|---------|
| `pf-metal-intro` | Sólida | ✓ Metal model | ✓ MCQ | Code example |
| `pf-gpu-kernels` | Precisa aprofundamento | ✓ Brief | ✓ MCQ | Kernel patterns |
| `pf-cuda-elective` | Sólida | ✓ Literacy only | ✓ MCQ | — |
| `pf-boss-metal` | Precisa reestruturação | ✓ Boss template | ✓ MCQ | Harness code |

**Gap Analysis P5:**
- Missing: GPU architecture fundamentals (SIMT, warps/wavefronts, occupancy)
- Missing: GPU memory hierarchy (registers, shared/threadgroup, global)
- Missing: Memory coalescing patterns
- Missing: Metal Shading Language tutorial
- Missing: Metal compute shader examples
- Missing: GPU profiling with Instruments
- Missing: Kernel fusion concepts
- Missing: CPU/GPU execution overlap

**Priority Improvements:**
1. Add `pf-gpu-arch` room: GPU execution model fundamentals
2. Add `pf-msl-intro` room: Metal Shading Language basics
3. Add `pf-metal-compute` room: First compute shader walkthrough
4. Expand `pf-boss-metal`: Provide Metal project template

---

### P6 — Inference Optimization

**Tracks:** `content/tracks/07-edge-ai/`, `pf-inference-bridge`

| Room ID | Status | Concept Depth | Exercises | Missing |
|---------|--------|---------------|-----------|---------|
| `memory-layout` | Precisa aprofundamento | ✓ NCHW/NHWC basic | ✓ MCQ | Tensor memory lab |
| `flops-bandwidth` | Sólida | ✓ Roofline link | ✓ MCQ | — |
| `simd-latency` | Sólida | ✓ Brief | ✓ MCQ | — |
| `aarch64-abi` | Sólida | ✓ AAPCS64 deep | ✓ Good | — |
| `export-runtime` | Sólida | ✓ Pipeline clear | ✓ MCQ | Export lab |
| `cmsis-nn` | Sólida | ✓ Deep quant | ✓ Good | — |
| `on-device` | Sólida | ✓ Checklist | ✓ Ritual | — |
| `edge-dl-forward` | Precisa aprofundamento | — | — | Forward pass impl |
| `edge-int8-detail` | Sólida | ✓ Requant | ✓ MCQ | — |
| `edge-benchmark` | Precisa aprofundamento | — | — | Benchmark guide |
| `edge-local-llm` | Sólida | ✓ KV cache | ✓ MCQ | — |
| `edge-dl-pipeline` | Scaffold | — | — | Incomplete |
| `edge-multimodal-lite` | Scaffold | — | — | Incomplete |
| `pf-inference-bridge` | Sólida | ✓ Bridge role | ✓ MCQ | — |

**Gap Analysis P6:**
- Missing: ONNX format deep dive
- Missing: Core ML conversion walkthrough
- Missing: ONNX Runtime optimization options
- Missing: llama.cpp architecture and optimizations
- Missing: Quantization techniques comparison (PTQ, QAT, GPTQ, AWQ)
- Missing: Operator fusion theory and practice
- Missing: Memory planning for inference
- Missing: Inference profiling methodology

**Priority Improvements:**
1. Add `edge-onnx-deep` room: ONNX graph, ops, optimization
2. Add `edge-coreml-export` room: PyTorch → Core ML workflow
3. Add `edge-quant-compare` room: Quantization techniques
4. Complete `edge-dl-pipeline` and `edge-multimodal-lite`

---

### P7 — Hardware-Software Co-design

**Track:** `content/tracks/11-performance/` (rooms 18-20)

| Room ID | Status | Concept Depth | Exercises | Missing |
|---------|--------|---------------|-----------|---------|
| `pf-rtl-intro` | Precisa aprofundamento | ✓ Comb/seq basic | ✓ MCQ | Verilog examples |
| `pf-hls-lite` | Precisa aprofundamento | ✓ Brief | ✓ MCQ | HLS workflow |
| `pf-boss-accelerator` | Precisa reestruturação | ✓ Boss template | ✓ MCQ | Project guide |

**Gap Analysis P7:**
- Missing: Digital logic fundamentals (gates, Boolean algebra)
- Missing: Sequential logic (flip-flops, FSMs)
- Missing: RTL design patterns (FSM + datapath)
- Missing: Verilog/SystemVerilog tutorial
- Missing: Testbench writing
- Missing: HLS pragmas and optimization
- Missing: FPGA architecture concepts
- Missing: Timing analysis basics
- Missing: Hardware interface protocols (AXI-lite, AXI-Stream)

**Priority Improvements:**
1. Add `pf-digital-logic` room: Gates, Boolean algebra, combinational
2. Add `pf-sequential` room: Flip-flops, FSMs, timing
3. Add `pf-verilog-intro` room: Basic Verilog syntax and patterns
4. Add `pf-testbench` room: Verification fundamentals

---

### Forge — Cumulative Project

**Track:** `content/tracks/12-emage-forge/`

| Room ID | Status | Concept Depth | Exercises | Missing |
|---------|--------|---------------|-----------|---------|
| `forge-portal` | Sólida | ✓ Continuity | ✓ MCQ | — |
| `forge-f0-scalar` | Precisa reestruturação | ✓ Foundation | ✓ MCQ | Starter code |
| `forge-f1-simd` | Precisa reestruturação | ✓ NEON prereqs | ✓ MCQ | NEON guide |
| `forge-f2-roofline` | Precisa reestruturação | ✓ Prereqs | ✓ MCQ | Roofline lab |
| `forge-f3-metal` | Precisa reestruturação | ✓ Metal prereqs | ✓ MCQ | Metal guide |
| `forge-f4-inference` | Precisa reestruturação | ✓ Prereqs | ✓ MCQ | Export guide |
| `forge-f5-codesign` | Precisa reestruturação | ✓ Prereqs | ✓ MCQ | HW guide |

**Critical Gap:** Forge rooms have good prerequisite chains but **no concrete implementation guidance**. The concept.md files explain prerequisites but don't provide:
- Project choice guidance (GEMM vs DSP filter vs convolution)
- Starter code structure
- Test harness templates
- Evidence collection methodology
- Benchmark comparison framework

**Priority:** See SPEC-forge.md for complete project specification.

---

## 2. Technical Fundamentals Coverage Matrix

### Required Knowledge vs Coverage

| Fundamental | P0 | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Gap |
|-------------|----|----|----|----|----|----|----|----|-----|
| Bit manipulation | ✓ | ✓ | — | — | — | — | — | — | — |
| Two's complement | ✓ | ✓ | — | — | — | — | — | — | — |
| IEEE 754 | — | — | — | — | ◐ | — | ✓ | — | P4 needs depth |
| Memory layout | — | ✓ | ✓ | — | — | — | ✓ | — | — |
| Pointers/aliasing | — | ✓ | — | — | — | — | — | — | — |
| Stack/heap | — | ✓ | — | — | — | — | — | — | — |
| Calling conventions | — | ✓ | — | — | — | — | ✓ | — | — |
| Assembly reading | ✓ | ✓ | — | — | — | — | ✓ | — | — |
| LLVM IR | — | ✓ | — | — | — | — | — | — | — |
| CPU pipeline | — | — | ◐ | — | — | — | — | — | P2 needs depth |
| Cache hierarchy | — | — | ◐ | — | — | — | — | — | P2 needs labs |
| SIMD concepts | — | — | — | ✓ | — | — | ✓ | — | — |
| NEON intrinsics | — | — | — | ◐ | — | — | — | — | P3 needs code |
| Tiling/blocking | — | — | — | ◐ | ✓ | — | — | — | P3 needs lab |
| Numerical stability | — | — | — | — | ◐ | — | — | — | P4 needs depth |
| Roofline model | — | — | — | — | ◐ | — | — | — | P4 needs lab |
| GPU architecture | — | — | — | — | — | ◐ | — | — | P5 needs depth |
| Metal basics | — | — | — | — | — | ◐ | — | — | P5 needs code |
| Quantization | — | — | — | — | — | — | ✓ | — | — |
| Export/runtime | — | — | — | — | — | — | ✓ | — | — |
| Digital logic | — | — | — | — | — | — | — | ◐ | P7 needs depth |
| RTL basics | — | — | — | — | — | — | — | ◐ | P7 needs code |
| Concurrency | — | ◐ | — | — | — | — | — | — | P1 needs room |
| OpenMP | — | — | — | — | — | — | — | — | **Missing** |
| Benchmarking | — | — | — | ◐ | — | — | — | — | Needs lab |

**Legend:** ✓ = Covered well | ◐ = Partial/shallow | — = Not applicable

---

## 3. Room Classification Summary

| Classification | Count | % | Action |
|----------------|-------|---|--------|
| **Sólida** | 89 | 57% | Minor polish only |
| **Precisa de aprofundamento** | 42 | 27% | Expand content |
| **Precisa de reestruturação** | 18 | 11% | Add code/labs |
| **Scaffold/Ausente** | 8 | 5% | Create or complete |

---

## 4. Priority Improvements (Ranked)

### P1 — Critical (Blocks learning objectives)

1. **Forge harness and project spec** (SPEC-forge.md)
   - Define concrete project options
   - Provide starter code structure
   - Create test harness templates

2. **P2 CPU Architecture depth**
   - Add OoO execution, branch prediction rooms
   - Create cache measurement lab

3. **P3 NEON implementation guide**
   - Add intrinsics practical room
   - Provide auto-vectorization analysis room

### P2 — High (Significant impact)

4. **P4 Numerical Computing depth**
   - Expand IEEE 754 error analysis
   - Add Roofline construction lab
   - Add GEMM implementation guide

5. **P5 Metal compute guide**
   - Add GPU architecture room
   - Create MSL tutorial
   - Provide compute shader example

6. **P1 Systems gaps**
   - Add UB/lifetime room
   - Add ELF/linker room
   - Add atomics room

### P3 — Medium (Polish and completeness)

7. **P7 Co-design foundation**
   - Add digital logic fundamentals
   - Add Verilog tutorial
   - Create testbench guide

8. **P6 Inference optimization depth**
   - Add ONNX deep room
   - Add Core ML export guide
   - Complete scaffold rooms

### P4 — Low (Nice to have)

9. **Assessment system improvements**
   - Add mastery criteria per room
   - Create placement quiz for P0

10. **Bibliography verification and expansion**
    - Verify all external URLs
    - Add missing academic references

---

## 5. Existing Tests Coverage

Current test suite (196 passing tests) covers:

| Test File | Coverage |
|-----------|----------|
| `test_emage_journey.py` | Journey loading, phase order, aliases |
| `test_performance.py` | Performance track structure, bosses |
| `test_neurotech.py` | Neurotech path, MSc requirements |
| `test_systems_pack.py` | Systems FLAG pack loading |
| `test_smoke.py` | Basic track loading, validators |
| `test_game_loop.py` | Room progression, code tasks |

**Recommendation:** Add tests for:
- Room content quality (concept.md length thresholds)
- Resource URL validity
- Forge stage prerequisite chains
- Exercise type distribution per phase

---

## 6. Conclusion

The e-mage curriculum has a solid architecture with correct pedagogical progression. The main gaps are:

1. **Depth in concept rooms** — Many rooms have good concepts but lack implementation guidance
2. **Practical exercises** — MCQ dominates; need more code/lab exercises
3. **Forge project specification** — The cumulative project exists as scaffold only
4. **P2-P5 technical depth** — Key performance engineering topics need expansion

This audit provides the foundation for prioritized improvements. See companion documents:
- `SPEC-forge.md` — Complete Forge project specification
- `GAPS-priority.md` — Prioritized gap list with implementation plan
- `BIBLIOGRAPHY-verified.md` — Verified resources by topic
