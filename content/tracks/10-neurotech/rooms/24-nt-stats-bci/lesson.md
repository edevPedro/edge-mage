# Lição — Stats para BCI

## Níveis

| Nível | Exemplo | Erro comum |
|-------|---------|------------|
| Trial | janela 2 s | tratar amostras de tempo como N independente |
| Sessão | um dia de gravação | “p-hackear” bandas até κ subir |
| Sujeito | leave-one-subject-out | generalizar de 1 pessoa |

## Fórmulas úteis

- κ = (p_o − p_e)/(1 − p_e)
- Para 2 classes equilibradas, p_e = 0,5
- Erro binomial (intuição): SE ≈ √(p(1−p)/N) na acurácia

## Fontes

- Lotte et al. classificação EEG-BCI — DOI [10.1088/1741-2560/4/2/R01](https://doi.org/10.1088/1741-2560/4/2/R01)
- Schlögl et al. κ em BCI — DOI [10.1088/1741-2560/2/4/L02](https://doi.org/10.1088/1741-2560/2/4/L02)
