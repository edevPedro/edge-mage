# Lição — Campo Elétrico e Distância

## 1. O Decaimento Dipolar no Meio Condutor
No estudo de potenciais bioelétricos macroscópicos, o gerador elementar é o dipolo de corrente:
1. **Decaimento com a Distância**:
   $$V(r) \propto \frac{1}{r^2}$$
   Diferente de uma carga pontual estática no vácuo ($1/r$), o meio condutor biológico é eletricamente neutro em escala macroscópica. As correntes que saem da fonte (*source*) entram imediatamente no sumidouro (*sink*) a uma curta distância $d$, gerando um momento dipolar $p = I \cdot d$.

2. **Fontes Superficiais vs Fontes Profundas**:
   - Superfície cortical: $d \approx 1.5\text{--}2.0\text{ cm} \implies$ sinal captável ($10\text{--}100\ \mu\text{V}$).
   - Estruturas subcorticais profundas (tálamo, hipocampo, amígdala): $d \approx 7.0\text{--}9.0\text{ cm} \implies$ atenuação de $>25\text{ dB}$ em relação a fontes corticais equivalentes.

## 2. As Ferramentas de Código Desta Sala
- `field_decay_ratio(r1, r2, power=2)`: Calcula a relação analítica de decaimento $(r_1 / r_2)^p$.
- `audit_deep_source_snr(v_cortical_uv, d_cortical_cm, d_deep_cm, scalp_noise_uv)`: Modela numericamente o decaimento quadrático de uma fonte profunda e calcula se sua amplitude no escalpo atinge o limiar mínimo de detecção linear ($\text{SNR} \ge 2.0$, ou $+6\text{ dB}$).

Para destravar o lab, abra [Michel & Brunet EEG source imaging OA](https://pmc.ncbi.nlm.nih.gov/articles/PMC6700197/) e leia a revisão prática de imageamento de fonte em Michel e Brunet para a conta de campo no escalpo usar distância e orientação, não só amplitude.
