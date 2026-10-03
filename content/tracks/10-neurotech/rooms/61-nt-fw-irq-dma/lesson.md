# Desafio — Detecção de Transições DMA Ping-Pong (HT e TC)

## 1. Objetivo do Desafio
Implementar a lógica de detecção de eventos de interrupção de Direct Memory Access (DMA) para um buffer circular de aquisição, identificando as transições de Meia Transferência (*Half Transfer* - HT) e Transferência Completa (*Transfer Complete* - TC) com base no avanço do ponteiro de escrita.

## 2. Especificação Técnica
Implemente a função `check_dma_irq(write_ptr, prev_ptr, half_size=512, full_size=1024)`:
- Determine se ocorreu uma transição de **Meia Transferência (HT)**:
  - Ocorre quando o ponteiro anterior estava estritamente abaixo da metade ($prev\_ptr < half\_size$) e o ponteiro atual atingiu ou ultrapassou a metade sem dar a volta completa ($write\_ptr \ge half\_size$ e $prev\_ptr < write\_ptr$).
- Determine se ocorreu uma transição de **Transferência Completa (TC)**:
  - Ocorre quando o ponteiro anterior estava na segunda metade ($prev\_ptr \ge half\_size$) e o ponteiro atual deu a volta modular retornando ao início do buffer ($write\_ptr < prev\_ptr$).
- Retorne a tupla booleana `(ht_irq, tc_irq)`.

## 3. Casos de Teste Canônicos
```python
# Cruzamento da primeira metade:
ht, tc = check_dma_irq(520, 500, 512, 1024)
assert ht is True and tc is False

# Wrap-around modular no fim do buffer:
ht2, tc2 = check_dma_irq(10, 1020, 512, 1024)
assert ht2 is False and tc2 is True
```

## 4. Critérios de Validação e Armadilhas
- Certifique-se de retornar uma tupla contendo exatamente dois booleanos `(ht, tc)`.
