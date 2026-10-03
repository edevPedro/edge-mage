# Lição — Vetores, Projeção Linear e Normalização Espacial

## 1. Contexto Operacional
Em sistemas de BCI não invasivos, sinais cerebrais adquiridos por eletrodos no escalpo são inerentemente misturas lineares de potenciais sinápticos corticais dispersos pelo crânio. A primeira linha de defesa matemática contra a baixa resolução espacial do EEG é a projeção vetorial.

Nesta sala, você aprenderá a manipular vetores de sinais multicanais e projetores espaciais, garantindo a preservação da escala de energia através da normalização $L_2$.

## 2. Passo a Passo Matemático

### Produto Interno (Projeção)
Dados dois vetores $a, b \in \mathbb{R}^n$:
$$\text{dot}(a, b) = \sum_{i=1}^n a_i b_i$$

### Norma Euclidiana $L_2$
$$\text{l2}(a) = \sqrt{\sum_{i=1}^n a_i^2}$$

### Normalização de Filtro Espacial
Dado um vetor de pesos espaciais $w \in \mathbb{R}^n$:
1. Calcule a norma $\text{norm} = \text{l2}(w)$.
2. Se $\text{norm} == 0$, levante `ValueError("Vetor nulo não possui direção espacial definida")`.
3. Retorne o vetor normalizado $\hat{w} = [w_1/\text{norm}, w_2/\text{norm}, \dots, w_n/\text{norm}]$.

## 3. O Desafio de Código
Implemente no laboratório:
- `dot(a, b)`: produto escalar elemento a elemento.
- `l2(a)`: raiz quadrada da soma dos quadrados.
- `normalize_spatial_filter(w)`: retorna $\hat{w}$ normalizado com norma unitária exata ($1.0$).

Consulte a documentação em [NumPy linalg norm](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html) se tiver dúvidas sobre álgebra linear vetorial em Python.
