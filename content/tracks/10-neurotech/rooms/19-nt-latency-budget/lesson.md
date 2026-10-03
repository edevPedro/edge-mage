# Desafio — Verificação de Orçamento de Latência (Latency Budget)

## 1. Objetivo do Desafio
Implementar rotinas para auditar os estágios temporais de um pipeline de BCI e simular o impacto de parâmetros de amostragem, ordem de filtros e clock de hardware contra deadlines de tempo real.

## 2. Especificação Técnica e Formulação
1. **Checagem Direta de Latência:** Implemente `total_latency_check(stages, deadline)` que recebe uma lista de latências em milissegundos `[t_sense, t_decide, t_act]` e um `deadline`:
   $$t_{\text{total}} = \sum t_i$$
   Retorna um dicionário `{"total_ms": t_total, "miss": t_total > deadline}`.
2. **Simulação Completa de Pipeline:** Implemente `simulate_bci_pipeline_latency(window_len_ms, filter_taps, sampling_rate_hz, compute_cycles, mcu_clock_mhz, actuator_delay_ms, deadline_ms)`:
   - $t_{\text{filter}} = ((\text{filter\_taps} - 1) / 2) \times (1000 / \text{sampling\_rate\_hz})$ (atraso de grupo linear em ms).
   - $t_{\text{compute}} = (\text{compute\_cycles} / (\text{mcu\_clock\_mhz} \times 10^6)) \times 1000$ (em ms).
   - $t_{\text{sense}} = \text{window\_len\_ms} + t_{\text{filter}}$.
   - $t_{\text{decide}} = t_{\text{compute}}$.
   - $t_{\text{act}} = \text{actuator\_delay\_ms}$.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que todas as unidades intermediárias sejam rigorosamente convertidas para milissegundos antes da soma.
- Lembre-se: em filtros FIR simétricos causais, o atraso de grupo é exatamente metade da ordem do filtro: $(N - 1) / (2 f_s)$.
