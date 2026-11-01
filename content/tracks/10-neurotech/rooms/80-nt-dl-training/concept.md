# Conceito — Treino: a função de custo manda

Aprender é minimizar uma função de custo sobre os pesos. Sem custo correto,
nenhuma arquitetura salva o modelo.

## 1. Classificação: softmax + cross-entropy
- **Logits** (`z`) → **softmax** `p_i = exp(z_i)/Σ exp(z_j)` vira probabilidade.
- **Cross-entropy** `−Σ y·log(p)` penaliza *confiança errada*: tanto errar a
  classe quanto errar com alta confiança.
- A combinação softmax + CE é numericamente estável e é a loss padrão para
  classes (2..N, inclusive MI-BCI).

## 2. Gradiente descendente
- Atualizar `θ ← θ − η·∇_θ L`. O gradiente diz "para onde a perda cresce";
  você anda no oposto.
- Em N pequeno: batch único oscila; use batches/lotes com shuffle e
  *validation* fixa para observar generalização.

## 3. Anti-overfit em N≪D (o trio)
1. **Regularização**: L2/weight decay, dropout, early stopping.
2. **Validação honesta**: nunca tune hiperparâmetro em teste; inter-session/
   cross-subject é mais difícil que random split.
3. **Mais dados / aumentação**: janelas múltiplas por trial, trials de treino
   por sujeito bem separadas.
- Verifique sempre contra o *chance level* (κ≈0 para 2 classes equilibradas).

## O que a próxima sala assume
`nt-tokens-seq` muda o domínio: de janelas contínuas para *tokens* discretos —
o pré-requisito dos transformers e da geração LLM.

## Leituras recomendadas
- [Deep Learning book — optimization & regularization](https://www.deeplearningbook.org/contents/optimization.html)
- [CS231n — loss functions](https://cs231n.github.io/linear-classify/)
- [Combrisson & Jerbi — chance level](https://doi.org/10.1016/j.jneumeth.2015.03.034)
- [Varoquaux — CV pitfalls](https://doi.org/10.1016/j.neuroimage.2016.10.038)