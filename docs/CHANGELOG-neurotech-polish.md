# CHANGELOG — Neurotech polish pass (full course)

Follow-up to P0 panel (`CHANGELOG-neurotech-p0.md`). Goal: polished **full course**, not a thin complement.

## Landed

### Pedagogy / path
- Renamed `NN-` folders to pedagogical order; every room has YAML `order`
- Loader sorts by `order`; loads `requires_rooms` + `requires_rooms_any`
- TUI unlock **enforces** room prerequisites (messages in room list / `:open`)
- F2 chain locked: electrode → ground → ADC → rhythms → filter → MI…
- F6: online → paper ∥ project → boss (`requires_rooms_any`)
- Test `test_neurotech_pedagogical_order_locked` + unlock/gate tests

### BCI / content
- New room **`nt-decode-mvp`** (labels → bandpower/cov → LDA toy → κ + code)
- SSVEP / deep CSP marked **elective** in SPEC (with Ang FBCSP DOI + Riemann cites)
- `mi_erds`: ERS rebound **above** baseline (matches header)
- Dual-use literacy MCQ; plasticity/calibration MCQ; laterality C3 fill
- Estuda thickened (ethics, volume, MI, F4–F6)

### Neuroeng / firmware
- MCU room renamed/clarified: MA/FIR host stub **≠** MI filter-bank / FBCSP
- Deadline-class disclaimer (MI feedback vs hard-RT 40 ms stress)
- sense/decide/act ↔ window_ms / compute_ms / act_ms tasks
- `latency_budget` thin wrapper → cortex stub; `online_loop` end-to-end stub
- Honest emulator metadata in demos / SPEC

### Physics / EE / anims
- `volume_blur` honesty (cartoon ≠ FEM) + thicker Estuda
- `artifact_trace` anim (artifacts ≠ `rhythm_bands`)
- Non-MCQ tasks present F2+; richer citations (PMC/DOI/OpenBCI/docs)

### Product
- `edevs` export v2 synced (23 rooms + pathNote + emulators)
- Grimório `neuro-decode` → `nt-decode-mvp`
- Web hub copy updated for full-path course

## Remaining gaps (honest)
- Live OpenBCI path still elective / not shipped as room
- `impedance_probe` UI slider still stub
- Full CSP vs Riemann bake-off room not authored (elective by design)
- SSVEP short room not authored (elective by design)
- Domain skills `agent-neurociencia` / `agent-eletrica` / `agent-fisica` were absent on disk at polish time
