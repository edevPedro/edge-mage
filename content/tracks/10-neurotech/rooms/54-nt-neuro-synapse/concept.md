# Conceito — Transmissão Sináptica, Funções de Condutância e Geração de LFP

## 1. Potenciais Pós-Sinápticos (PSPs) vs. Potenciais de Ação
Enquanto os potenciais de ação são eventos puramente axônicos, digitais (tudo-ou-nada) e ultra-rápidos ($\sim 1\text{ ms}$), os potenciais pós-sinápticos são analógicos, graduados e temporalmente extensos ($10\text{ a }100\text{ ms}$):

- **EPSP (Excitatory Postsynaptic Potential):** Despolarização da membrana pós-sináptica, tipicamente mediada por receptores ionotrópicos glutamatérgicos (AMPA, NMDA) que promovem influxo de íons $Na^+$ e $Ca^{2+}$.
- **IPSP (Inhibitory Postsynaptic Potential):** Hiperpolarização da membrana, gerada por influxo de $Cl^-$ via receptores $\text{GABA}_A$ ou efluxo de $K^+$ via receptores $\text{GABA}_B$.

## 2. A Função Alfa de Condutância Sináptica
A evolução temporal da condutância pós-sináptica $g_{syn}(t)$ após a chegada de um spike é classicamente modelada pela função alfa de Rall:

$$g_{syn}(t) = g_{peak} \cdot \left(\frac{t}{\tau_{syn}}\right) \cdot \exp\left(1 - \frac{t}{\tau_{syn}}\right), \quad t \ge 0$$

Propriedades fundamentais:
- No instante $t = \tau_{syn}$, a condutância atinge seu pico exato: $g_{syn}(\tau_{syn}) = g_{peak} \cdot (1) \cdot e^0 = g_{peak}$.
- Para $t < 0$, $g_{syn}(t) = 0.0$.
- O decaimento assintótico reflete o fechamento dos canais iônicos e a recaptação do neurotransmissor da fenda sináptica.

## 3. Da Sinapse ao LFP e ao EEG
Neurônios piramidais nas camadas corticais III e V possuem árvores dendríticas apicais longas e orientadas perpendicularmente à superfície cortical. Quando uma sinapse excitatória despolariza o dendrito apical, íons positivos entram na célula criando um *sink* de corrente local no espaço extracelular. A conservação de carga elétrica exige que correntes passem pelo citoplasma e saiam pelo corpo celular (*source*).

Esse par sink-source separado espacialmente forma um dipolo de corrente primário:
$$V_{LFP}(r) = \frac{1}{4 \pi \sigma} \sum_i \frac{I_i}{|r - r_i|}$$

Por terem duração prolongada ($10\text{--}50\text{ ms}$), os PSPs somam-se linearmente no tempo e no espaço, dando origem ao Potencial de Campo Local (LFP) intracortical e, após atravessar crânio e tecidos, ao EEG de escalpo.

## O Que a Próxima Sala Assume
A próxima sala (`nt-rhythms`) — **Ritmos α/β/γ/µ** — investiga as oscilações cerebrais macroscópicas populacionais e a modulação dos ritmos alfa, beta, teta e gama no escalpo.

## Artigos de Apoio e Leituras Recomendadas
- [Einevoll et al. LFP (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3884846/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
