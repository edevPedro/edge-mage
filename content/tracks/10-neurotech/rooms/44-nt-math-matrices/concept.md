# Conceito — Matrizes em Neuroengenharia, Transformações Lineares e Covariância Amostral

A representação matricial é a linguagem canônica para descrever séries temporais multicanal e conectividade espacial em BCI.

## 1. A Matriz de Dados Multicanal
Um ensaio (epoch) de EEG com $C$ canais e $T$ amostras temporais é estruturado na matriz $X \in \mathbb{R}^{C \times T}$:
$$X = \begin{bmatrix} x_{1,1} & x_{1,2} & \dots & x_{1,T} \\ x_{2,1} & x_{2,2} & \dots & x_{2,T} \\ \vdots & \vdots & \ddots & \vdots \\ x_{C,1} & x_{C,2} & \dots & x_{C,T} \end{bmatrix}$$
Cada linha representa a série temporal de um eletrodo; cada coluna representa a captura espacial instantânea do escalpo.

## 2. A Matriz de Covariância Espacial Amostral
Assumindo que os sinais tenham média temporal zero (sinal centralizado após filtragem passa-faixa), a matriz de covariância espacial $\Sigma \in \mathbb{R}^{C \times C}$ é dada por:
$$\Sigma = \frac{1}{T - 1} X X^T$$
Propriedades fundamentais da covariância:
- **Simetria:** $\Sigma_{i, j} = \Sigma_{j, i}$.
- **Elementos da Diagonal ($\Sigma_{i, i}$):** Representam a variância (potência total) do canal $i$.
- **Elementos Fora da Diagonal ($\Sigma_{i, j}$):** Representam a covariância mútua entre os canais $i$ e $j$.
- **Traço ($\text{tr}(\Sigma)$):** Soma das variâncias de todos os eletrodos, quantificando a energia total do campo elétrico capturado.

## 3. Modos de Falha na Prática de Engenharia
1. **Divisão por $T$ em vez de $T - 1$:** Introduzir um viés sistemático na estimativa de covariância amostral em janelas curtas.
2. **Incompatibilidade de Dimensões:** Multiplicar $X^T X$ (que gera uma matriz $T \times T$ de correlação temporal massiva) em vez de $X X^T$ (que gera a matriz $C \times C$ de covariância espacial desejada).

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-math-eigen`) decompõe essas matrizes de covariância em autovalores e autovetores através do método da iteração de potência (Power Iteration).

## 5. Ponto de Destrave do Lab
Consulte o guia de álgebra linear matricial de [Strang (Linear Algebra and Its Applications, Cengage Learning)](https://math.mit.edu/~gs/).
