# Gradiente

Para `f(x)`, o gradiente `∇f` aponta para o **maior aumento** de f.
Descida do gradiente: `x ← x − η ∇f(x)`.

## Em 1D

Se `f'(x) > 0`, andamos para a **esquerda** (diminuir x) para reduzir f — o sinal de menos na fórmula.

## Em várias dimensões

∇f é o vetor das derivadas parciais. Cada parâmetro (peso) recebe sua própria componente.

## Learning rate η

- η pequeno → passos lentos, estável
- η grande → oscilação / divergência

No edge, o **treino** costuma ser off-device; on-device você mais vê **inferência**. Ainda assim, fine-tune leve e QAT (quantization-aware training) usam a mesma intuição de update.
