# Lição — Welch / vazamento

## Parâmetros

- `nperseg` / duração do segmento → Δf
- `noverlap` → estabilidade vs independência
- janela Hann/Hamming reduz vazamento

## Em lab

`synth_eeg_stream` + band-energy probes; **não** reivindique fisiologia.

## Fontes

- scipy.signal.welch docs
- Nunez / Michel volume conduction context — DOI [10.3389/fnins.2019.00666](https://doi.org/10.3389/fnins.2019.00666) (Michel & Brunet OA path)
