# Conceito — Autovalores, Autovetores e o Método da Iteração de Potência

A decomposição espectral de matrizes de covariância é a base matemática de PCA, CSP e classificadores Riemannianos em BCI.

## 1. Definição Algébrica de Autovetores e Autovalores
Para uma matriz quadrada $A \in \mathbb{R}^{C \times C}$, um vetor não-nulo $v \ne 0$ é um autovetor associado ao autovalor $\lambda \in \mathbb{R}$ se satisfaz:
$$A v = \lambda v$$
Geometricamente:
- A transformação linear induzida por $A$ apenas estica ou contrai o vetor $v$ pelo fator $\lambda$, sem rotacioná-lo no espaço.
- Em matrizes de covariância simétricas e positivas definidas (SPD), todos os autovalores são reais e estritamente positivos ($\lambda_i > 0$), e os autovetores associados a autovalores distintos são mutuamente ortogonais ($v_i^T v_j = 0$).
- O autovetor principal aponta na direção de maior variância espacial dos dados; o autovalor $\lambda_1$ quantifica exatamente a magnitude dessa variância máxima.

## 2. O Algoritmo da Iteração de Potência (Power Iteration)
Para encontrar o maior autovalor $\lambda_1$ e seu autovetor unitário $v_1$ sem calcular o polinômio característico $\det(A - \lambda I) = 0$:
1. Inicializar $v^{(0)}$ como um vetor unitário arbitrário (não ortogonal a $v_1$).
2. Iterar recursivamente para $k = 1, 2, \dots$:
   $$w^{(k)} = A v^{(k-1)}$$
   $$v^{(k)} = \frac{w^{(k)}}{\|w^{(k)}\|_2}$$
3. Calcular a estimativa do autovalor pelo Quociente de Rayleigh:
   $$\lambda^{(k)} = (v^{(k)})^T A v^{(k)}$$

A taxa de convergência geométrica depende da razão de separação entre os dois maiores autovalores: $|\lambda_2 / \lambda_1| < 1$.

## 3. Modos de Falha na Prática de Engenharia
1. **Autovalores Iguais ou Próximos (Espectro Degenerado):** Se $\lambda_1 \approx \lambda_2$, a convergência torna-se lenta, exigindo aceleradores de Chebyshev ou algoritmos de decomposição QR.
2. **Vetor Inicial no Núcleo:** Escolher um vetor inicial perfeitamente ortogonal ao autovetor dominante (probabilidade quase nula com inicialização estocástica).

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-math-probability`) introduz o cálculo de probabilidades, distribuições gaussianas e a probabilidade de acerto ao acaso em tarefas de decisão.

## 5. Ponto de Destrave do Lab
Consulte o tratamento formal de decomposição espectral em [Golub & Van Loan (Matrix Computations, Johns Hopkins University Press)](https://jhupbooks.press.jhu.edu/title/matrix-computations).
