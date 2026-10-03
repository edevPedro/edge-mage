# Lição — Filter bank para EEG

## Objetivos

1. Dado `fs`, respeitar Nyquist ao escolher bandas.
2. Montar um banco toy mu/beta para MI.
3. Separar pré-processamento de classificação; evitar trial leak.
4. Correr o emulador synth e inspecionar potência por banda.

## Passos

1. Calcule Nyquist para `fs ∈ {128, 250, 512}`.
2. Proponha banco: `(8–12)`, `(16–24)`, opcional `(24–30)`. Justifique com ritmos.
3. Escreva a ordem: raw → (notch?) → bandpass_i → power_i → concat features.
4. Liste 2 jeitos de vazar informação no pré-proc (ex.: z-score global com teste; escolher banda olhando labels do teste).
5. Rode o emulador (abaixo) e anote um número de potência por banda.

Para destravar o lab, abra [Ang et al. — Filter Bank Common Spatial Pattern (FBCSP) IEEE](https://doi.org/10.1109/IJCNN.2008.4634130) e leia a construção do filter bank no FBCSP de Ang (sub-bandas antes do CSP) para escolher o banco toy (8–12) e (16–24) Hz.

## Labs

**Numeric.** `fs=250`. Qual a máxima frequência teórica representável? Se o banco inclui 70–90 Hz, o que falta na cadeia EE?

**Code (sandbox / mental).** Pseudo:

```text
for band in [(8,12), (16,24)]:
  y = bandpass(x, fs, *band)
  feat.append(log(var(y) + eps))
```

Compare `feat` entre canais C3/C4 em duas classes synth.

## Runa

Limpar esta sala dropa **`rune-neuro-acq`**.

## Emulador

```bash
python -m edge_mage.emulators synth
mage emu synth
```
