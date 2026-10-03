# Desafio — Tensão Induzida por Loop Magnético de PCB

## 1. Objetivo do Desafio
Implementar a rotina analítica da Lei de Faraday para calcular a amplitude de tensão de ruído induzida em um laço de corrente condutor em função de sua área geométrica, campo magnético e frequência.

## 2. Especificação Técnica e Formulação
Dados a área do loop `area_m2` em metros quadrados, a densidade de fluxo magnético `b_field_tesla` em Tesla, e a frequência do campo `frequency_hz` em Hertz:
- Implemente a função `induced_voltage_loop(area_m2, b_field_tesla, frequency_hz)`:
  $$V_{\text{ind}} = 2\pi \times \text{frequency\_hz} \times \text{b\_field\_tesla} \times \text{area\_m2}$$
- Retorne o valor flutuante da amplitude de pico da tensão induzida em Volts.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de converter a área de centímetros quadrados para metros quadrados quando necessário ($1\text{ cm}^2 = 10^{-4}\text{ m}^2$).
- Todos os parâmetros devem ser estritamente não-negativos.
