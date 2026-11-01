# Conceito — CNN para EEG: compartilhar é o jogo

A **convolução 1D** resolve o problema do MLP em séries temporais: em vez de uma
matriz densa que ignora a estrutura do tempo, um filtro curto `k` desliza pelo
sinal compartilhando os *mesmos* pesos em cada deslocamento. Isso injeta o
*inductive bias* de que "padrão local aparece em qualquer instante".

## 1. Por que convolução encaixa com EEG
- **Filtros temporais aprendidos**: convoluções de `k≈32` amostras equivalem a
  filtros passa-faixa aprendidos — a evolução do filter-bank fixo.
- **Custo sub-linear no tempo**: os parâmetros não crescem com `n_samples`;
  largura do kernel decide o custo.
- Fórmula de saída (valid): `n_out = floor((n − k)/stride) + 1`.

## 2. Decomposição temporal × espacial (depthwise)
- Uma conv *regular* mistura canais e tempo ao mesmo tempo → muitos parâmetros.
- **Depthwise** aplica 1 filtro por canal (combinação espacial por banda) —
  o análogo do filtro espacial do CSP.
- Juntas (EEGNet): conv 1D (bandas/filtro) → conv espacial depthwise
  (topografia/combinação de canais) → conv separável 1×1 (mix de features).

## 3. Receptive field
- `k` amostras por estágio; com L estágios, cada saída "enxerga" uma janela
  maior no tempo (`≈ L×(k−1)+1`) — atenção ao tamanho frente à latência do app
  online.

## O que a próxima sala assume
`nt-dl-training` fecha o loop que falta: função de perda (cross-entropy),
gradiente e o porquê de overfit com N pequeno.

## Leituras recomendadas
- [EEGNet (Lawhern et al., 2018)](https://iopscience.iop.org/article/10.1088/1741-2560/aace8c) — o inductive bias aplicado a biopotenciais.
- [CS231n — CNNs](https://cs231n.github.io/convolutional-networks/)
- [MobileNets — depthwise separable convs](https://arxiv.org/abs/1704.04861)