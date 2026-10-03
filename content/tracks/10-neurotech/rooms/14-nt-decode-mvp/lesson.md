# Desafio — Predição e Ajuste com Discriminante Linear Regularizado

## 1. Objetivo do Desafio
Implementar a função de predição linear do modelo LDA e aplicar a regularização de encolhimento de covariância para garantir determinismo e robustez numérica em conjuntos de calibração reduzidos.

## 2. Especificação Técnica e Formulação
1. **Predição Linear:** Desenvolva `predict_lda(x, w, b)` que calcula o produto interno e soma o bias:
   $$s = \sum_{i=0}^{D-1} x_i w_i + b$$
   Retornando `1` se $s \ge 0$, e `0` caso contrário.
2. **Regularização:** Na função de ajuste regularizado, calcule a covariância encolhida $\Sigma_{\text{reg}} = (1 - \gamma)\Sigma + \gamma (\text{tr}(\Sigma)/D)\mathbf{I}$ antes de inverter a matriz via `numpy.linalg.solve` ou `pinv`.
3. **Métrica:** Avalie o classificador calculando o coeficiente Kappa de Cohen:
   $$\kappa = \frac{\text{acurácia} - 0.5}{1 - 0.5} = 2 \cdot \text{acurácia} - 1$$

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que a dimensão do vetor de pesos $w$ seja rigorosamente compatível com a dimensão do vetor de entrada $x$.
- Em matrizes de covariância com canais correlacionados, nunca tente inverter a matriz empírica sem regularização prévia.
