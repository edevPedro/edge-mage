# Desafio — Embeddings e vizinhos mais próximos

## 1. Objetivo do Desafio
Implementar o núcleo de modelos multimodais embutidos: normalização L2,
similaridade de cosseno e a busca do rótulo mais próximo (retrieval).

## 2. Especificação Técnica e Formulação
- `normalize(v)` → `v / ||v||₂`; se `||v||₂ == 0`, devolve `v` como está.
- `cosine_sim(a, b)` → produto interno dos vetores L2-normalizados; `0.0` se
  qualquer um for zero.
- `top1_label(emb, centroids, labels)` → `labels[i]` do centroide com maior
  `cosine_sim(emb, centroids[i])`.

## 3. Critérios de Validação e Armadilhas
- Vetor zero não pode dar divisão por zero (`normalize` devolve igual;
  `cosine_sim` devolve 0).
- Vetores paralelos → cosseno ≈ 1; ortogonais → ≈ 0.
- A ordem de `labels` casa com a de `centroids` (índice de mesmo lugar).