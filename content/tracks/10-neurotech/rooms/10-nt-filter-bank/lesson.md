# Lição — Filter bank para EEG

1. Dado `fs`, a banda útil deve respeitar Nyquist.
2. Para un MI toy: passe-banda mu e/ou beta → potência (ou variância) por canal.
3. Separe **pré-processamento** de **classificação**; vazamento de trial invalida o número.

## Runa

Limpar esta sala dropa **`rune-neuro-acq`** no inventário (círculo paralelo).  
Cadeia eletrodo→terra→ADC completa também concede a mesma runa se o filter-bank ainda estiver aberto.

## Leituras

- OpenBCI [EEG Setup](https://docs.openbci.com/GettingStarted/Biosensing-Setups/EEGSetup/)
- Riemannian / covariâncias: [HAL Yger et al.](https://inria.hal.science/hal-01394253/document)


## Emulador

```bash
python -m edge_mage.emulators synth
mage emu synth
```
