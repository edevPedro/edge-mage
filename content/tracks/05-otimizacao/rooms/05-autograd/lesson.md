# Autograd & grafo de computação

## O que o framework faz

1. Forward: cada op registra como desfazer a derivada (nó no grafo).
2. `backward()` a partir de um escalar (a loss): propaga ∂L para folhas (`requires_grad`).
3. Optimizer lê `.grad` e atualiza pesos; depois `zero_grad()`.

Leia o tutorial oficial: [A Gentle Introduction to torch.autograd](https://pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html).

## Edge / deploy

No device você **não** quer o tape. Inferência = forward só. Treino/QAT ficam off-device (ou em fine-tune controlado).

## Craft mínimo

Entender `requires_grad`, `backward`, e por que `no_grad` é obrigatório em benchmark de latência.
