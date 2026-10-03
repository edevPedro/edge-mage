# Lição — ADC e escala µV

1. Escreva `fs`, faixa e **µV/LSB** (ou ganho) em todo lab — sem isso o inteiro é opaco.
2. Micro-exemplo: faixa total 200 000 µV em 2²⁴ níveis → µV/LSB ≈ 0.0119. Documente se a unidade do arquivo é µV ou counts.
3. Anti-alias antes de subamostrar; respeite Nyquist.
4. O `synth_eeg` do curso usa **µV didáticos** (ordem de grandeza de escalpo), não calibração clínica.
5. Reuse intuição Edge/Systems de ADC quando disponível.

## Fontes
- OpenBCI Cyton: https://docs.openbci.com/GettingStarted/Boards/CytonGS/
