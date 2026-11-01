# Conceito — MLP: a célula fundadora do deep learning

Um **MLP (multilayer perceptron)** empilha camadas afins intercaladas por
não-linearidades. É a menor rede capaz de representar a mesma família de
funções que os modelos de sequência maiores usam — sem ainda a complexidade de
convoluções ou atenção.

## 1. Camada linear
- Uma camada computa `h = W·x + b`, com `W` de `[d_out × d_in]` e `b` de `d_out`.
- Parâmetros por camada: `d_in × d_out` pesos + `d_out` biases.

## 2. Não-linearidade (ReLU)
- Sem ReLU, empilhar camadas afins é uma única afim — a profundidade colapsa.
- `relu(z) = max(0, z)` introduz a composição de features em estágios
  (ex.: bandas → padrões espaciais → decisão).

## 3. Profundidade ≠ largura
- Uma camada escondida já é um aproximador universal *em teoria*;
- Na prática, **profundidade** (várias camadas) aprende representações mais
  compostas, mas paga com mais parâmetros — o que dói em N≪D.
- Em dados neurais: comece 1–2 camadas escondidas com regularização L2/dropout;
  suba a profundidade só com validação rigorosa.

## 4. Contexto dos laboratórios
- `nt-cnn-eeg` substitui a matriz densa por convoluções (inductive bias do
  sinal); `nt-dl-training` fecha o loop de aprendizado (loss + gradiente).

## O que a próxima sala assume
`nt-cnn-eeg` assume o forward do MLP para estender à convolução 1D
compartilhada por tempo — o mesmo custo de parâmetros compartilhados no tempo
que o EEGNet usa.

## Leituras recomendadas
- [MLP & backprop — Deep Learning book, cap. 6](https://www.deeplearningbook.org/contents/mlp.html)
- [CS231n — Neural Networks](https://cs231n.github.io/neural-networks-1/)
- [PyTorch — nn.Linear](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html)