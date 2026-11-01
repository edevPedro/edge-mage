# Requantização & per-channel

Depois do matmul, `acc` é int32. Para o próximo layer consumir int8, o kernel faz:

```
q_out = clamp( round( acc · s_out ), −128, 127 )
```

## Requantizar ≠ truncar

Truncar ignora a escala e vaza precisão. A spec [LiteRT 8-bit](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec) define o multiplicador fixo (scale recebida como fixed-point) justamente para o caminho ser reprodutível em silício.

## Per-channel

Com per-tensor, um único scale cobre todos os canais — canais quietos desperdiçam resolução. **Per-channel** dá uma escala por canal de saída: melhor precisão a custo de mais metadados. No papel de SmoothQuant, essa escolha reduz outliers dos ativadores.

## Clamp

Após round, saturar em [−128, 127]. Sem clamp, um valor 200 "vira" um int8 corrompido (wrap-around), e o modelo diverge silenciosamente.

O código da sala, `per_channel_scale(q, scales, ch)`, usa a escala do canal `ch`.

## Viés int32

Bias não é quantizado em float: ele entra como int32 com escala composta `s_in·s_w`, somado antes do requant final.