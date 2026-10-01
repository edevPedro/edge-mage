# ADC & potência

ADC de n bits: `2ⁿ` níveis. LSB ≈ `Vref / 2ⁿ`.

Mais resolução ≠ sempre melhor: ruído, tempo de conversão e corrente do clock importam.
Subir o clock do MCU aumenta desempenho e costuma aumentar potência — tradeoff clássico edge.
