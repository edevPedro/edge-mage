# Desafio — Forward de um MLP one-hidden-layer

## 1. Objetivo do Desafio
Implementar, sem biblioteca, o forward completo de um MLP com uma camada
escondida ReLU e saída linear (logits), e validar com pesos de brinquedo.

## 2. Especificação Técnica e Formulação
Dado `x` (lista), `W1`, `b1` (camada escondida) e `W2`, `b2` (saída):
```
h = relu(W1 @ x + b1)      # ativação
out = W2 @ h + b2          # logits (sem softmax ainda)
```
Implemente:
- `relu(z)` → `max(0, z)`;
- `matvec(M, v)` → produto matriz×vetor (lista de listas × lista);
- `mlp_forward(x, W1, b1, W2, b2)` → lista de saídas.

## 3. Critérios de Validação e Armadilhas
- Aplique ReLU *elemento a elemento* apenas na camada escondida (saída final é
  linear — logits crus).
- Dimensões: `W1` é `[d_hidden × d_in]`; `W2` é `[d_out × d_hidden]`.
- Use ponto flutuante — sem arredondamentos no caminho do forward.