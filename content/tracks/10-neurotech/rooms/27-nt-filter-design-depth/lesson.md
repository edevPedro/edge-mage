# Lição — Design de filtro (profundidade)

## Atraso FIR

delay_s ≈ (N−1)/(2·fs)

Ex.: N=65, fs=250 → delay ≈ 64/(500) = 0,128 s ≈ 128 ms — material no budget.

## Online

Use filtros causais; declare latência no artefato `neuro-online-loop`.

## Fontes

- scipy.signal.firwin / butter
- OpenBCI filter notes + ADS1299 AFE context
