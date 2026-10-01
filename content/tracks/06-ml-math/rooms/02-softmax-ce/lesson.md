# Softmax & Cross-Entropy

## Softmax

`p_i = e^{z_i} / Σ_j e^{z_j}` transforma logits z em distribuição (`p_i > 0`, `Σ p = 1`).

## Estabilidade numérica

`e^{z}` explode se z for grande. Truque:

`softmax(z) = softmax(z − max(z))`

O max cancela na razão e evita overflow.

## Cross-entropy

Com label one-hot na classe k: `CE = −log p_k`.

Minimizar CE = maximizar a probabilidade da classe correta.

## Craft PyTorch

Em produção de treino, use `nn.CrossEntropyLoss` com **logits** (não softmax prévio): a loss aplica log-softmax fused — mais estável e o padrão da API oficial.

## Por que importa no edge

Classificadores on-device (wake-word, gestos, anomalia) terminam em softmax + argmax.
Quantização pode afetar logits — valide a calibração (golden float vs int8).
