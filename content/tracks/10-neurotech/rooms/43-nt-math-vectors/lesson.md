# Desafio — Álgebra Vetorial, Produto Interno e Normalização de Filtros

## 1. Objetivo do Desafio
Implementar as operações fundamentais de álgebra linear vetorial que sustentam a filtragem espacial em BCI: produto interno, norma euclidiana e normalização para vetor unitário.

## 2. Especificação Técnica e Formulação
Implemente as três funções canônicas em Python sem bibliotecas externas:
1. `dot(a, b)`: Calcula o produto interno euclidiano $\sum_{i=0}^{N-1} a_i b_i$. Exige vetores de mesmo comprimento.
2. `l2_norm(v)`: Calcula a norma euclidiana $\|v\|_2 = \sqrt{\sum_{i=0}^{N-1} v_i^2}$.
3. `normalize_vector(v)`: Retorna o vetor unitário $\hat{v} = v / \|v\|_2$. Se $\|v\|_2 = 0$, levanta `ValueError("vetor de norma zero")`.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que vetores de dimensões incompatíveis em `dot(a, b)` levantem `ValueError`.
- A norma do vetor normalizado $\|\hat{v}\|_2$ deve ser estritamente igual a $1.0$ dentro da precisão de float.
