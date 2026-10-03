# Lição — Artefatos no pipeline

1. Nomeie fontes: EOG, EMG, movimento, linha 50/60 Hz.
2. Separe *detecção/rejeição* de trial vs *robustez* do modelo.
3. Micro-exemplo: `artifact_inject` com `kind=line` eleva potência ~60 Hz — compare com `detect_line_power`.
4. Em MI, rejeitar trials com blink extremo é comum; fingir que não existem não é.
5. Estuda → Sala: rode `mage emu artifact` antes de culpar o classificador.

## Fontes
- Contexto MI / desafios: [Padfield et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/)
