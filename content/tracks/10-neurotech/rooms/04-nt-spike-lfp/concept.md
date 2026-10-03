# Conceito — Spike → LFP: Escalas Temporais e Decaimento Espacial

## 1. Fundamento Físico e Bioelétrico
A atividade elétrica cerebral extracelular é dividida em dois regimes fundamentais com físicas e escalas distintas:

| Grandeza | Origem Biofísica | Duração / Banda | Decaimento Espacial | Amplitude Extracelular |
|---|---|---|---|---|
| **Spike (Potencial de Ação)** | Despolarização axonal rápida mediada por canais de $Na^+$/$K^+$ | $\sim 1\text{ ms}$ ($300\text{--}3000\text{ Hz}$) | Quadrupolo/Dipolo: $\sim 1/r^2$ a $1/r^3$ | $50\text{--}500\ \mu\text{V}$ (a $<50\ \mu\text{m}$) |
| **LFP (Local Field Potential)** | Somação de correntes pós-sinápticas (PSPs) em dendritos piramidais | $\sim 10\text{--}100\text{ ms}$ ($0.5\text{--}300\text{ Hz}$) | Dipolo aberto: $\sim 1/r^2$ a $1/r$ | $10\text{--}100\ \mu\text{V}$ no escalpo |

A física que rege a propagação extracelular foi documentada por [Buzsáki et al. (PMC4907333)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4907333/) e modelada computacionalmente por [Einevoll et al. (PMC3884846)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3884846/).

### O Modelo de Decaimento com a Distância
Para um spike somático com amplitude de referência $V_0$ a uma distância de calibração $r_0 = 20\ \mu\text{m}$, o potencial registrado por um eletrodo à distância $r$ decai rapidamente:

$$V(r) \approx V_0 \cdot \left(\frac{r_0}{r}\right)^2 \quad (\text{para } r \ge r_0)$$

- Em um microeletrodo intracortical posicionado a $r = 50\ \mu\text{m}$ do soma:
  $$V(50\ \mu\text{m}) = 100\ \mu\text{V} \cdot \left(\frac{20}{50}\right)^2 = 16\ \mu\text{V}$$
  Com um piso de ruído térmico/amplificador de $1.0\ \mu\text{V}_{\text{RMS}}$, a relação sinal-ruído é $\text{SNR} = 16.0 \ge 2.0$, permitindo a detecção clara e ordenamento (*spike sorting*).

- Em um eletrodo de EEG de escalpo posicionado a $r = 20\text{ mm} = 20.000\ \mu\text{m}$:
  $$V(20.000\ \mu\text{m}) = 100\ \mu\text{V} \cdot \left(\frac{20}{20.000}\right)^2 = 100 \cdot 10^{-6}\ \mu\text{V} = 0.0001\ \mu\text{V}$$
  O sinal é atenuado por um fator de $1.000.000\times$, afundando ordens de grandeza abaixo do ruído térmico Johnson de qualquer eletrodo e do piso do conversor analógico-digital.

## 2. Modos de Falha Operacionais
1. **Confundir LFP com Spike Filtrado**: Supor que o LFP é apenas uma média móvel de potenciais de ação. Na realidade, potenciais de ação de neurônios vizinhos são assíncronos e sofrem cancelamento destrutivo quase total. O LFP reflete a somação espacial de potenciais pós-sinápticos excitatórios e inibitórios (EPSPs/IPSPs) orientados espacialmente ao longo dos dendritos apicais paralelos das células piramidais corticais.
2. **Prometer Spike Sorting no Escalpo**: Desenvolvedores convencionais frequentemente tentam subir a taxa de amostragem de um EEG de escalpo para $10\text{ kHz}$ acreditando que vão "pegar spikes individuais de neurônios". A física do meio e a atenuação geométrica tornam spikes de neurônios únicos indetectáveis no escalpo, não importando a taxa de amostragem do ADC.

## 3. O que a Próxima Sala Assume
A sala seguinte (`nt-volume-blur` (Condução de volume e borrão espacial)) assume que você compreende que os potenciais captados no escalpo são somações de dipolos de corrente síncronos (LFPs macroscópicos). Ela estuda como esses dipolos sofrem dispersão lateral e filtragem espacial ao atravessar as diferentes camadas condutoras da cabeça (LCR, osso craniano de alta resistividade e pele).
