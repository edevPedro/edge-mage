# ADC e bits

ADC de **n bits** com referência Vref divide a faixa em `2^n` níveis.
Resolução ≈ `Vref / 2^n`.

Ex.: 12-bit, Vref=3.3 V → LSB ≈ 3.3/4096 ≈ 0.805 mV.

Potência do MCU sobe com clock e com rádio — Edge AI precisa orçar mW, não só FLOPs.
