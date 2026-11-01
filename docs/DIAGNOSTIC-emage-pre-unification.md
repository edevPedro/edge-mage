# DIAGNOSTIC — e-mage before single-track unification

**Date:** 2026-11-02  
**Scope:** Repo `edevPedro/edge-mage` (+ edevs Estudo mirror).  
**Purpose:** Honest pre-change diagnosis so unification preserves strength and kills competing-course UX.

---

## 1. What exists today

| Surface | Shape | Problem for the learner |
|---------|--------|-------------------------|
| TUI launcher | 5 peer picks: Fundamentals · Systems · Edge · Performance · Neurotech | Feels like five courses to choose; no single “what’s next” |
| `courses.py` | Five `CourseInfo` ids, soft-gate after Mago base | Specializations framed as alternate products |
| `content/tracks/` | Edge math→on-device (01–09) + Neurotech (10) + Performance (11) | Perf/Neuro excluded from Edge pack via sibling filter |
| `content/courses/` | Fundamentals YAML + Systems pack/craft | Parallel catalogs, not one progression |
| Web Estudo | Same five course cards (`courses.ts`) | Mirrors multi-course UX |
| Pedagogy loop | Quiz → Spell → Ritual (good) | Intact; not the UX failure mode |
| Gates | `unlock_xp`, `requires_rooms`, rituals, ranks | Real but **per course**, not journey-wide mastery narrative |

---

## 2. Strengths to preserve

1. **Estuda → Sala → Boss** (story/concept/lesson + tasks + ritual evidence) — keep as the unit of learning.
2. **Performance Mage scaffold** — 20 rooms, pedagogical order, Performance Boss template, M4 caveats — already matches the desired technical spine (arch → NEON → Roofline → Metal → bridge → co-design).
3. **Systems FLAG pack** — dense offline catalog (systems/llvm/math) + craft bosses; shared `room_id` credit.
4. **Edge on-device ritual** — measurable latency/RAM evidence; honest rank gate for Edge Mage / Mago Supremo.
5. **Neurotech density** — MSc-prep circle with emulators; valuable as **elective**, not competitor.
6. **Progress model** — `completed_rooms_by_id`, mastery bumps, publish artifacts, soft preview without Mago base.
7. **Resource lint + CI** — quality bar already partially automated.

---

## 3. Gaps / failure modes

| Gap | Evidence | Impact |
|-----|----------|--------|
| **Competing journeys as UX** | Launcher BANNER + README “Courses” table + `--course` choices | User must manually switch “mages”; rejects product goal |
| **Spine order wrong for stated mission** | Performance ends with co-design before full Edge inference path in TUI; Edge is a sibling course | Inference not ON the spine after GPU foundations |
| **No cumulative project** | Bosses are phase-local; no one artifact that evolves scalar→SIMD→Metal→inference | Misses “one main project” pedagogy |
| **Adaptive mastery is thin** | Mastery = room replay counter; quiz fails don’t point remediation; unlock often XP/checkbox | Not “demonstrated mastery” narrative |
| **Cross-course prereqs weak** | `requires_rooms` works via `room_id` credit, but journeys never compose tracks | Soft deps documented, not enforced as progression |
| **Duplicate / overlapping math** | Fundamentals shared + Edge `01-fundamentos` + Systems math pack | Risk of redundant rooms if naïvely concatenated |
| **Hours honesty** | Performance aspirational 310–415 h vs scaffold 200–280 h; academy vs specialization messaging | Need one calendar story (1–3 years) |
| **Hardware assumptions** | CUDA/FPGA optional but easy to over-promise | Must keep M4-first + elective CUDA/FPGA |
| **Pro C++ ≠ arch mastery** | No progressive assessment at portal | Risk of skipping literacy rooms |

---

## 4. Content inventory (snapshot)

| Module label (legacy course) | Location | Approx. rooms | Role after unification |
|------------------------------|----------|---------------|------------------------|
| Fundamentals | `content/courses/fundamentals` + `shared/` | ~7 | **P0** literacy → Mago base |
| Systems | pack `systems.json` + craft YAML | 70+ | **P1** systems craft |
| Edge math/signals/robotics | tracks 01–05 | dozens | Support / enrichment (not competing home) |
| Edge ML path | tracks 05–09 (otimização → rituais → edge-ai) | dozens | **P6** inference optimization ON spine |
| Performance | track 11 | 20 | **P2–P5 + P7** (sliced phases in journey loader) |
| Neurotech | track 10 | ~89 | **Elective branch** |

---

## 5. Diagnosis (one paragraph)

e-mage already has the **right pedagogical atoms** and most of the **right technical content**, but the **product shell presents five independent courses**. Performance content is the natural low-level→GPU→co-design spine; Edge on-device is the natural inference phase; Neurotech is a strong elective. Unification should **re-sequence and gate**, not rewrite. Success = learner opens TUI and sees **one primary progression** with a clear next unlock; legacy course ids remain as a secondary module browser only.

---

## 6. Non-goals for this unification pass

- Destroying Neurotech or Performance room markdown.
- Inventing ML “personalization” without evidence hooks.
- Requiring CUDA or FPGA hardware for the main path.
- Auto-committing or force-pushing.
- Fake URLs / invented citations.

---

## 7. Definition of done (unification)

See `docs/SPEC-emage-single-track.md` § Definition of done.

**Follow-up constraints (2026-11-02):** foundations-first Estuda before every Spell/Boss; offline-complete local tree (TUI source of truth; URLs optional only).