# Lição — Decode MVP

## Pipeline

```text
trials + labels → bandpower/cov → LDA (toy) → κ / acurácia
```

- **Offline:** dataset completo disponível; sem deadline de feedback.
- **κ:** `(p_o - p_e) / (1 - p_e)`. Em 2 classes equilibradas, `p_e = 0.5`.
- **LDA toy:** score linear; classe 1 se `sum(w_i x_i) + b ≥ 0`.

## Checkpoint ligado

**CP-Decoder MVP** (SPEC §7): classificar binário em synth/open EEG, reportar κ,
documentar ausência de trial leak. Fontes: Padfield (PMC), Singh et al. (PMC8003721),
Lotte et al. (DOI na sala).

## Ferramentas (lab real)

- sklearn: `LinearDiscriminantAnalysis`, `cohen_kappa_score` (links na sala)
- MNE-Python para I/O / pré-processamento EEG (não obrigatório no TUI sandbox)

## Emulator

`synth_eeg_stream` — gerar contraste de band-energy; **não** é ERD fisiológico.
