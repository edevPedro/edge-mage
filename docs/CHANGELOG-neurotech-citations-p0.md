# CHANGELOG — Neurotech citations + CS P0 (PhD panel)

Panel: PhD CS + Neurotech + Neuroscience (follow-on to prior BCI/Firmware/Físico pass).

## Landed (P0)

### Citations (verified before write)
- **Sensors 21/2173** attribution: Alzahab → **Singh et al. PMC8003721** (SPEC + all rooms). Alzahab kept only as optional hDL review **PMC7827826** / brainsci DOI (not Sensors 2173).
- **Pfurtscheller & Neuper** → Neurosci Lett 1997 `10.1016/S0304-3940(97)00889-6`
- **Nunez** → `10.1017/S0140525X00003253` (+ Michel PMC6700197 OA in F1 lessons)
- **Neuper imagery** → Cogn Brain Res `10.1016/j.cogbrainres.2005.08.014`
- **Schlögl** → JNE 2005 κ paper `10.1088/1741-2560/2/4/L02` (was wrong Clin Neurophysiol DOI)
- **Blankertz** → Frontiers OA **PMC5116473** (was wrong NeuroImage mouse-brain DOI)
- **F1 lesson resources:** Buzsáki / Einevoll / Michel promoted into Estuda `lesson.md` (not YAML-only)
- **Decode + metrics:** sklearn LDA, `cohen_kappa_score`, MNE docs links
- **Rhythms:** beta framing aligned with ERD↓ (not “ativo = ↑”)

### CS
- **`nt-decode-mvp`:** added `fit-kappa` code task (`fit_threshold_lda` + `cohen_kappa`) so claim↔tasks match
- **`spd_toy`:** `emulator: null` + honesty notes (conceptual / not shipped)

### Pedagogy
- Thickened Estuda for `nt-latency-budget`, `nt-online-stub`, `nt-checkpoint-paper`, `nt-checkpoint-project` (+1 resource each in lesson)

## Deferred
- Ship real `spd_toy` UI/CLI emulator
- Full CSP/FBCSP bake-off rooms
- Broader Estuda polish beyond F5–F6 thin rooms
- Optional Alzahab hDL deep-dive room (bib only for now)
