# Desafio — Atenção com Q/K/V (scaled dot-product)

## 1. Objetivo do Desafio
Implementar o núcleo da atenção escalada (scaled dot-product attention) com
listas de listas (sem NumPy), para enxergar as três operações: scores, softmax
por linha e combinação com V.

## 2. Especificação Técnica e Formulação
- `attention_scores(Q, K, scale)` → `M[i][j] = scale · Σ_d Q[i][d]·K[j][d]`
  (a linha `i` vs a coluna `j` de K).
- `softmax_rows(M)` → softmax aplicado a cada linha independentemente.
- `attention_out(Q, K, V, scale)` → `softmax_rows(attention_scores(Q,K,scale)) @ V`,
  onde `(P@V)[i][j] = Σ_m P[i][m]·V[m][j]`.

## 3. Critérios de Validação e Armadilhas
- A linha de `P` soma 1 (teste cobre `sum(P[0])==1`).
- Ordem correta dos índices em `Q@Kᵀ`: linha = query, coluna = chave.
- Com Q=K=I (identidade), o par `(i,i)` pontua mais — o teste usa isso para
  conferir a mistura final de valores.