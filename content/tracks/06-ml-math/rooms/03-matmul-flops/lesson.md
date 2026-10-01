# Matmul = camada + FLOPs

Uma densa é GEMM: `Y = XW` (mais bias).

## Dimensões

Se `X` é `B×M` e `W` é `M×N`, então `Y` é `B×N`.
O eixo interno `M` precisa coincidir.

## FLOPs (ordem de grandeza)

≈ `2 · B · M · N` operações de ponto flutuante (mul+add) para a densa.

Exemplo: B=1, M=128, N=64 → `2·128·64 = 16384` FLOPs.

No edge, some camadas (conv, depthwise) mudam a fórmula, mas a disciplina é a mesma: estime antes de prometer latência.

## Custo dominante

Em redes densas/grandes, o matmul/GEMM costuma dominar o tempo — não o softmax.
