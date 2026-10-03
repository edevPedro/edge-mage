# Lição — Acurácia, Cohen's Kappa e Information Transfer Rate (ITR)

## 1. Por que Acurácia Bruta Não Basta
1. **O Desbalanceamento de Classes**:
   Quando as classes possuem proporções diferentes no conjunto de teste, um classificador nulo que prevê exclusivamente a classe majoritária obtém acurácia elevada, mas utilidade zero.

2. **O Coeficiente Kappa de Cohen ($\kappa$)**:
   $$\kappa = \frac{p_o - p_e}{1 - p_e}$$
   - $p_o$: Acurácia observada global.
   - $p_e$: Concordância marginal esperada puramente pelo acaso.
   - $\kappa = 1.0$: Concordância perfeita.
   - $\kappa = 0.0$: Desempenho equivalente ao chute aleatório ou predição cega da classe majoritária.
   - $\kappa < 0$: Desempenho inferior ao acaso (inversão sistemática de rótulos).

3. **Information Transfer Rate (ITR) de Wolpaw**:
   $$B = \log_2(N) + P \log_2(P) + (1-P)\log_2\left(\frac{1-P}{N-1}\right) \quad (\text{bits/ensaio})$$
   $$\text{ITR} = B \times M \quad (\text{bits/minuto})$$
   Permite comparação objetiva entre diferentes tecnologias de BCI (P300, SSVEP, Imagética Motora) levando em conta o número de escolhas possíveis e o tempo necessário para emitir cada decisão.

## 2. As Funções de Laboratório Desta Sala
- `wolpaw_itr(n_classes, accuracy, trials_per_min)`: Computa a capacidade de canal e a taxa de transferência em bits por minuto segundo a formulação de Wolpaw.
- `calculate_cohen_kappa(y_true, y_pred)`: Avalia o coeficiente Kappa a partir dos vetores de rótulos reais e preditos, ajustando com rigor metodológico pelo acaso marginal.

Para destravar o lab, abra [Schlögl et al. — Characterization of four-class MI EEG (JNE 2005; κ in BCI)](https://doi.org/10.1088/1741-2560/2/4/L02) e leia a definição de κ de Schlögl, (p_o − p_e)/(1 − p_e), para a métrica offline não ficar só em accuracy.
