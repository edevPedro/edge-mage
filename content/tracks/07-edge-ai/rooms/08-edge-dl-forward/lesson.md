# Forward Int8 no edge

Um matmul int8 só é útil se o kernel implementar o **contrato inteiro** do runtime. O protocolo básico (o mesmo do [paper de Jacob et al.](https://arxiv.org/abs/1712.05877) e da [spec LiteRT 8-bit](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec)):

1. Entrada `q_in · s_in` e peso `q_w · s_w` (pesos simétricos ⇒ zero-point 0).
2. **FMA int8→int32**: `acc += q_in[i] * q_w[i]`, acumulando em int32.
3. Saída: `y ≈ (acc − zp_out) · (s_in · s_w)` — a **escala dupla** é o produto das escalas.

## Por quê int32?

`127 · 127 = 16129`; com K=8, `acc` chega a ≈129k — estoura int8. O acumulador int32 absorve o produto sem clamp a cada passo (clamp arredonda e destrói gradiente/referência).

O CMSIS-NN usa exatamente esse caminho: `arm_nn_mat_mult_s8` acumula int32 e faz requantização na saída. Sparsidade/zero-point assimétrico à parte, o contrato de escala é inegociável para "quantizar de verdade".

## Dequantização

`dequant(q, s) = q · s` é a verificação mental de qualquer kernel: se o valor float não bate dentro da tolerância, é sinal de scale/zero-point errado.

O código da sala exercita os três passos: `q8_fma_dot` (FMA int32), `dual_scale` (escala dupla) e `dequant_scaled`.