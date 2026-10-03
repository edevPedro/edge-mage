# Conceito — Paradigmas de Imagética Motora e Sincronização Temporal

A decodificação de biopotenciais depende criticamente da relação temporal entre eventos experimentais externos (estímulos visuais, auditivos ou táteis) e a dinâmica eletrofisiológica do córtex.

## 1. O Paradigma Clássico de Graz (Motor Imagery)
O protocolo padronizado de Imagética Motora divide cada ensaio (trial) em fases estritas:
1. **Fixação / Baseline ($t = 0\text{ s}$):** Uma cruz na tela indica ao sujeito para relaxar e focar a atenção, estabelecendo o nível de referência espectral.
2. **Estímulo / Cue ($t = 2\text{--}3\text{ s}$):** Uma seta indica a classe a ser imaginada (mão direita, mão esquerda, pés ou língua).
3. **Período de Imagética Ativa ($t = 3\text{--}7\text{ s}$):** O participante imagina a cinestesia do movimento (a sensação tátil e proprioceptiva de mover o membro, não apenas a imagem visual).
4. **Intervalo Inter-Ensaios (ITI):** Pausa aleatória ($1\text{--}3\text{ s}$) para evitar fadiga e desincronizar respostas antecipatórias.

## 2. Fatiamento Temporal de Epochs
Um epoch é o recorte do sinal contínuo multicanal em um intervalo semiaberto de amostras centrado em um marcador temporal (trigger):
$$\text{epoch} = X[\text{trigger} - \text{pre} : \text{trigger} + \text{post}]$$
Onde $\text{pre}$ é o número de amostras antes do evento e $\text{post}$ é o número de amostras após o evento. O comprimento total do epoch em amostras é $\text{pre} + \text{post}$.

## 3. Lateralidade Cortical e o Ritmo Sensoriomotor
- **Contralateralidade:** A imagética da mão direita desincroniza (ERD) o córtex motor esquerdo (eletrodo $C3$). A imagética da mão esquerda desincroniza o córtex motor direito (eletrodo $C4$).
- **Sincronização Ipsilateral (ERS):** Concomitantemente, o hemisfério que controla a mão inativa pode exibir um aumento relativo de sincronização.

## 4. Modos de Falha na Prática de Engenharia
1. **Mistura de Janelas Temporais:** Incluir o potencial evocado visual inicial (respostas P100 e N200 causadas pelo estímulo da tela) dentro da janela de decodificação motora, fazendo o modelo classificar o reflexo óptico em vez da imagética intencional.
2. **Jitter de Sincronismo de Hardware:** Se a placa de aquisição e o software de estímulo tiverem atrasos variáveis na marcação de triggers, os epochs ficarão desalinhados no tempo, destruindo a consistência das características espectrais.

## O Que a Próxima Sala Assume
A próxima sala (`nt-features-bandpower`) — **Potência de banda / covariância** — extrai vetores de características baseados na variância logarítmica das bandas e em matrizes de covariância espacial.

## Artigos de Apoio e Leituras Recomendadas
- [Padfield et al. EEG-MI (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Singh et al. MI-BCI review (Sensors 2021, PMC8003721)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8003721/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Pfurtscheller & Neuper — Motor imagery activates primary sensorimotor area (Neurosci Lett 1997)](https://doi.org/10.1016/S0304-3940(97)00889-6) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Neuper et al. — Imagery of motor actions (Cogn Brain Res 2005)](https://doi.org/10.1016/j.cogbrainres.2005.08.014) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
