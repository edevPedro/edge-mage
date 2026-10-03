# Lição — Orçamento de Latência Closed-Loop e Restrições Hard Real-Time

## 1. O Pipeline Sense → Decide → Act
Para garantir feedback em tempo real sem latência perceptível pelo córtex motor ($<50\text{--}100\text{ ms}$):
1. **Estágio Sense (Ingestão)**:
   $$T_{\text{ingest}} = \frac{N_{\text{packet}}}{f_s} \times 1000 \quad (\text{ms})$$
2. **Estágio Decide (Cálculo)**:
   $$T_{\text{compute}} = T_{\text{filtros}} + T_{\text{inferência}}$$
3. **Estágio Act (Exibição)**:
   $$T_{\text{display}} \approx \frac{1000}{\text{refresh\_hz}} \quad (\approx 16.6\text{ ms em 60 Hz})$$

## 2. Prevenção de Estouro de Buffer (Buffer Overrun)
O intervalo de avanço da janela deslizante (*hop interval*) determina o tempo disponível para cálculo:
$$T_{\text{hop}} = \frac{N_{\text{hop}}}{f_s} \times 1000 \quad (\text{ms})$$
Se $T_{\text{compute}} > T_{\text{hop}}$, a taxa de produção de dados supera a taxa de consumo, provocando perda de amostras (*buffer overrun*) e jitter severo.

## 3. As Funções de Laboratório Desta Sala
- `total_latency_check(stages_ms, max_allowed_ms)`: Soma os estágios e avalia contra o limite global.
- `simulate_bci_pipeline_latency(fs, packet_samples, hop_samples, n_channels, biquad_sections, classifier_time_ms, display_refresh_ms, deadline_ms)`: Simula todos os estágios do pipeline closed-loop, detectando estouro de buffer e quebra de prazo fatal sensorial.

Para destravar o lab, abra [Singh et al. — MI-BCI review (online challenges context, PMC8003721)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8003721/) e leia os desafios de tempo real no review de Singh (deadline de janela, não só κ offline) para somar os estágios do orçamento em ms.
