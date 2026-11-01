# Desafio — Convolução 1D e a anatomia temporal do EEG

## 1. Objetivo do Desafio
Implementar a fórmula de comprimento de saída de uma conv 1D e uma convolução
*valid* na mão, para interiorizar por que convolução compartilha parâmetros e
não cresce com `n_samples`.

## 2. Especificação Técnica e Formulação
- `conv1d_out_len(n_samples, kernel_len, stride=1, pad=0)` retorna
  `floor((n_samples + 2*pad − kernel_len)/stride) + 1` (mínimo 0).
- `conv1d_valid(x, kernel)` aplica conv 1D sem padding, stride 1:
  `y[n] = Σ_k kernel[k] * x[n+k]`, para `n` de `0` a `len(x)-len(kernel)`.

## 3. Critérios de Validação e Armadilhas
- Se o kernel for maior que o sinal, `conv1d_valid` retorna lista vazia.
- Compare com o MLP: mesmo número de features de entrada, a conv usa `k`
  pesos por canal em vez de `n_samples` — é isso que segura o overfit.
- Resultado com `n == k` tem exatamente 1 saída (janela cobre o sinal inteiro).