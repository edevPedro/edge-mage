# Conceito — Ritmos Eletroencefalográficos e Modulação Sensoriomotora

A atividade bioelétrica espontânea do cérebro organiza-se em bandas de frequência características, geradas por alças oscilatórias tálamo-corticais e circuitos de interneurônios inibitórios.

## 1. O Fundamento Biofísico das Bandas Espectrais
O espectro contínuo de EEG é convencionalmente dividido em bandas clássicas:
- **Delta ($0.5	ext{--}4	ext{ Hz}$):** Oscilações lentas de grande amplitude ($> 50\ \mu	ext{V}$), características de sono profundo de ondas lentas (NREM estágio 3) ou patologias encefálicas em vigília.
- **Theta ($4	ext{--}8	ext{ Hz}$):** Associadas a sonolência, memória de trabalho e navegação espacial (ritmo theta hipocampal).
- **Alfa e Mu ($8	ext{--}12	ext{ Hz}$):** 
  - **Alfa:** Predominância occipital em vigília relaxada com olhos fechados; reflete inibição ativa do córtex visual.
  - **Mu ($\mu$):** Ritmo sensoriomotor registrado sobre o córtex motor primário ($C3$, $Cz$, $C4$); atenua-se com o movimento real ou imaginado.
- **Beta ($12	ext{--}30	ext{ Hz}$):** Vigília ativa, processamento cognitivo e dinâmica motora. Em tarefas motoras, exibe rebote pós-movimento (ERS - Sincronização Relacionada a Evento).
- **Gama ($> 30	ext{ Hz}$):** Vinculação temporal de informações e atenção focal; amplitudes muito baixas no escalpo ($< 5\ \mu	ext{V}$) e altamente vulnerável a contaminação por eletromiograma (EMG) muscular craniano.

## 2. Dinâmica ERD/ERS em BCI de Imagética Motora
Em tarefas de imagética motora (Motor Imagery - MI):
- **ERD (Event-Related Desynchronization):** Queda de potência nas bandas $\mu$ e $eta$ no hemisfério contralateral ao membro imaginado, provocada pela ativação assíncrona das populações neuronais piramidais.
- **ERS (Event-Related Synchronization):** Aumento de potência no hemisfério ipsilateral ou rebote de beta após o término da tarefa motora.

## 3. Modos de Falha na Prática de Engenharia
1. **Confundir Ritmo Alfa Occipital com Ritmo Mu Motor:** Como ambos ocupam a faixa de $8	ext{--}12	ext{ Hz}$, filtros projetados sem referência espacial podem capturar variações no relaxamento visual do voluntário em vez de intenção motora.
2. **Confundir Banda Gama com Contaminação de EMG:** Atividade acima de $30	ext{ Hz}$ é dominada por contrações musculares da face e do pescoço, levando modelos ingênuos a "aprender" movimentos de mandíbula em vez de modulação cortical.

## O Que a Próxima Sala Assume
A próxima sala (`nt-neuro-maps`) — **Neurociência — Mapas corticais e 10–20** — mapeia a topografia do homúnculo sensoriomotor de Penfield e a nomenclatura internacional de eletrodos 10-20.

## Artigos de Apoio e Leituras Recomendadas
- [EEG MI — Techniques and Challenges (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Singh et al. — MI-BCI comprehensive review (Sensors 2021, PMC8003721)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8003721/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Pfurtscheller & Lopes da Silva — Event-related EEG/MEG synchronization (review)](https://doi.org/10.1016/S1388-2457(99)00141-8) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
