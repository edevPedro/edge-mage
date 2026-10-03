# Lição — Decode MVP: Labels → LDA → Decodificação em Tempo Real

## 1. O Discriminante Linear Regularizado de Fisher
1. **O Vetor de Projeção Ótimo**:
   $$\mathbf{w} = \boldsymbol{\Sigma}_{\text{reg}}^{-1} (\boldsymbol{\mu}_1 - \boldsymbol{\mu}_0)$$
   Projeta o espaço de características multicanal em um escalar 1D ótimo para separação entre as duas intenções motoras.

2. **Regularização de Shrinkage**:
   $$\boldsymbol{\Sigma}_{\text{reg}} = (1 - \gamma) \boldsymbol{\Sigma} + \gamma \left(\frac{\text{tr}(\boldsymbol{\Sigma})}{D}\right) \mathbf{I}$$
   Previne matrizes singulares em regimes de amostras pequenas ($N \approx D$), comum em calibrações rápidas de BCI.

3. **O Limiar Bayesiano de Decisão**:
   $$b = -\frac{1}{2} \mathbf{w}^T (\boldsymbol{\mu}_1 + \boldsymbol{\mu}_0)$$
   A predição é puramente $\mathbf{w}^T \mathbf{x} + b \ge 0$, executável em menos de um microssegundo em microcontroladores Cortex-M.

## 2. As Funções de Laboratório Desta Sala
- `predict_lda(x, w, b)`: Avalia o hiperplano linear para um vetor de entrada.
- `fit_threshold_lda(class0, class1)`: Ajusta o limiar unidimensional ótimo equidistante entre as médias.
- `cohen_kappa(y_true, y_pred)`: Avalia o coeficiente Kappa de Cohen corrigido pela taxa esperada ao acaso.
- `fit_regularized_lda_2d(X_train, y_train, shrinkage)`: Calcula médias de classe, dispersão intra-classes, aplica regularização de encolhimento, inverte a matriz e extrai $(\mathbf{w}, b)$ para dados de C3 e C4.

Para destravar o lab, abra [sklearn — LinearDiscriminantAnalysis](https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.LinearDiscriminantAnalysis.html) e leia o parâmetro de shrinkage do LDA no scikit-learn, para o predict_lda do MVP não virar acurácia sem regularização.
