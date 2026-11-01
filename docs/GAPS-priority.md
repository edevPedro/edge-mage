# GAPS — Prioritized Improvements for e-mage Deep Curriculum

**Date:** 2026-11-01  
**Based on:** AUDIT-emage-deep-curriculum.md  
**Scope:** Actionable improvements prioritized by impact on learning objectives

---

## Priority Framework

| Priority | Criteria | Timeline |
|----------|----------|----------|
| **P1 Critical** | Blocks core learning objectives | Immediate |
| **P2 High** | Significant impact on depth | Near-term |
| **P3 Medium** | Polish and completeness | Future |
| **P4 Low** | Nice to have | Backlog |

---

## P1 — Critical Improvements

### 1.1 Forge Project Implementation Guide

**Gap:** Forge rooms have prerequisite chains but no concrete implementation guidance.

**Impact:** Without starter code and harness templates, Forge cannot serve as the cumulative project.

**Action Items:**
- [x] Create SPEC-forge.md with project options and requirements
- [ ] Create `content/labs/forge-starter/` with CMake project template
- [ ] Add test harness templates for GEMM, FIR, and Jacobi
- [ ] Update each Forge room with links to starter code
- [ ] Add code tasks to Forge rooms (not just MCQ)

**Files to Create/Modify:**
```
content/labs/forge-starter/
├── CMakeLists.txt
├── src/
│   ├── gemm_scalar.cpp
│   ├── gemm_neon.cpp
│   ├── gemm.metal
│   └── gemm_quant.cpp
├── tests/
│   └── test_golden.cpp
└── bench/
    └── benchmark.cpp
```

---

### 1.2 P2 CPU Architecture Depth

**Gap:** `pf-pipeline` and `pf-cache-vm` are too shallow for serious architecture understanding.

**Impact:** Cannot explain performance without understanding CPU execution model.

**Action Items:**
- [ ] Expand `pf-pipeline` concept.md: Add OoO, superscalar, register renaming
- [ ] Create `pf-branch-pred` room: Branch prediction, BTB, speculative execution
- [ ] Create `pf-cache-lab` room: Empirical cache measurement experiments
- [ ] Create `pf-false-sharing` room: Multi-threaded cache effects
- [ ] Add code tasks with measurable experiments

**New Rooms:**
```yaml
# content/tracks/11-performance/rooms/02b-pf-ooo-superscalar/
id: pf-ooo-superscalar
title: Out-of-Order & Superscalar Execution
phase: F1-arch
order: 2.5
requires_rooms: [pf-pipeline]

# content/tracks/11-performance/rooms/02c-pf-branch-pred/
id: pf-branch-pred
title: Branch Prediction
phase: F1-arch
order: 2.6
requires_rooms: [pf-pipeline]

# content/tracks/11-performance/rooms/03b-pf-cache-lab/
id: pf-cache-lab
title: Cache Measurement Lab
phase: F1-arch
order: 3.5
requires_rooms: [pf-cache-vm]
```

---

### 1.3 P3 NEON Implementation Guide

**Gap:** NEON rooms explain concepts but don't show how to write intrinsics.

**Impact:** Cannot complete Forge F1 without practical intrinsics knowledge.

**Action Items:**
- [ ] Create `pf-neon-intrinsics` room: Practical patterns (load, arithmetic, store)
- [ ] Create `pf-autovec-check` room: Verifying compiler vectorization
- [ ] Add code tasks with intrinsics exercises
- [ ] Update `pf-boss-arm-math` with starter harness

**New Rooms:**
```yaml
# content/tracks/11-performance/rooms/05b-pf-neon-intrinsics/
id: pf-neon-intrinsics
title: NEON Intrinsics in Practice
phase: F2-arm
order: 5.5
requires_rooms: [pf-neon-intro]

# content/tracks/11-performance/rooms/05c-pf-autovec-check/
id: pf-autovec-check
title: Analyzing Auto-Vectorization
phase: F2-arm
order: 5.6
requires_rooms: [pf-neon-intro]
```

---

## P2 — High Priority Improvements

### 2.1 P4 Numerical Computing Depth

**Gap:** IEEE 754 and Roofline are mentioned but not practiced.

**Impact:** Cannot do serious numerical work without error analysis skills.

**Action Items:**
- [ ] Expand `pf-nla-ieee` concept.md: Error propagation, stability analysis
- [ ] Create `pf-roofline-lab` room: Build Roofline plot for M4
- [ ] Create `pf-gemm-impl` room: Step-by-step tiled GEMM
- [ ] Create `pf-openmp-intro` room: Basic CPU parallelization
- [ ] Add numerical stability exercises

**New Rooms:**
```yaml
# content/tracks/11-performance/rooms/10b-pf-roofline-lab/
id: pf-roofline-lab
title: Building a Roofline Plot
phase: F3-hpc
order: 10.5
requires_rooms: [pf-roofline]

# content/tracks/11-performance/rooms/11b-pf-gemm-impl/
id: pf-gemm-impl
title: GEMM Implementation Workshop
phase: F3-hpc
order: 11.5
requires_rooms: [pf-gemm-jacobi]

# content/tracks/11-performance/rooms/11c-pf-openmp-intro/
id: pf-openmp-intro
title: OpenMP Basics
phase: F3-hpc
order: 11.6
requires_rooms: [pf-roofline]
```

---

### 2.2 P5 Metal Compute Guide

**Gap:** Metal rooms don't provide enough for first GPU kernel implementation.

**Impact:** Cannot complete Forge F3 without Metal tutorial.

**Action Items:**
- [ ] Create `pf-gpu-arch` room: GPU execution model fundamentals
- [ ] Create `pf-msl-intro` room: Metal Shading Language basics
- [ ] Create `pf-metal-compute` room: First compute shader walkthrough
- [ ] Expand `pf-boss-metal` with project template
- [ ] Add GPU profiling with Instruments guide

**New Rooms:**
```yaml
# content/tracks/11-performance/rooms/13b-pf-gpu-arch/
id: pf-gpu-arch
title: GPU Architecture Fundamentals
phase: F4-gpu
order: 13.5
requires_rooms: [pf-metal-intro]

# content/tracks/11-performance/rooms/13c-pf-msl-intro/
id: pf-msl-intro
title: Metal Shading Language
phase: F4-gpu
order: 13.6
requires_rooms: [pf-gpu-arch]

# content/tracks/11-performance/rooms/14b-pf-metal-compute/
id: pf-metal-compute
title: First Metal Compute Shader
phase: F4-gpu
order: 14.5
requires_rooms: [pf-msl-intro]
```

---

### 2.3 P1 Systems Gaps

**Gap:** Critical systems topics missing from P1.

**Impact:** Foundation gaps propagate to later phases.

**Action Items:**
- [ ] Create `sys-ub-lifetime` room: Undefined behavior, object lifetime
- [ ] Create `sys-elf-deep` room: ELF structure, symbols, relocations
- [ ] Create `sys-linker-loader` room: Static/dynamic linking
- [ ] Create `sys-atomics` room: Memory ordering, atomics
- [ ] Add to systems.json pack

**New Rooms (FLAG format):**
```json
{
  "id": "sys-ub-lifetime",
  "title": "Undefined Behavior & Object Lifetime",
  "track": "systems",
  "phase_id": "s2",
  "checkpoint": "FLAG{ub:dangling-ref}"
}
```

---

## P3 — Medium Priority Improvements

### 3.1 P7 Co-design Foundation

**Gap:** Digital logic and RTL fundamentals missing.

**Action Items:**
- [ ] Create `pf-digital-logic` room: Gates, Boolean algebra
- [ ] Create `pf-sequential` room: Flip-flops, FSMs, timing
- [ ] Create `pf-verilog-intro` room: Basic Verilog syntax
- [ ] Create `pf-testbench` room: Verification fundamentals
- [ ] Update boss with clearer project options

---

### 3.2 P6 Inference Depth

**Gap:** Some scaffold rooms incomplete.

**Action Items:**
- [ ] Create `edge-onnx-deep` room: ONNX format details
- [ ] Create `edge-coreml-export` room: PyTorch → Core ML
- [ ] Create `edge-quant-compare` room: PTQ, QAT, GPTQ comparison
- [ ] Complete `edge-dl-pipeline` and `edge-multimodal-lite`

---

### 3.3 Assessment System Improvements

**Gap:** Mastery criteria not explicit per room.

**Action Items:**
- [ ] Add `mastery_criteria` field to room.yaml schema
- [ ] Define observable mastery indicators per room
- [ ] Create P0 placement quiz
- [ ] Add mastery-based progression gates

---

## P4 — Low Priority Improvements

### 4.1 Bibliography Verification

- [ ] Verify all external URLs in resources
- [ ] Add missing academic references
- [ ] Create central bibliography document

### 4.2 Test Coverage Expansion

- [ ] Add room content quality tests
- [ ] Add resource URL validation tests
- [ ] Add Forge prerequisite chain tests

### 4.3 Documentation Polish

- [ ] Update README with audit findings
- [ ] Add architecture diagrams
- [ ] Improve CURRICULUM.md detail

---

## Implementation Order

### Phase 1: Documentation (This PR)
1. ✅ AUDIT-emage-deep-curriculum.md
2. ✅ SPEC-forge.md
3. ✅ GAPS-priority.md
4. [ ] BIBLIOGRAPHY-verified.md

### Phase 2: P2 Architecture Expansion
1. [ ] Expand pf-pipeline concept.md
2. [ ] Create pf-ooo-superscalar room
3. [ ] Create pf-branch-pred room
4. [ ] Create pf-cache-lab room

### Phase 3: P3 NEON Implementation
1. [ ] Create pf-neon-intrinsics room
2. [ ] Create pf-autovec-check room
3. [ ] Expand pf-boss-arm-math

### Phase 4: Forge Starter
1. [ ] Create forge-starter lab structure
2. [ ] Add GEMM implementation template
3. [ ] Add test harness

### Future Phases:
- P4 numerical depth
- P5 Metal guide
- P1 systems gaps
- P7 co-design foundation

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Rooms with code tasks | ~40% | 80% |
| Boss rooms with harness | 0% | 100% |
| P2 depth score | 2/5 | 4/5 |
| P3 implementation score | 2/5 | 4/5 |
| Forge completeness | 10% | 80% |

---

## Notes

- Preserve all existing room IDs and progression
- New rooms use fractional order (e.g., 2.5) to insert without renumbering
- All changes must pass existing test suite
- No changes to Neurotech branch (optional)
- Bibliography verification deferred to separate pass
