# Conceito — Multimodal lite

## Espaço compartilhado
Embeddings contrastivos: texto/imagem/áudio no mesmo espaço.

## Similaridade
`cos(θ) = a·b / (|a||b|)` — retrieval por cosseno.

## Orçamento
`bytes = dim · count · dtype_bytes`; top-k por cosseno.