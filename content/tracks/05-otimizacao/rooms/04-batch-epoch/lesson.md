# Batch, epoch e o pipeline

## Epoch

Uma **epoch** = uma passagem completa pelo dataset de treino.

## Mini-batch

Em vez de um exemplo (SGD puro) ou o dataset inteiro (batch), usamos B exemplos:

`θ ← θ − η · média_B(∇L)`

Maior B → gradiente mais estável, mais RAM/ativação. No edge, B costuma ser 1 na inferência.

## Forward / backward

- Forward: ativações até a loss
- Backward: gradientes via regra da cadeia
- Update: aplicar ∇ nos pesos

## Edge

Dispositivos embutidos priorizam **inferência eficiente**; treino full fica na nuvem/workstation. Exceções: fine-tune leve, on-device learning restrito.
