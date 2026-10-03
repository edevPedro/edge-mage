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

**Guided study estimate (required path):** **~210–360 h** (F0-found + foundation→advanced em todos os pilares + Estuda denso + labs + research rituals).  
Calendar: **~10–16 months** at 5–8 h/week (multi-year band OK at lower weekly load). Electives extra (+10–18 h).

**Honesty:** pisos antigos (50–60 h / 75–110 h / 120–200 h) **não** descrevem este catálogo. Com base matemática/física completa (trig→cálculo→complexos→Fourier), EE completa (circuitos→semicondutores→AFE→PCB/EMI→shield/PI), física eletrostática, neuro sistemas, CS/FW realtime e espinha BCI, o claim sobe. **Nunca** recalibrar para baixo. Média ponderada ≈ **2,4–4,0 h/sala** × 92 required.

| Phase | Title | Rooms (±) | Hours (±) | Estuda depth | Focus |
|-------|-------|-----------|-----------|--------------|--------|
| **F0-found** | Fundamentos pré-MSc | **18** | **30–50** | full | Trig, exp/log, cálculo, complexos, Fourier, ondas, energia/potência, fasores, filtros, fonte de alimentação, amostragem, anatomia neuronal, sistema EEG, binário/bits, C essencial, modelo de memória, classificador linear |
| **F0** | Portal & ethics | 2 | 6–10 | full | Estuda→Sala; Belmont; consent; dual-use literacy |
| **F1-math** | Math foundations→advanced | 6 | 14–22 | standard→full | Vectors→matrices→eigen→prob→estimation→GD (CSP/Riemann-ready) |
| **F2-physics** | Physics foundations→advanced | 6 | 14–22 | standard | Electrostatics→dipole→RC→LFP→blur→field |
| **F3-elec** | Electrical foundation→advanced | **10** | **28–42** | standard→full | Ohm/KCL→semi→electrode→ref→opamp→**INA/DRL**→ADC→antialias→**PCB/EMI**→**shield/PI** |
| **F4-neuro** | Neuroscience foundations→systems | 6 | 14–22 | standard→full | HH→synapse→rhythms→maps→plasticity→**systems BCI** |
| **F5-cs** | CS foundations→realtime | 5 | 12–18 | standard | Complexity→ringbuf→numerics→harness→**RT testing** |
| **F6-dsp** | DSP / acquisition | 4 | 12–18 | full/standard | Filter-bank, Welch, FIR/IIR, artifacts |
| **F7-paradigm** | Paradigms | 3 | 10–14 | full/standard | MI, bandpower, trial design |
| **F8-decode** | Decode / ML | 8 | 22–34 | full/standard | Stats, power, CV, LDA, CSP, Riemann, ML |
| **F9-fw** | Firmware / online | 9 | 20–32 | standard | Stream, IRQ/DMA, MCU, Q15, bridge, **RT constraints**, latency, online, closed-loop |
| **F10-mage** | Neuro Mage | 3 | 8–12 | standard (ritual) | Paper XOR project + boss marco |
| **F11-apps** | Applications | 3 | 8–12 | standard | Assistive, NFB, P300 (published literacy) |
| **F12-cases** | Emulated published cases | 2 | 8–12 | full | Berlin MI; BCI Competition IV walkthroughs |
| **F13-research** | Thesis-prep | 6 | 20–32 | full/standard | IRB, critique, proposal, Methods, project, paper MSc |
| **F14-supremo** | Climax | 1 | 4–8 | standard (ritual) | Boss **Mago Supremo** (rota Neural) |
| **elective** | SSVEP / FBCSP / OpenBCI | 3 | +10–18 | standard (real Estuda) | Optional depth |

**Catalog:** **95** rooms (**92** required + 3 electives), incluindo **18 salas F0-found de fundamentos pré-MSc**.  
**Required total (sum of phase bands):** roughly **~210–360 h** guided; electives on top.

### F0-found — Salas de fundamentos (18 salas novas)

| id | Pillar | Pré-requisito de |
|----|--------|------------------|
| `nt-found-units-scales` | math | todas |
| `nt-found-trig` | math | física, DSP, eletrostática |
| `nt-found-exp-log` | math | ruído, filtros RC, probabilidade |
| `nt-found-calculus` | math | gradiente descendente, campos |
| `nt-found-complex-euler` | math | impedância AC, Fourier, filtros |
| `nt-found-fourier` | math | DSP, banco de filtros, Welch |
| `nt-physics-waves` | physics | EEG ritmos, superposição, DSP |
| `nt-physics-energy-power` | physics | SNR, PSD, ruído de AFE |
| `nt-elec-ac-phasors` | electrical | op-amp, INA, filtros analógicos |
| `nt-elec-filters-intro` | electrical | banco de filtros, FIR/IIR |
| `nt-elec-power-supply` | electrical | PCB/EMI, shielding |
| `nt-dsp-sampling` | dsp | banco de filtros, aliasing |
| `nt-neuro-cell-anatomy` | neuroscience | HH, sinapse, ritmos |
| `nt-neuro-eeg-system` | neuroscience | montagem, referência, MI-BCI |
| `nt-cs-binary-bits` | cs | Q15, DMA, protocolo SPI |
| `nt-cs-c-basics` | cs | firmware ISR, ponteiros, volatile |
| `nt-fw-memory-model` | firmware | DMA, IRQ, RT constraints |
| `nt-ml-linear-classifier` | ml | decode MVP, LDA, CSP |

`estuda_depth` tags (`full` \| `standard` \| `lite`) may appear in room YAML as the schema allows; default pedagogical target for required rooms is **standard or full** — not permanent lite stubs.

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
- [x] Hours **180–300 h** guided documented (upward with foundation→advanced EE + pillars; never below MSc-prep band)  
- [x] Reading list with DOIs  
- [x] Thesis-prep checkpoints  
- [x] Alternate Mago Supremo wiring (Edge path preserved)  
- [x] **95** rooms authored (**92** required + 3 electives), incl. **18 salas F0-found de fundamentos pré-MSc** (trig, exp/log, cálculo, complexos/Euler, Fourier, ondas, energia/SNR, fasores AC, filtros, fonte de alimentação, amostragem/Nyquist, anatomia neuronal, sistema EEG/10-20, binário/bits, C essencial, modelo de memória, classificador linear) + EE circuit/semi/INA/PCB/shield + physics/neuro/CS/FW foundation→advanced rooms
- [x] **83** laboratórios de código Python com testes automatizados (65 originais + 18 novos F0-found), cobrindo desde conversão de unidades e funções trigonométricas até LDA 2D regularizado
- [x] Emulators + Estuda→Sala  
- [x] Tests: path length, gates, Supremo from neurotech  

