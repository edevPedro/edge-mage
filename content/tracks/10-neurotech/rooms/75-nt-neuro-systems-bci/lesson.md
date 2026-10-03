# Desafio — Cálculo Numérico de ERD/ERS

## 1. Objetivo do Desafio
Implementar a rotina de quantificação da Dessincronização Relacionada a Eventos (ERD) e Sincronização Relacionada a Eventos (ERS) a partir das potências médias de banda obtidas em épocas de linha de base e de tarefa motora.

## 2. Especificação Técnica
Implemente a função `erd_ers_percent(baseline_power, task_power)`:
- Calcule a variação percentual relativa conforme a convenção de Pfurtscheller:
  $$\text{resultado} = \left( \frac{P_{baseline} - P_{task}}{P_{baseline}} \right) \times 100$$
- Onde:
  - `baseline_power`: Potência espectral média na janela de repouso ($P_{base} > 0$).
  - `task_power`: Potência espectral média na janela ativa de imagética motora ($P_{task} \ge 0$).
- Retorne o valor numérico em ponto flutuante.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que potências de tarefa menores que a baseline resultem em valores estritamente positivos (ERD).
- Quando a potência na tarefa for superior à da baseline, o resultado deve ser naturalmente negativo (ERS).
