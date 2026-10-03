# SPEC — Neurotech course (e-mage) · MSc-prep

Course id: **`neurotech`** — sibling to **Edge ML Mage** (`edge`), with an **alternate route to Mago Supremo**.  
Product: **e-mage** · `content/tracks/10-neurotech/` · web: edevs `/estudo/cursos/neurotech`.

**Pedagogy (mandatory):**

```text
Estuda (lição + história + animação/conceito) → Sala (lab / FLAG / emulator tasks)
```

Agents: `agent-pedagogo` + `agent-bci` · `agent-neuroeng` · `agent-eletrica` · `agent-fisica` · `agent-neurociencia`.

---

## 1. Goals (master’s-prep, not BCI-only survey)

A learner who finishes the **required path** (climax **Mago Supremo** via Neurotech) can:

| Pillar | Outcome |
|--------|---------|
| **Math** | Vectors/matrices/eigen, probability, estimation, GD lite — quantitative labs |
| **Physics** | Dipole, RC tissue, spike→LFP, volume blur, field distance intuition |
| **Electrical** | Electrode/SNR, ground/ref, op-amp noise/CMRR, ADC µV, Nyquist/anti-alias |
| **Neuroscience** | HH lite, synapse/PSP, rhythms, cortical maps 10–20, plasticity/co-adaptation |
| **CS** | Complexity vs deadline, ring buffer, numerics, test harness |
| **Firmware / Embedded** | IRQ/DMA, MCU filter stub, Q15, AArch64/Edge bridge, latency budget |
| **BCI applications** | Offline→online decode, assistive/NFB/P300 literacy (non-clinical) |
| **Cases** | Emulate **published** paradigms (Berlin MI, BCI Comp IV) — no invented patients |
| **Research** | IRB literacy, paper critique, proposal, Methods, mini-project, paper module MSc |

Does **not** mint a clinician or implant surgeon. Educational **noninvasive** BCI only.

---

## 2. Relation to Edge ML Mage & Mago Supremo

| Concern | Rule |
|---------|------|
| **Rota Edge (inalterada)** | Systems craft + Edge on-device + shared math → `mago_supremo` |
| **Rota Neurotech (alternativa)** | Mago base + 3 runas neuro + Neuro Mage + `rune-neuro-research` + paper-module-msc + ritual `neuro-supremo` → **mesmo** `mago_supremo` |
| **Neuro Mage** | Marco intermediário (não é o ápice global) |
| **Shared / Edge reuse** | AArch64 profundo fica no Edge; Neurotech faz ponte (`nt-fw-aarch64-bridge`) |
| **Edge-only players** | Sem regressão: on-device path intacto |

### Supremo checklist (Neurotech)

```text
mago_base
  ∧ rune-neuro-acq ∧ rune-neuro-decode ∧ rune-neuro-online
  ∧ neuro-mage
  ∧ rune-neuro-research ∧ neuro-paper-module-msc
  ∧ neuro-supremo   # boss nt-mago-supremo
→ mago_supremo
```

TUI: `ProgressStore.has_neuro_supremo_path()` · `global_rank_from_flags(has_neuro_supremo=…)`.  
Web: `evaluateSupremoEvidence` + rooms/rituals sync (edevs).

---

## 3. Pedagogy contract

| Layer | Content |
|-------|---------|
| **Estuda** | `story.md` + `concept.md` + `lesson.md` (+ animation when it teaches) |
| **Sala** | `room.yaml` tasks: mcq / fill / numeric / code / ritual |
| **Checkpoint** | Paper module **or** project slice with real DOI/URL |
| **Boss / ritual** | Artifact under `study-log/artifacts/` |

Emulators: **teach or omit**.

---

## 4. Phase map (MSc) + hours

**Guided study estimate (required path):** **~120–200 h** (≈ 2.5–3.5 h/room × 65 salas + reading/research rituals).  
Calendar: **~4–8 months** at 5–8 h/week. Electives extra.

| Phase | Title | Rooms (±) | Hours (±) | Focus |
|-------|-------|-----------|-----------|--------|
| **F0** | Portal & ethics | 2 | 3–5 | Estuda→Sala; consent; dual-use literacy |
| **F1-math** | Math foundations | 6 | 12–18 | Vectors→matrices→eigen→prob→estimation→GD |
| **F2-physics** | Physics foundations | 5 | 10–15 | Dipole, RC, LFP, blur, field |
| **F3-elec** | Electrical / AFE | 5 | 10–16 | Electrode→CMRR→ADC→Nyquist |
| **F4-neuro** | Neuroscience | 5 | 10–15 | HH, synapse, rhythms, maps, plasticity |
| **F5-cs** | CS foundations | 4 | 8–12 | Complexity, ringbuf, numerics, harness |
| **F6-dsp** | DSP / acquisition | 4 | 8–14 | Filter-bank, Welch, FIR/IIR, artifacts |
| **F7-paradigm** | Paradigms | 3 | 6–10 | MI, bandpower, trial design |
| **F8-decode** | Decode / ML | 8 | 16–28 | Stats, power, CV, LDA, CSP, Riemann, ML |
| **F9-fw** | Firmware / online | 8 | 14–24 | Stream, IRQ/DMA, MCU, Q15, bridge, online, closed-loop |
| **F10-mage** | Neuro Mage | 3 | 6–10 | Paper XOR project + boss marco |
| **F11-apps** | Applications | 3 | 6–10 | Assistive, NFB, P300 (published) |
| **F12-cases** | Emulated published cases | 2 | 6–10 | Berlin MI; BCI Competition IV |
| **F13-research** | Thesis-prep | 6 | 16–28 | IRB, critique, proposal, Methods, project, paper MSc |
| **F14-supremo** | Climax | 1 | 4–8 | Boss **Mago Supremo** (rota Neural) |
| **elective** | SSVEP / FBCSP / OpenBCI | 3 | +6–12 | Optional |

**Catalog:** **68** rooms (65 required + 3 electives).

### Thesis-prep checkpoints

| Gate | Room / ritual | Standard |
|------|---------------|----------|
| Proposal | `nt-research-proposal` | question, hypothesis, data, metric, ethics, timeline |
| Methods | `nt-thesis-methods` | reproducible Methods outline + seeds/versions |
| Project | `nt-research-project` | executed slice → `rune-neuro-research` |
| Paper MSc | `nt-paper-module-msc` | DOI + Methods/figure slice + critique |
| Climax | `nt-mago-supremo` | seals `neuro-supremo` → global Supremo |

### Reading list (core DOIs / OA — verify)

| Topic | Citation |
|-------|----------|
| MI-BCI review | Singh et al. DOI [10.3390/s21062173](https://doi.org/10.3390/s21062173) |
| EEG-MI techniques | Padfield et al. [PMC6471241](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/) |
| Classification | Lotte et al. DOI [10.1088/1741-2560/4/2/R01](https://doi.org/10.1088/1741-2560/4/2/R01) |
| κ / MI | Schlögl et al. DOI [10.1088/1741-2560/2/4/L02](https://doi.org/10.1088/1741-2560/2/4/L02) |
| ERD/ERS | Pfurtscheller & Lopes da Silva DOI [10.1016/S1388-2457(99)00141-8](https://doi.org/10.1016/S1388-2457(99)00141-8) |
| MI S1/M1 | Pfurtscheller & Neuper DOI [10.1016/S0304-3940(97)00889-6](https://doi.org/10.1016/S0304-3940(97)00889-6) |
| CSP | Ramoser et al. DOI [10.1109/86.895946](https://doi.org/10.1109/86.895946) |
| FBCSP | Ang et al. DOI [10.1109/IJCNN.2008.4634130](https://doi.org/10.1109/IJCNN.2008.4634130) |
| Riemannian MDM | Barachant et al. DOI [10.1109/TBME.2011.2172210](https://doi.org/10.1109/TBME.2011.2172210) |
| Berlin BCI | Blankertz et al. [PMC5116473](https://pmc.ncbi.nlm.nih.gov/articles/PMC5116473/) · DOI [10.3389/fnins.2016.00530](https://doi.org/10.3389/fnins.2016.00530) |
| BCI Comp IV | Tangermann et al. DOI [10.1088/1741-2560/9/2/025009](https://doi.org/10.1088/1741-2560/9/2/025009) |
| P300 speller | Farwell & Donchin DOI [10.1016/0013-4694(88)90149-6](https://doi.org/10.1016/0013-4694(88)90149-6) |
| SSVEP (elective) | Zhu et al. DOI [10.1088/1741-2560/7/4/041001](https://doi.org/10.1088/1741-2560/7/4/041001) |
| Stats MEG/EEG | Combrisson & Jerbi DOI [10.1016/j.jneumeth.2015.03.034](https://doi.org/10.1016/j.jneumeth.2015.03.034) |
| CV pitfalls | Varoquaux et al. DOI [10.1016/j.neuroimage.2016.10.038](https://doi.org/10.1016/j.neuroimage.2016.10.038) |
| HH | Hodgkin & Huxley DOI [10.1113/jphysiol.1952.sp004764](https://doi.org/10.1113/jphysiol.1952.sp004764) |
| LFP | Einevoll [PMC3884846](https://pmc.ncbi.nlm.nih.gov/articles/PMC3884846/) · Buzsáki [PMC4907333](https://pmc.ncbi.nlm.nih.gov/articles/PMC4907333/) |
| Source/blur | Michel & Brunet [PMC6700197](https://pmc.ncbi.nlm.nih.gov/articles/PMC6700197/) |
| BCI principles | Wolpaw DOI [10.1016/j.clinph.2012.01.010](https://doi.org/10.1016/j.clinph.2012.01.010) |
| Neurorights | Ienca & Andorno DOI [10.1186/s40504-017-0050-1](https://doi.org/10.1186/s40504-017-0050-1) |
| Belmont | [OHRP Belmont Report](https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/index.html) |
| OpenBCI | [Cyton GS](https://docs.openbci.com/GettingStarted/Boards/CytonGS/) |
| AFE | [TI ADS1299](https://www.ti.com/lit/ds/symlink/ads1299.pdf) |

---

## 5. Emulators

| Id | Teaches | Status |
|----|---------|--------|
| `synth_eeg_stream` | Multichannel synth + µ probes | shipped |
| `artifact_inject` | Blink/EMG/line | shipped |
| `cortex_m_stub` | ADC→buffer→FIR→UART latency | shipped (host stub) |
| `latency_budget` | sense/decide/act | shipped |
| `online_loop` | window→feature→label→log | shipped |

CLI: `mage emu all`

---

## 6. Ranks & runes

```text
NEURO_RANKS: Novice → Signal Adept → Decode Adept → Closed-Loop Adept → Neuro Mage
GLOBAL:      … → Mago Supremo  ← Edge path OR Neurotech climax
```

| Rune | Drop |
|------|------|
| `rune-neuro-acq` | `nt-filter-bank` (or electrode chain) |
| `rune-neuro-decode` | `nt-decode-mvp` |
| `rune-neuro-online` | `nt-online-stub` |
| `rune-neuro-research` | `nt-research-project` |

---

## 7. Safety & scope

- Educational noninvasive BCI + synthetic/open data by default  
- No pathogen / weapon / DIY invasive implant instructions  
- Neurological **case** rooms only for **published** paradigms/benchmarks  
- Clinical claims forbidden  

---

## 8. How to try

```bash
# TUI
cd edge-mage && mage --course neurotech
mage emu all

# Web
# edevs → /estudo/cursos/neurotech
```

Path: foundations → DSP/decode → firmware/online → **Neuro Mage** → apps → published cases → research → **Mago Supremo**.

---

## 9. Definition of done (SPEC)

- [x] Multi-pillar MSc phase map (Math→…→Supremo)  
- [x] Hours **120–200 h** guided documented  
- [x] Reading list with DOIs  
- [x] Thesis-prep checkpoints  
- [x] Alternate Mago Supremo wiring (Edge path preserved)  
- [x] 68 rooms authored (65 required + 3 electives)  
- [x] Emulators + Estuda→Sala  
- [x] Tests: path length, gates, Supremo from neurotech  
