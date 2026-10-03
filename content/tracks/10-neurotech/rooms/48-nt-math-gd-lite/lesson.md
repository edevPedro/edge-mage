# Lição — Otimização por Gradiente Descendente

## 1. Contexto Operacional
O gradiente descendente é o motor algorítmico do aprendizado de máquina moderno. Em neurotecnologia, ele é empregado tanto em pequenos filtros adaptativos em microcontroladores quanto no treinamento de redes convolucionais profundas (EEGNet) para decodificação de intenção motora.

## 2. Passo a Passo Matemático

### O Passo de Atualização
Dada a lista de pesos $w$ e a lista de gradientes $g$, com taxa de aprendizado `lr`:
$$w_j \leftarrow w_j - \text{lr} \times g_j$$

### Treinamento Iterativo de Filtro Linear
Dadas $N$ amostras $X$ com alvos $y$ e pesos iniciais $w$:
1. A cada época:
   - Para cada amostra $i \in [0, N-1]$, calcule a predição linear $\hat{y}_i = \sum_j w_j X_{i, j}$.
   - O resíduo é $e_i = \hat{y}_i - y_i$.
   - O vetor gradiente tem componentes $g_j = \frac{1}{N} \sum_{i=0}^{N-1} e_i X_{i, j}$.
   - Atualize $w = \text{gd\_step}(w, g, \text{lr})$.
2. Ao final de todas as épocas, calcule a perda quadrática média final:
   $$\text{loss} = \frac{1}{2N} \sum_{i=0}^{N-1} (\hat{y}_i - y_i)^2$$
3. Retorne `(w, loss)`.

Consulte [scikit-learn SGDClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html) para entender variações de otimização em dados bioelétricos.
