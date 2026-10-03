# Desafio — Avaliação Estatística: Cohen's Kappa e Wolpaw ITR

## 1. Objetivo do Desafio
Implementar a Taxa de Transferência de Informação de Wolpaw (ITR) e o cálculo formal do coeficiente Kappa de Cohen a partir de rótulos verdadeiros e preditos, garantindo a avaliação livre de viés de classificadores neurais.

## 2. Especificação Técnica e Formulação
1. **Fórmula de Wolpaw ITR:** Implemente `wolpaw_itr(n_classes, accuracy, trials_per_min)`. Se $\text{accuracy} = 1.0$, o retorno é simplesmente $M \cdot \log_2(N)$. Caso contrário, aplique a entropia condicional clássica de canal simétrico.
2. **Cálculo de Kappa:** Implemente `calculate_cohen_kappa(y_true, y_pred)` calculando:
   - $p_o$: Acurácia observada (fração de acertos).
   - $p_e$: Concordância esperada ao acaso pela multiplicação das frequências marginais de cada classe.
   - $\kappa = (p_o - p_e) / (1 - p_e)$. Se $p_e = 1.0$, retorne zero.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que se o modelo sempre previr a mesma classe fixa para dados balanceados, o Kappa colapsa estritamente para zero ($0.0$).
- Lembre-se: em avaliações offline honestas, o pré-processamento e o treino nunca devem acessar dados do fold de teste.
