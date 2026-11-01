# SPEC — Performance Mage (e-mage)

Course id: **`performance`** — specialization sibling to **Edge ML Mage** and **Systems Mage**.  
Product: **e-mage** · `content/tracks/11-performance/` · web: edevs `/estudo/cursos/performance`.

**Pedagogy (mandatory):**

```text
Estuda (story + concept + lesson) → Sala (short tasks)
  → Performance Boss / portfolio project (large, mandatory craft)
```

Not a quiz-only track. Theory is rigorous; exercises are short; **projects carry the grade**.

---

## 1. Role in the academy

| Course | Role |
|--------|------|
| **Fundamentals** | Math, C/C++, terminal — Mago base |
| **Systems Mage** | AArch64, LLVM, ABI, memory literacy |
| **Performance Mage** | Measure → explain → prove: NEON, Roofline, Metal, co-design |
| **Edge ML Mage** | On-device inference path (Mago Supremo primary route) |
| **Neurotech** | Parallel circle — BCI / neural signals (preserved) |

**Fundamentals academy stays the foundation.** Performance deepens systems craft into a university-level specialization band without inventing a competing “new study project from scratch.”

### Soft deps only toward Edge

- Performance is **not** a hard gate for Edge ML rooms or Mago Supremo.
- Advanced Edge rooms *may* soft-link Performance (SIMD / Roofline literacy).
- Inference Engineering months (9–10) are a **bridge**: literacy here, full runtime ritual in Edge.

---

## 2. Goals (after required path)

| Pillar | Outcome |
|--------|---------|
| **Architecture** | Pipeline/hazards, cache/VM/TLB, AArch64 under a performance lens |
| **ARM perf** | NEON/ASIMD, tiling, prefetch, counters; mini math library with evidence |
| **Numerical / HPC** | IEEE754 honesty, Roofline, GEMM/Jacobi/heat with correctness |
| **GPU** | Metal compute on Apple Silicon; CUDA as elective literacy |
| **Inference bridge** | ORT / Core ML / llama.cpp / CMSIS-NN literacy → Edge projects |
| **Co-design** | Digital logic + Verilog/HLS lite → pedagogical accelerator |

Does **not** mint a silicon tapeout engineer or CUDA specialist overnight. Puts the learner ahead of “I only micro-benchmarked once.”

---

## 3. Performance Boss ritual

Every boss room (`pf-boss-*`) encodes:

1. **Two implementations** — clear baseline + optimized (SIMD / tile / Metal / HW model).
2. **Measure** — fixed input, repeated runs, machine + flags noted (median / p95).
3. **Explain** — Roofline or equivalent bottleneck story (memory vs compute).
4. **Prove numerical correctness** — golden reference + explicit abs/rel tolerance.

Without (4), the boss is **incomplete** even if faster.

Suggested artifacts under `study-log/artifacts/`:

| Boss room | Artifact | Portfolio name |
|-----------|----------|----------------|
| `pf-boss-arm-math` | `perf-arm-math.md` | ARM Math Library |
| `pf-boss-physics` | `perf-physics.md` | Physics Simulation |
| `pf-boss-metal` | `perf-metal-engine.md` | Metal Compute Engine |
| (Edge pointer) | Edge on-device / export | Edge Inference Runtime |
| `pf-boss-accelerator` | `perf-accelerator.md` | Hardware Accelerator |

Ritual templates: `docs/rituals/performance-boss-template.md`.

---

## 4. Phase map + hours (honest)

**Aspirational specialization band:** **~310–415 h** guided at **6–8 h/week** (~10–14 months calendar).  
This matches the 12-month content outline encoded as phases/rooms. **Do not treat empty titles as hours earned** — only rooms with real Estuda + Sala (+ bosses) count.

| Phase | Title | Rooms (now) | Hours (± scaffold) | Focus |
|-------|-------|-------------|--------------------|--------|
| **F0** | Portal | 1 | 2–4 | Modular map, M4 caveats, Estuda→Sala |
| **F1-arch** | Architecture & memory | 3 | 18–28 | Pipeline, cache/VM/TLB, AArch64 perf |
| **F2-arm** | ARM performance | 4 | 40–55 | NEON, tiling, counters, **ARM Math boss** |
| **F3-hpc** | Numerical & Roofline | 4 | 45–60 | IEEE754, Roofline, GEMM/Jacobi, **Physics boss** |
| **F4-gpu** | GPU | 4 (1 elective) | 45–65 | Metal kernels, CUDA elective, **Metal boss** |
| **F5-inf** | Inference bridge | 1 | 12–20 | Soft pointer to Edge runtime work |
| **F6-hw** | Co-design | 3 | 35–50 | RTL/HLS lite, **Accelerator boss** |

**Catalog now:** **20** rooms (**19** required + **1** elective).  
Sum of phase bands above ≈ **197–282 h** of *scaffolded* guided work; the **310–415 h** README band includes deeper lab time, portfolio polish, and future room densification (honest gap — see §7).

Shared architecture literacy with Systems: deepen here; do **not** delete Systems content.

---

## 5. Apple Silicon / M4 caveats (mandatory in docs & portal)

1. **µarch ≠ Cortex-A** — M-series timings/PMU do not transfer 1:1 to mobile Cortex-A.
2. **No SVE on M4** — labs focus **NEON/ASIMD**; SVE is comparative literacy.
3. **Metal ≠ CUDA** — different memory model and tooling; CUDA is elective/complement.

---

## 6. TUI / web wiring

```text
mage --course performance
```

- Track: `content/tracks/11-performance/` (`course: performance`)
- Excluded from Edge `load_all_tracks` siblings filter (with Neurotech)
- Soft gate: Mago base preferred; preview allowed
- Web: `content/estudo/performance/export.json` + course card

---

## 7. Content gaps (remaining)

| Gap | Notes |
|-----|--------|
| Deeper Estuda on mid-pillar rooms | First rooms of each pillar are dense; some later rooms still expand |
| Full harness repos per boss | Rituals point to artifacts; sample code trees TBD |
| Shared room credit with Systems cache/asm | Soft cross-links, not duplicated FLAG spam |
| CUDA lab machine story | Elective assumes access or reading-only path |
| FPGA board labs | Accelerator boss is pedagogical RTL/HLS — board optional later |
| Hours → 310–415 | Requires more lab depth + electives over time |

---

## 8. Checklist (definition of done for this SPEC revision)

- [x] Course id `performance` in catalog + `--course performance`
- [x] Track with rooms covering four pillars + inference bridge + bosses
- [x] Performance Boss documented + boss YAMLs
- [x] READMEs / CURRICULUM / changelog mention academy vs specialization
- [x] Edge remains non-gated by Performance
- [x] M4 caveats documented
- [x] Tests: catalog + track load + pedagogical order
