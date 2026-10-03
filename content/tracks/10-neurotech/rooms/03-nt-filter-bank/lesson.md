# Lição — Filter bank para EEG

1. Dado `fs`, a banda útil deve respeitar Nyquist.
2. Para un MI toy: passe-banda mu e/ou beta → potência (ou variância) por canal.
3. Separe **pré-processamento** de **classificação**; vazamento de trial invalida o número.

## Checkpoint futuro

Projeto fatia **CP-Filter bank** (SPEC §7): implementar bandpower em EEG sintético com testes.

## Leituras

- OpenBCI [EEG Setup](https://docs.openbci.com/GettingStarted/Biosensing-Setups/EEGSetup/)
- Riemannian / covariâncias: [HAL Yger et al.](https://inria.hal.science/hal-01394253/document)
