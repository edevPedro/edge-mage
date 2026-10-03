# Desafio — Spike → PSP → LFP

## 1. Objetivo do Desafio
Analisar as três escalas fundamentais da bioeletricidade e realizar a auditoria biofísica de detectabilidade extracelular.

## 2. As Três Escalas da Bioeletricidade
1. **Potencial de Ação (Spike)**:
   - Duração: $\sim 1\text{ ms}$.
   - Banda espectral: $300\text{--}3000\text{ Hz}$.
   - Gerador: Despolarização axonal rápida via condutâncias ativas dependentes de voltagem ($Na^+$ e $K^+$).
   - Detecção: Apenas intracelular ou com microeletrodos extracelulares penetrantes a $<100\ \mu\text{m}$ do soma.

2. **Potenciais Pós-Sinápticos (PSPs)**:
   - Duração: $10\text{--}100\text{ ms}$.
   - Banda espectral: $0.5\text{--}100\text{ Hz}$.
   - Gerador: Correntes transmembrana dendríticas desencadeadas por neurotransmissores em sinapses excitatórias e inibitórias.
   - Geometria: Neurônios piramidais orientados perpendicularmente à superfície cortical formam dipolos alinhados em paliçada, permitindo somação linear de correntes extracelulares.

3. **Potencial de Campo Local (LFP) e EEG**:
   - O LFP é a somação do campo extracelular gerado por milhares a milhões de dendritos ativados sincronicamente.
   - No escalpo (EEG), essa somação atravessa o líquor, crânio e couro cabeludo, sofrendo atenuação e filtro passa-baixa espacial.

## 2. A Auditoria de Detectabilidade Extracelular
No laboratório de código desta sala, você implementará duas ferramentas:
1. `separate_spike_lfp(signal, win)`: Decomposição de sinal biológico multiescala em componentes lentas (LFP) e resíduos rápidos (spikes).
2. `audit_spike_detectability(spike_amplitude_uv, distance_um, noise_floor_uv)`: Auditoria biofísica que calcula a atenuação $V(r) = V_0 (r_0/r)^2$ e verifica se o sinal atinge uma relação sinal-ruído mínima ($\text{SNR} \ge 2.0$) para detecção acima do ruído térmico do amplificador.

Para destravar o lab, abra [Einevoll et al. — Modelling and analysis of LFP (PMC3884846)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3884846/) e leia a distinção de Einevoll entre LFP (correntes sinápticas somadas) e spike, para a auditoria de detectabilidade com atenuação 1/r².
