# FLOPs, banda e o gargalo real

No edge, “modelo leve” não basta: você precisa saber **onde o tempo e a energia vão**.

## FLOPs (ordem de grandeza)

Para uma densa `Y = XW` com X ∈ R^{B×M}, W ∈ R^{M×N}:

- Multiplicações ≈ `B · M · N`
- Somas ≈ `B · M · N` (mesma ordem)
- Costuma-se contar ~`2 · B · M · N` FLOPs (mul+add)

Batch `B` multiplica o custo de compute — e também a pressão de ativação na RAM.

## Memória vs compute

Bytes movidos muitas vezes dominam a latência (memory-bound):

- Pesos int8: `M·N` bytes
- Ativações: dependem de layout e lifetime na arena

Largura de banda (GB/s) × tempo ≈ bytes transferíveis. Se o kernel precisa de mais bytes do que a banda entrega no budget de latência, SIMD sozinho não salva.

## Roofline (intuição)

- **Compute-bound**: aumenta FLOPs/s (melhor kernel, maior clock útil)
- **Memory-bound**: reduz bytes (quantização, fusão de ops, melhor locality)

## Batching no edge

Batch > 1 melhora throughput em servidores; em MCU/NPU on-device costuma-se **B=1** por latência e RAM. Meça os dois eixos: latência de uma amostra e energia por inferência.
