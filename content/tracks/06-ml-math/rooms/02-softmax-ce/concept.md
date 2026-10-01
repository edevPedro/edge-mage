# Conceito — Softmax e CE

## Softmax estável
`softmax(z)_i = exp(z_i − max z) / Σ exp(z_j − max z)`

## Cross-entropy
`CE = −Σ y_i log p_i` (one-hot → `−log p_{classe}`)
