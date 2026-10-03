# Lição — CV Aninhado, Vazamento de Dados e Splits em Blocos

## 1. A Anatomia do Vazamento de Dados (Data Leakage)
1. **Seleção Circular de Features (Double Dipping)**:
   A seleção de variáveis ou normalização (z-score, min-max) deve ocorrer **estritamente dentro do conjunto de treino**. Se o teste entrar no cômputo da média ou correlação, as métricas tornam-se epistemicamente inválidas.

2. **Autocorrelação Temporal e Split em Blocos**:
   Dividir amostras aleatoriamente (Shuffle K-Fold) em dados contínuos de séries temporais vaza dependência temporal entre janelas consecutivas. A divisão deve ser realizada em blocos contíguos de ensaios completos (`split_blocked`).

3. **Validação Cruzada Aninhada (Nested Cross-Validation)**:
   - Outer Loop: Mede o desempenho de generalização do sistema.
   - Inner Loop: Realiza a escolha e ajuste de hiperparâmetros (como coeficientes de regularização $\gamma$).

## 2. As Funções de Laboratório Desta Sala
- `split_blocked(n_trials, n_folds)`: Realiza a partição determinística de ensaios em blocos contíguos disjuntos, garantindo que nenhum índice de treino sobreponha o teste.
- `audit_leakage_effect(X, y, train_idx, test_idx)`: Demonstra numericamente o colapso epistemológico gerado pelo vazamento em dados de ruído branco puro contra uma pipeline metodologicamente blindada.

Para destravar o lab, abra [Varoquaux et al. 2017 — assessing prediction](https://doi.org/10.1016/j.neuroimage.2016.10.038) e leia as pegadinhas de cross-validation de Varoquaux (split por trial, não por janela correlacionada) para o lab de vazamento.
