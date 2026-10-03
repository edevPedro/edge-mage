# SPEC — Neurotech course (e-mage)

Course id: **`neurotech`** — sibling circle to **Edge ML Mage** (`edge`), not a replacement.  
Product: **e-mage** · content lives under `content/tracks/10-neurotech/` · web mirror via edevs Estudo when wired.

**Pedagogy (mandatory from now on for this course):**

```text
Estuda (lição + história + animação/conceito) → Sala (lab / FLAG / emulator tasks)
```

Agents: `agent-pedagogo` + domain skills `agent-bci` · `agent-neuroeng` · `agent-eletrica` · `agent-fisica` · `agent-neurociencia`.

---

## 1. Goals

A learner who finishes Neurotech (target rank **Neuro Mage** — parallel circle) can:

| Domain | Outcome |
|--------|---------|
| **BCI** | Explain online vs offline decode; run a MI-style feature→classifier MVP on synthetic or open EEG |
| **EEG** | Name bands (µ/α/β/γ), artifacts, montages; use filter banks deliberately |
| **Physics** | Give dipole / volume-conduction intuition for why scalp EEG is blurry |
| **Math** | Covariance / Riemannian *primer* level; not a full differential-geometry course |
| **Firmware / embedded** | Sketch acquisition → buffer → filter → packet → decoder stub on MCU-class constraints (AArch64-friendly, reuse Edge) |

Does **not** mint a clinical neurophysiologist or implant surgeon. Complements Edge on-device ML.

---

## 2. Relation to Edge ML Mage & Mago Supremo

| Concern | Rule |
|---------|------|
| **Mago Supremo** | Unchanged: Systems craft runes + Edge on-device evidence (`gamification.ts`). Neurotech **must not** soft-gate or replace those runes. |
| **Parallel circle** | Neurotech XP / grimório skills / `rune-neuro-*` live in a **parallel** progress slice (same UX patterns, separate course id). |
| **Shared rooms** | May credit shared cores (`amostragem`, `adc-potencia`, `intro-asm`, Edge latency rooms) via `room_id` — same as Systems↔Edge. |
| **AArch64** | Deep ISA still Edge/BCI path; Neurotech firmware rooms point to Edge `aarch64-abi` / CMSIS rather than duplicating ISA farms. |

Suggested Neuro ranks (course-internal, XP + rituals):  
**Novice → Signal Adept → Decode Adept → Closed-Loop Adept → Neuro Mage** (final ritual = online loop stub artifact **or** paper-module evidence).

Suggested runes (do not collide with `rune-llvm-pass` / Edge on-device):

| Rune id | Gate |
|---------|------|
| `rune-neuro-acq` | Checkpoint: acquisition / filter-bank project slice |
| `rune-neuro-decode` | Checkpoint: MI decoder MVP or Riemannian toy |
| `rune-neuro-online` | Ritual: online loop stub + latency budget write-up |

---

## 3. Pedagogy contract

| Layer | Content |
|-------|---------|
| **Estuda** | `story.md` + `concept.md` + `lesson.md` (+ animation when it teaches) |
| **Sala** | `room.yaml` tasks: mcq / fill / numeric / code / emulator hooks |
| **Checkpoint** | Whole paper **or** paper module (reproduce figure / reimplement Methods slice) **or** whole/partial real project |
| **Boss / ritual** | Artifact under `study-log/artifacts/` (e.g. `neuro-online-loop.md`) |

Emulators and animations: **teach or omit**.

---

## 4. Phase map (F0…F6)

Hours assume ~4–6 h/week. Totals ≈ **35–55 h** study (±), **2–4 months** calendar — Edge-README duration style.

| Phase | Title | Hours (±) | Focus | Owner agents |
|-------|-------|-----------|-------|--------------|
| **F0** | Portal & ethics | 2–3 | What BCI is / isn’t; consent; Estuda→Sala habit | pedagogo + bci |
| **F1** | Physics & tissue lite | 4–6 | Dipole, volume conduction, spike→LFP | fisica + neurociencia |
| **F2** | Acquisition chain | 5–8 | Electrodes, SNR, filters, ADC, grounding | neuroeng + eletrica |
| **F3** | EEG rhythms & paradigms | 5–7 | α/β/γ/µ, MI/SSVEP lite, artifacts | neurociencia + bci |
| **F4** | Decode offline | 6–10 | Features, CSP/Riemannian primer, metrics | bci (+ math spiral) |
| **F5** | Firmware & edge stub | 5–8 | Buffers, filter bank on device, latency | eletrica + bci (+ Edge reuse) |
| **F6** | Online loop & checkpoints | 6–10 | Simulated online, paper/project rituals | pedagogo + bci + neuroeng |

### Room stubs (ids · titles · owner)

Format: `room-id` — Title — **owner**

**F0**
- `nt-portal` — Portal do círculo Neural — **pedagogo+bci**
- `nt-ethics-consent` — Ética, consentimento, limites — **bci+pedagogo**

**F1**
- `nt-dipole-scalp` — Dipolo → potencial de escalpo — **fisica**
- `nt-spike-lfp` — Spike → LFP (intuição) — **fisica+neurociencia**
- `nt-volume-blur` — Condução de volume e borrão espacial — **fisica**

**F2** (cadeia via `requires_rooms`: eletrodo → terra/ref → ADC → filter-bank)
- `nt-electrode-snr` — Eletrodo, impedância, SNR — **neuroeng**
- `nt-ground-ref` — Terra, referência, 50/60 Hz — **eletrica+neuroeng**
- `nt-adc-bio` — ADC e escala µV — **eletrica**
- `nt-filter-bank` — Banco de filtros EEG — **eletrica** (após ritmos + ADC)

**F3**
- `nt-rhythms` — Ritmos α/β/γ/µ — **neurociencia** (pode vir antes do filter-bank para intuição de banda)
- `nt-mi-paradigm` — Imagética motora (paradigma) — **bci+neurociencia**
- `nt-artifacts` — Artefatos (EOG/EMG/movimento) — **bci+eletrica**

**F4**
- `nt-features-bandpower` — Potência de banda / covariância — **bci**
- `nt-riemann-primer` — Primer Riemanniano (SPD toy) — **bci**
- `nt-metrics-offline` — Acurácia, κ, vazamento de trial — **bci**

**F5**
- `nt-stream-buffer` — Stream sintético e ring buffer — **bci+eletrica**
- `nt-mcu-filter` — Filter bank embutido (stub) — **eletrica**
- `nt-latency-budget` — Orçamento de latência closed-loop — **neuroeng+bci**

**F6**
- `nt-online-stub` — Loop online simulado — **bci**
- `nt-checkpoint-paper` — Ritual módulo de paper — **pedagogo+bci**
- `nt-checkpoint-project` — Ritual fatia de projeto — **pedagogo+neuroeng**
- `nt-neuro-mage` — Boss Neuro Mage — **pedagogo**

**Shipped rooms (F0→F6 catalog):** all stubs in §4 authored under `content/tracks/10-neurotech/rooms/` (22 salas). Pedagogical path: F2 acquisition order eletrodo→ground→ADC→filter; `nt-rhythms` may precede filter-bank for band intuition. **Checkpoints:** paper module **or** project slice (parallel); Neuro Mage evidence = online stub + one of the two — not both required.

**Neurological clinical case rooms:** none invented. Only literature-backed MI/artifact/benchmark paradigms (see §7). Rejected fake “patient diagnosis” rooms without public solved-case URLs.

---

## 5. Emulator concepts

| Emulator id | Teaches | Notes |
|-------------|---------|-------|
| `synth_eeg_stream` | Multichannel colored noise + band-energy probes (µ-burst / suppression) | **Didactic µV-scale**; probes ≠ physiological MI/ERD · **shipped** `edge_mage/emulators/synth_eeg.py` |
| `artifact_inject` | Blink / EMG / line noise overlays | **shipped** `edge_mage/emulators/artifact_inject.py` |
| `cortex_m_stub` | ADC → ring buffer → FIR → UART packet + latency | **Python host stub** (Cortex-M *class* mental model) — **not QEMU / not CMSIS runtime**; splits `window_ms` vs `compute_ms` · **shipped** `edge_mage/emulators/cortex_m_stub.py` |
| `latency_budget` | Pipeline stages with ms costs | Exercised via Cortex stub `deadline_ms` + room `nt-latency-budget` |
| `impedance_probe` | Contact quality → SNR slider | **Stub / not shipped UI** — honesty note in `nt-electrode-snr` (numeric SNR task instead) |
| `spd_toy` | 2×2 or small SPD covariances on a grid | Conceptual in `nt-riemann-primer` |

CLI: `mage emu all` · `python -m edge_mage.emulators [synth|artifact|cortex|all]`

No real human data required for MVP; optional OpenBCI live path later as elective.

---

## 6. Animation list (describe only)

| Animation id | What learner sees | Room hooks |
|--------------|-------------------|------------|
| `filter_freq_response` | Magnitude curve; poles/zeros lite; band highlight | `nt-filter-bank` |
| `dipole_field` | Current dipole under skull layers → scalp map | `nt-dipole-scalp` |
| `spike_to_lfp` | Spike train → synaptic current → slower LFP trace | `nt-spike-lfp` |
| `rhythm_bands` | Time series with α/β/γ overlays | `nt-rhythms` |
| `mi_erds` | Cartoon ERD/ERS over motor cortex | `nt-mi-paradigm` |
| `closed_loop_timeline` | Sense → decide → act bars vs deadline | `nt-latency-budget`, `nt-online-stub` |
| `volume_blur` | Fine source map vs smeared scalp | `nt-volume-blur` |

---

## 7. Sample checkpoint table (real open sources)

| Checkpoint | Type | Evidence | Primary sources |
|------------|------|----------|-----------------|
| **CP-MI review map** | Paper module | 1-page map of MI-BCI pipeline stages from a review | [Alzahab et al., Sensors 2021 (MDPI)](https://www.mdpi.com/1424-8220/21/6/2173) · [Padfield et al., Sensors 2019 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/) |
| **CP-Riemann figure** | Paper module | Reproduce SPD / distance intuition figure or toy MDRM on synthetic cov | [Yger et al. review (HAL PDF)](https://inria.hal.science/hal-01394253/document) · [Congedo et al. 2017 primer](https://www.tandfonline.com/doi/full/10.1080/2326263X.2017.1297192) · [arXiv:2407.20250](https://arxiv.org/abs/2407.20250) |
| **CP-OpenBCI chain** | Project slice | Document Cyton/GUI → stream → file; or synthetic stand-in + cite setup | [Cyton Getting Started](https://docs.openbci.com/GettingStarted/Boards/CytonGS/) · [EEG Setup](https://docs.openbci.com/GettingStarted/Biosensing-Setups/EEGSetup/) |
| **CP-Filter bank** | Project slice | Implement bandpower features for µ/β on synth EEG; tests in harness | OpenBCI docs + F3/F4 rooms |
| **CP-Decoder MVP** | Project slice | Offline MI binary classify on open or synth set; report κ + no trial leak | MI reviews above |
| **CP-Online stub** | Project slice | Sliding window → feature → label → latency log artifact | Emulator `latency_budget` |
| **CP-Firmware driver** | Project slice | Ring buffer + stub SPI/UART packet parse (no unsafe hardware required) | Edge ADC rooms + F5 |

Artifact template fields (ritual): `paper_or_project`, `url`, `what_reproduced`, `metrics`, `latency_ms` (if online), `limits`.

---

## 8. Estimated duration (README style)

| Slice | Study hours (±) | Calendar (±) |
|-------|-----------------|--------------|
| F0–F1 Portal + physics | 6–9 h | 1–2 weeks |
| F2–F3 Acquisition + rhythms | 10–15 h | 3–5 weeks |
| F4 Decode offline | 6–10 h | 2–3 weeks |
| F5–F6 Firmware + online + rituals | 11–18 h | 4–8 weeks |
| **Neurotech full** → Neuro Mage | **~35–55 h** | **~2–4 months** |

Faster with Edge ML already done (shared sampling/ADC/latency intuition).

---

## 9. Rank / rune hooks (e-mage compatible)

```text
e-mage global:  Mago base → … → Mago Supremo   (UNCHANGED hardcore)
neurotech:      parallel courseProgress.neurotech + rituals neuro-*
```

Implementation (landed):

- TUI course id `neurotech` in `edge_mage/courses.py` + launcher + `mage --course neurotech`.
- Grimório: `content/grimoire/skills.yaml` entries `neuro-…` (+ elite `neuro-mage`).
- Web Estudo: fourth course `/estudo/cursos/neurotech` + `content/estudo/neurotech/export.json` (soft-gate Mago base like Edge).
- **Never** require Neurotech rituals for Mago Supremo.

---

## 10. MVP implementation order (YAML rooms first)

Build in this order so Estuda→Sala and emulators land early:

1. **Track skeleton** `10-neurotech/track.yaml` + README  
2. **`nt-portal`** — pedagogo+bci (habit + ethics teaser)  
3. **`nt-rhythms`** — neurociencia (bands; animation `rhythm_bands`)  
4. **`nt-filter-bank`** — eletrica (animation `filter_freq_response`; hooks emulator later)  
5. Emulator MVP: `synth_eeg_stream` + `artifact_inject` (code in TUI later)  
6. **`nt-mi-paradigm`** + **`nt-features-bandpower`**  
7. **`nt-stream-buffer`** + **`nt-latency-budget`**  
8. Checkpoints CP-Filter bank → CP-Decoder MVP → **`nt-online-stub`** ritual  
9. Wire course launcher + grimoire + optional web export  
10. Remaining F1/F2/F4 rooms + paper checkpoint boss  

---

## 11. Content layout

```text
content/tracks/10-neurotech/
  README.md
  track.yaml
  rooms/
    01-nt-portal/
    02-nt-rhythms/
    03-nt-filter-bank/
    …
docs/SPEC-neurotech-course.md   ← this file
```

Each room: `story.md` · `concept.md` · `lesson.md` · `room.yaml`.

---

## 12. Safety & scope

- Educational noninvasive BCI and synthetic data by default  
- No pathogen / weapon / DIY invasive implant instructions  
- Ethics rooms required before any “live human optional” elective  
- Clinical claims forbidden; research literacy encouraged  

---

## 13. Definition of done (SPEC)

- [x] Phase map with room stubs and owners  
- [x] Emulator + animation lists  
- [x] Checkpoint table with real URLs  
- [x] Hours estimate  
- [x] Rank/rune parallel-circle rules  
- [x] MVP YAML order  
- [x] Full room catalog authored (F0→F6, 22 salas)  
- [x] TUI course id + web pack (`neurotech` export + launcher)  
- [x] Emulator MVP: `synth_eeg_stream` + `artifact_inject` + `cortex_m_stub`  

