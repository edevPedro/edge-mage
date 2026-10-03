# Desafio — Atualização de Pesos por Gradiente Descendente (GD Step)

## 1. Objetivo do Desafio
Implementar a regra de atualização paramétrica do Gradiente Descendente para um vetor de pesos e seu respectivo gradiente sob uma taxa de aprendizado fixa.

## 2. Especificação Técnica e Formulação
Dado um vetor de pesos atual `w` de dimensão $D$, o vetor gradiente correspondente `grad` de mesma dimensão, e a taxa de aprendizado escalar `lr`:
- Implemente a função `gd_step(w, grad, lr)`:
  $$w_{\text{novo}}[i] = w[i] - \text{lr} \times \text{grad}[i]$$
  para cada coordenada $i = 0, \dots, D-1$.
- Retorne a lista contendo o novo vetor de pesos atualizado.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que os vetores `w` e `grad` possuam o mesmo comprimento. Caso contrário, levante `ValueError`.
- A subtração é obrigatória: certifique-se de não inverter a operação para adição.
