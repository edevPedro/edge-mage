# SPEC — e-mage single continuous journey

**Product:** e-mage  
**Primary journey id:** `emage` (aliases: default launcher entry, `mage --course emage`)  
**Status:** Architecture + MVP wiring (2026-11-02)  
**Supersedes (UX):** competing picks among Systems / Performance / Edge / Neurotech as peer “courses.”  
**Preserves:** module labels, room content, Quiz/Spell/Ritual loop, ranks, publish artifacts.

Related: `docs/DIAGNOSTIC-emage-pre-unification.md`, `docs/SPEC-performance-mage.md`, `docs/SPEC-neurotech-course.md`, `SPEC-edge-mage-loop.md`.

---

## 1. Product thesis

One continuous, adaptive learning journey:

```text
Low-Level Performance Engineering
  → CPU Arch & Optimization
  → SIMD
  → HPC / Numerical
  → GPU (Metal-first)
  → Inference Optimization (Edge ML ON spine)
  → HW/SW Co-design (FPGA when ready)
```

**Not** a catalog of independent Mage courses. Legacy names (Systems Mage, Performance Mage, …) remain **internal module / phase labels**.

Neurotech is an **optional application branch** off the spine — accessible, never a competing home screen default.

---

## 2. Learner assumptions (honest)

| Fact | Curriculum consequence |
|------|------------------------|
| Pro C++ / finance / threads / SQL | Skip “learn syntax” fluff; do **not** skip arch/asm/SIMD/GPU assessment |
| CS + Physics in progress | Keep physics/signals as enrichment; depth comes later |
| MacBook Air M4 · 16GB · Metal | Labs default to AArch64 + NEON + Metal; no assume discrete NVIDIA |
| ESP32 / Arduino available | Optional embedded labs; Cortex-M ≠ Apple µarch |
| No CUDA / FPGA required to start | CUDA + FPGA = electives / late phase |

**M4 caveats (mandatory in portal + phase intros):**

1. Apple µarch ≠ Cortex-A (timings/PMU do not transfer 1:1).  
2. No SVE on M4 — deep vector labs = **NEON/ASIMD**.  
3. Metal ≠ CUDA (memory model + tooling).  
4. Host ARM64 ≠ Cortex-M (ESP32 path is separate literacy).

---

## 3. Pedagogy (unchanged atoms, stronger gates)

### Foundations-first (non-negotiable)

For **every** problem, lab, boss, or Forge stage:

1. **Estuda first** — `concept.md` (+ `story.md`) teaches the *prerequisite foundation* that makes the solution make sense (why the machine behaves that way, what the bottleneck class is, what correctness means).
2. **Sala second** — short Quiz/Spell only after that foundation is on the page.
3. **Never** dump a NEON / GPU / inference / RTL task whose solution depends on unread arch, memory, numerics, or ABI material — gate with `requires_rooms` to the teaching rooms, and put the why/how in-repo (not “go read this URL to learn the concept”).
4. External `resources:` links are **optional further reading** only. Offline study must work from `concept.md` + `lesson.md` alone.

| Layer | Name | Evidence |
|-------|------|----------|
| 1 | **Quiz** | MCQ / numeric / fill — gaps & vocabulary |
| 2 | **Spell** | `code` / `c_code` + harness tests — implementation |
| 3 | **Ritual** | Boss + artifact under `study-log/artifacts/` + `mage publish` — integrated proof |

**Adaptive (MVP — not fake ML):**

- Unlock by **prereq rooms** (`requires_rooms` / `requires_rooms_any`) + **rituals** + skill gates — not XP alone for phase portals.
- Failed quiz / spell → remediation pointer to the Estuda room that teaches the concept (see §7).
- Mastery replay (`mastery` 0..3) remains; phase bosses require **numerical correctness + measure**, not speed theater.
- Progressive assessment: portal quiz assumes C++ comfort but **tests** cache/ISA/SIMD literacy before P2+.

---

## 4. Phase map (modules inside one progression)

| Phase | Module label (internal) | Content source | Gate into phase | Hours (± guided) |
|-------|-------------------------|----------------|-----------------|------------------|
| **P0** | Foundations | `courses/fundamentals` + shared core | open | 25–40 |
| **P1** | Systems craft | Systems pack (systems/llvm/math) + craft bosses | Mago base (`fundamentals-clear`) preferred; preview OK | 50–90 |
| **P2** | CPU arch & memory | Performance rooms `pf-portal`…`pf-aarch64-perf` | P0 clear (room credit) | 20–35 |
| **P3** | SIMD / ARM perf | `pf-neon-intro`…`pf-boss-arm-math` | P2 chain | 40–55 |
| **P4** | Numerical / HPC | `pf-nla-ieee`…`pf-boss-physics` | ARM Math boss | 45–60 |
| **P5** | GPU (Metal) | `pf-metal-intro`…`pf-boss-metal` (+ CUDA elective) | Physics boss | 45–65 |
| **P6** | Inference optimization | Edge tracks: otimização → ml-math → rituais → edge-ai (+ `pf-inference-bridge`) | Metal boss **or** soft preview after Systems; Softmax ritual still gates `edge-ai` | 50–90 |
| **P7** | HW/SW co-design | `pf-rtl-intro`…`pf-boss-accelerator` | Inference bridge + preferably on-device ritual | 35–50 |
| **E*** | Enrichment | física-sinais, elétrica-edge, robotica, programação spiral | After P0; never replace spine | 30–60 |
| **B** | Neurotech branch | track `neurotech` | After P0; optional; does not replace P6 on-device for primary Supremo | 180–300+ |

**Calendar:** ~**400–650 h** guided spine (P0–P7) at 4–8 h/week ≈ **1–3 years** sustainable. Enrichment + Neurotech + densified labs push the upper end. Do not claim a 12-week miracle.

---

## 5. Prerequisite map (authoritative)

```text
fundamentals-clear (Mago base)
    │
    ├─► P1 systems / llvm / math / craft
    │
    └─► P2 pf-portal → pipeline → cache-vm → aarch64-perf
            │
            └─► P3 neon → tiling → counters → boss-arm-math
                    │
                    └─► P4 nla → roofline → gemm-jacobi → boss-physics
                            │
                            └─► P5 metal → kernels → (cuda elective) → boss-metal
                                    │
                                    ├─► P6 Edge ML path (math→export→CMSIS→on-device)
                                    │       pf-inference-bridge (literacy hinge)
                                    │
                                    └─► P7 rtl → hls → boss-accelerator
                                            (prefer on-device evidence)

Neurotech branch ◄── P0 (soft); recommended after signals/electrical enrichment
```

**Rules:**

- Performance is **on the spine**, not an Edge hard-gate sibling.  
- Edge on-device remains the primary **inference ritual** for Mago Supremo (Edge route).  
- Neurotech climax remains an **alternate** Supremo route (unchanged honesty).  
- CUDA elective never blocks Metal boss.  
- FPGA board labs optional; pedagogical RTL/HLS suffices for P7 boss.

---

## 6. Main cumulative project — “Forge”

**Name:** Forge (working title)  
**Idea:** One codebase / portfolio thread that **evolves** across phases instead of disconnected demos.

| Stage | Phase | Deliverable (objective criteria) |
|-------|-------|----------------------------------|
| F0 | P0–P1 | Scalar reference kernel (e.g. GEMM or DSP filter) + harness + Git evidence |
| F1 | P3 | NEON/ASIMD optimized path; ≥1 metric vs scalar; correctness vs golden |
| F2 | P4 | Roofline story + tiled/blocked variant; abs/rel tolerance documented |
| F3 | P5 | Metal compute path (or documented fallback); same golden |
| F4 | P6 | Quantized / on-device or host-ORT inference path using same math motif; latency+RAM |
| F5 | P7 | Optional accelerator sketch (HLS/RTL lite) or honest “stop here” portfolio |

Rooms: `content/tracks/12-emage-forge/` (portal + stage rituals). Boss templates reuse Performance Boss + Edge on-device checklists.

**Pass rule (every Forge stage):** two implementations **or** clear baseline+optimized · measure · explain bottleneck · prove numerical correctness.

---

## 7. Adaptive hooks (MVP)

Implemented / required:

1. **Journey loader** — `load_tracks_for_course("emage")` returns ordered phase tracks.  
2. **Cross-phase unlock** — room gates honor `completed_rooms_by_id` (already). Phase portals set `requires_rooms` on first room of slice where needed.  
3. **P7 soft gate** — co-design track `requires_ritual: on-device` *or* completion of `pf-inference-bridge` via `requires_rooms_any` on portal room (document in room YAML).  
4. **Remediation map** — `edge_mage/mastery.py` maps task failure tags → room ids (minimal table for P2–P3).  
5. **Launcher** — primary action: **Continue journey (`emage`)**; secondary: Module browser (legacy ids).  
6. **`:continue`** — uses pedagogical order of the loaded journey tracks.

Not in MVP: Bayesian knowledge tracing, remote A/B, auto-generated quizzes.

---

## 8. Module content outline (spine)

### P0 Foundations
Concepts: bits, vectors, asm literacy, ISA glance, clearance.  
Exercises: shared rooms + fundamentals-clear.  
Project: Forge F0 scaffold.

### P1 Systems craft
Concepts: memory, ABI, ELF, LLVM IR literacy, math CS touchpoints.  
Exercises: FLAG pack + craft bosses.  
Project: link Forge harness to real toolchain evidence (`nm`/`objdump` optional).

### P2 Arch & memory
Concepts: pipeline/hazards, cache/VM/TLB, AArch64 perf lens, M4 caveats.  
Exercises: pf-portal…pf-aarch64-perf.  
Project: profile scalar Forge kernel.

### P3 SIMD
Concepts: NEON, tiling, counters/PMU honesty.  
Exercises: through ARM Math boss.  
Project: Forge F1 NEON path.

### P4 HPC
Concepts: IEEE754, Roofline, GEMM/Jacobi.  
Exercises: through Physics boss.  
Project: Forge F2 Roofline write-up.

### P5 GPU
Concepts: Metal compute, kernel structure; CUDA elective literacy.  
Exercises: through Metal boss.  
Project: Forge F3 Metal path.

### P6 Inference
Concepts: autograd literacy → quant → export/runtime → CMSIS-NN / on-device; bridge room.  
Exercises: Edge tracks + rituais + on-device.  
Project: Forge F4 inference evidence.

### P7 Co-design
Concepts: RTL/HLS lite, pedagogical accelerator.  
Exercises: through Accelerator boss.  
Project: Forge F5 optional.

### Branch — Neurotech
Keep SPEC-neurotech; launcher lists under **Branches**, not primary.

### Enrichment
Signals / electrical / robotics — unlock after P0; recommended before Neurotech apps.

---

## 9. Bibliography (verified primary sources)

Use these in rooms; prefer official docs over blogs. Do not invent URLs.

| Topic | Source |
|-------|--------|
| AArch64 ABI | https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst |
| Arm ARM | https://developer.arm.com/documentation/ddi0487/latest |
| Arm NEON | https://developer.arm.com/architectures/instruction-sets/intrinsics/ |
| Apple Metal | https://developer.apple.com/documentation/metal/ |
| Apple Metal Shading Language | https://developer.apple.com/metal/Metal-Shading-Language-Specification.pdf |
| Roofline (Williams et al.) | https://doi.org/10.1145/1498765.1498785 |
| IEEE 754 overview | https://ieeexplore.ieee.org/document/8766229 |
| PyTorch export | https://pytorch.org/docs/stable/export.html |
| ONNX | https://onnx.ai/ |
| LiteRT / TF Lite | https://ai.google.dev/edge/litert |
| CMSIS-NN | https://github.com/ARM-software/CMSIS-NN |
| RISC-V unpriv (literacy) | https://docs.riscv.org/ |
| x86-64 psABI (literacy) | https://gitlab.com/x86-psABIs/x86-64-ABI |

Papers only when tied to a lab (Roofline, quant survey). Neurotech citations remain in Neurotech SPEC.

---

## 10. Quality criteria

A phase/room ships only if:

1. Estuda (concept) + Sala (tasks) present; theory rooms not MCQ-only.  
2. **Foundations-first:** concept teaches the prereq needed for the tasks; external URLs optional only.  
3. Resources prefer official docs when linked; `scripts/lint_resources.py` clean.  
4. Bosses: measure + explain + golden correctness.  
5. M4 caveats stated at P2 portal and GPU portal.  
6. No competing “pick your Mage” as default UX.  
7. Hours labeled scaffold vs aspirational.  
8. **Offline:** core path loads from bundled content + `~/.mage` progress; no network required for `mage --course emage`.  
9. Tests: journey load order, phase gates, legacy course aliases still load.

## 10b. Offline contract

| What | Offline? |
|------|----------|
| Lessons / story / concept / tasks YAML | Yes — in `content/` |
| Systems FLAG pack | Yes — bundled `content/packs/systems.json` (install seeds `~/.mage/packs/`) |
| Progress / ranks / rituals | Yes — `~/.mage/` |
| `mage sync` / GitHub auth / web Estudo | Optional when online |
| CUDA machine / FPGA board | Not required for core path |

TUI is source of truth for offline study; web Estudo is a mirror/CTA.

---

## 11. Repo implementation plan

### Done in this unification pass

- [x] `DIAGNOSTIC` + this SPEC  
- [x] Course id `emage` + journey loader (phase-sliced performance + ordered modules)  
- [x] Launcher: primary Continue journey + module browser  
- [x] Cross-phase track orders + P7 gate hooks  
- [x] Forge track scaffold (`12-emage-forge`)  
- [x] Mastery remediation MVP map  
- [x] README EN+PT + CURRICULUM single-journey copy  
- [x] Tests for pedagogical journey order  
- [x] edevs Estudo: primary journey card / docs sync  

### Remaining (honest)

- [ ] Densify thin Estuda rooms; full Forge harness repos per stage  
- [ ] Deeper remediation (per-task hint → room) beyond MVP table  
- [ ] Web Estudo full UI single-spine nav (beyond course meta)  
- [ ] Hours → upper aspirational band via lab depth  
- [ ] FPGA board electives when hardware available  
- [ ] Progressive placement exam richer than portal MCQs  

---

## 12. CLI / UX contract

```text
mage                  → launcher (Continue journey first)
mage --course emage   → primary progression
mage --course performance|systems|edge|…  → module browser aliases (still work)
:courses              → launcher
:continue             → next open room on current journey tracks
```

Default when entering from launcher **Continue**: `emage`.

---

## 13. Definition of done

Learner opens TUI and sees **one primary progression** with clear next unlock; Performance/Systems/Edge content exist as **phases**, not competing default picks; SPEC docs complete; tests pass; remaining gaps listed in §11.
