# Desafio — Análise de Jitter Temporal e Violação de Prazos

## 1. Objetivo do Desafio
Implementar a rotina analítica de diagnóstico temporal para processar um vetor de marcas de tempo (*timestamps*), computando o jitter absoluto médio e o número de violações que ultrapassaram a tolerância estipulada.

## 2. Especificação Técnica
Implemente a função `timing_analysis(timestamps_s, target_interval_s=0.004, max_jitter_s=0.001)`:
- Receba uma lista de marcas temporais contínuas em segundos `timestamps_s`.
- Se a lista tiver menos de 2 elementos, retorne `(0.0, 0)`.
- Para cada par consecutivo de timestamps $(t_i, t_{i+1})$:
  - Calcule o intervalo decorrido: $\Delta t = t_{i+1} - t_i$.
  - Calcule o erro absoluto em relação ao intervalo nominal:
    $$e_i = |\Delta t - target\_interval\_s|$$
  - Acumule o erro total para a média.
  - Se $e_i > max\_jitter\_s$, incremente o contador de violações (`misses_count`).
- Retorne a tupla `(mean_jitter, misses_count)` onde `mean_jitter` é a média aritmética dos erros absolutos sobre todos os intervalos válidos.

## 3. Exemplo de Referência
```python
ts = [0.0, 0.004, 0.008, 0.014]
# Intervalos: 0.004 (erro 0.0), 0.004 (erro 0.0), 0.006 (erro 0.002)
# Erro médio: (0.0 + 0.0 + 0.002) / 3 = 0.0006666...
# Misses (> 0.001): 1 (o terceiro intervalo)
j, m = timing_analysis(ts, 0.004, 0.001)
assert m == 1
assert abs(j - 0.002 / 3.0) < 1e-5
```

## 4. Critérios de Validação e Armadilhas
- Certifique-se de dividir pelo número de intervalos ($N - 1$), e não pelo número de timestamps ($N$).
