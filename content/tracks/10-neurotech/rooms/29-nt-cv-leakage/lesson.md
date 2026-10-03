# Lição — Validação sem vazamento

## Regras

1. Fit scaler/CSP/filtro *dentro* do fold de treino.
2. Nunca optimize no teste.
3. Reporte se a unidade é trial, sessão ou sujeito.

## Fontes

- Lotte et al. DOI [10.1088/1741-2560/4/2/R01](https://doi.org/10.1088/1741-2560/4/2/R01)
- Varoquaux et al. cross-validation — DOI [10.1016/j.neuroimage.2016.10.038](https://doi.org/10.1016/j.neuroimage.2016.10.038)
