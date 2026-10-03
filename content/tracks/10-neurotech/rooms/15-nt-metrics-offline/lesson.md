# Lição — Offline honesto

1. Decode **offline** = dataset gravado, sem deadline de loop.
2. Reporte acurácia **e** κ; declare balanceamento de classes.
3. Anti-vazamento: split por trial/sessão; fit de filtros/scalers só no treino.
4. Micro-exemplo: se a feature usa estatística do teste, o número não vale.
5. Sala: calcule κ numérico e nomeie o tipo de vazamento.

## Fontes
- [Padfield et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/)
