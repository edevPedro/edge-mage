# Desafio — Detecção e Sinalização de Artefatos de Amplitude

## 1. Objetivo do Desafio
Implementar um algoritmo de triagem de artefatos por limiar de amplitude absoluta para identificar amostras contaminadas por piscadas de olhos (EOG), saturação de eletrodo ou picos de ruído de rede.

## 2. Especificação Técnica e Formulação
Dado um array ou lista de amostras de sinal contínuo $S = [s_0, s_1, \dots, s_{N-1}]$ e um limiar escalar positivo `threshold` (em microvolts):
- Implemente a função `flag_artifacts(samples, threshold)` que retorna uma lista booleana com o mesmo número de elementos, onde cada posição é `True` se $|s_i| > \text{threshold}$ e `False` caso contrário:
  $$\text{flags}[i] = (|s_i| > \text{threshold})$$

## 3. Critérios de Validação e Armadilhas
- Utilize sempre o valor absoluto da amplitude $|s_i|$, pois artefatos de piscada e eletrodo solto produzem deflexões tanto positivas quanto negativas.
- Lembre-se: em sinais biológicos de escalpo em repouso, amplitudes acima de $100\ \mu\text{V}$ são fortíssimas indicadoras de contaminação não-neural.
