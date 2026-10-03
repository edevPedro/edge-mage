# CHANGELOG — Neurotech P0 panel pass

Panel reviews: PhD BCI · Firmware · Físico · Elétrico · Pedagogo.

## Landed (P0)

- **MI / ERD↓·ERS↑** in `nt-mi-paradigm` (+ MCQ `erd-dir`); anti-confusion vs synth band-energy probes
- **`synth_eeg`**: didactic µV-scale; bursts labeled band-energy probe (not MI/ERD); `schedule_mu_suppression`
- **`cortex_m_stub`**: `window_ms` vs `compute_ms`; demo/tests miss at ~40 ms; docs = Python host stub (not QEMU / not CMSIS runtime)
- **Anims:** `dipole_field` scalp amps vs θ; `spike_to_lfp` AP→PSP→LFP + “LFP ≠ filtered AP”
- **F2 `requires_rooms`:** electrode → ground/ref → ADC → filter-bank (rhythms may precede filter)
- **`nt-adc-bio`:** µV/LSB numeric; unit honesty
- **`nt-electrode-snr`:** SNR dB numeric; `impedance_probe` honesty (emulator null / stub)
- **Estuda** fleshed for priority thin rooms; checkpoints paper **or** project; non-MCQ (bandpower code, κ numeric, leak fill, online window_ms)

## Deferred (P1/P2)

- **P1** `volume_blur` merge / model limits (Físico) — prefer anim P0s first
- **P1** ship real `impedance_probe` UI slider
- **P1** enforce `requires_rooms` in TUI loader (today metadata + README/SPEC; unlock still XP/order-based)
- **P2** rename room folders `NN-nt-*` to match pedagogical F2 order
- **P2** richer ERS phase in `mi_erds` animation beyond caption/dip cartoon
- **P2** full Estuda polish for remaining non-priority rooms
