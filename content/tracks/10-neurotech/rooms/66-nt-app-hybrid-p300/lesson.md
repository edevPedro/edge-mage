# Desafio — Detecção do Pico P300 em Épocas de ERP

## 1. Objetivo do Desafio
Implementar a rotina de detecção de pico de amplitude positiva para o potencial evocado P300, localizando o valor máximo do sinal de EEG dentro da janela temporal canônica de 250 a 450 milissegundos pós-estímulo.

## 2. Especificação Técnica
Implemente a função `p300_peak(erp_signal, fs=250, start_ms=250, end_ms=450)`:
- Converta os tempos de início e fim da janela de interesse para índices da lista utilizando a frequência de amostragem `fs`:
  $$i_{start} = \text{int}\left(\frac{start\_ms}{1000} \times fs\right)$$
  $$i_{end} = \text{int}\left(\frac{end\_ms}{1000} \times fs\right)$$
- Extraia a fatia do sinal correspondente ao intervalo $[i_{start}, i_{end}]$ (inclusive ou conforme indexação padrão de fatiamento).
- Retorne o valor máximo escalar (float) encontrado nessa fatia temporal.

## 3. Exemplo de Referência
```python
# Sinal de 200 amostras a fs=250 Hz (1 amostra a cada 4 ms)
# 250 ms -> índice 62; 450 ms -> índice 112
sig = [0.0] * 200
sig[75] = 12.5  # Pico em 300 ms (75 * 4 ms = 300 ms)
assert abs(p300_peak(sig, fs=250, start_ms=250, end_ms=450) - 12.5) < 1e-5
```

## 4. Critérios de Validação e Armadilhas
- Certifique-se de que a busca ocorra estritamente dentro da janela solicitada.
- Retorne o valor numérico da voltagem de pico (float).
