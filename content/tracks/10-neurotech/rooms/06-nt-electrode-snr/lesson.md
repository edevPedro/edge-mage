# Lição — Contato e SNR

1. Meça/relacione qualidade de contato antes de culpar o modelo.
2. SNR é orçamento: sinal útil vs artefato/ruído. Em dB: ≈ 20·log₁₀(A_sinal/A_ruído) para amplitudes RMS.
3. Micro-exemplo: 10 µV de ritmo útil sobre 5 µV de ruído → SNR linear 2 ≈ 6 dB — decode fica difícil.
4. **Honestidade de ferramenta:** o emulador `impedance_probe` está no SPEC como conceito; **ainda não há UI/slider shipped**. Nesta sala use raciocínio numérico + docs OpenBCI; synth EEG para labs de ruído depois.

## Fontes
- OpenBCI [EEG Setup](https://docs.openbci.com/GettingStarted/Biosensing-Setups/EEGSetup/)
