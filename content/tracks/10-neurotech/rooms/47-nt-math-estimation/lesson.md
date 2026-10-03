# Desafio — Estimação Não-Viesada de Matriz de Covariância Amostral

## 1. Objetivo do Desafio
Implementar a rotina de cálculo da matriz de covariância amostral não-viesada para séries temporais multicanal com subtração explícita de média e correção de Bessel ($T - 1$).

## 2. Especificação Técnica e Formulação
Dada uma matriz bidimensional $X$ com $C$ linhas (canais) e $T$ colunas (amostras temporais):
- Implemente `sample_covariance_matrix(X)`:
  1. Subtraia a média temporal de cada canal: $\tilde{X}_{c, t} = X_{c, t} - \bar{X}_c$.
  2. Calcule a matriz de produto externo e divida por $T - 1$:
     $$\Sigma_{i, j} = \frac{1}{T - 1} \sum_{t=0}^{T-1} \tilde{X}_{i, t} \tilde{X}_{j, t}$$
  3. Retorne a matriz resultante $C \times C$.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que a diagonal contenha as variâncias amostrais não-viesadas de cada canal.
- Exija $T > 1$ para prevenir divisão por zero na correção de Bessel.
