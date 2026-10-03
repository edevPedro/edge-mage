# Conceito — Dissecação e Reprodutibilidade de Artigos de BCI

A capacidade de ler criticamente, dissecar o pipeline e replicar resultados publicados na literatura internacional de neuroengenharia é o alicerce para qualquer atuação em nível de pós-graduação (MSc/PhD) ou pesquisa aplicada industrial.

## 1. Componentes Essenciais de um Artigo em Neurotecnologia
Um trabalho científico reprodutível de BCI deve explicitar inequivocamente:
1. **Origem dos Dados e Ética:** Identificador do comitê de ética (IRB), termo de consentimento, número de sujeitos e link público permanente do dataset (DOI ou repositório aberto como PhysioNet ou Zenodo).
2. **Hardware e Aquisição:** Modelo do amplificador/conversor (ex. ADS1299, g.tec), taxa de amostragem ($f_s$), eletrodos utilizados (sistema 10-20) e eletrodo de referência.
3. **Pré-Processamento e Causalidade:** Tipo e ordem dos filtros digitais, frequências de corte, tratamento de artefatos e fatiamento de epochs.
4. **Extração de Características e Modelagem:** Formulação matemática do extrator (bandpower, CSP, Riemann) e hiperparâmetros do classificador.
5. **Protocolo de Validação:** Esquema de particionamento (Block K-Fold / Leave-One-Run-Out), métricas descontando o acaso (Cohen's Kappa) e significância estatística.

## 2. O Papel do Checkpoint de Paper
O ritual de checkpoint de paper exige a criação de um documento formal de registro (`study-log/artifacts/checkpoint-paper.md`) contendo a citação do artigo, URL acessível e a descrição técnica do pipeline que conecta a teoria à prática de laboratório.

## 3. Modos de Falha na Literatura Científica
1. **Omissão de Hiperparâmetros de Filtragem:** Artigos que mencionam apenas "sinal foi filtrado entre 8 e 30 Hz", sem declarar se o filtro foi causal ou bidirecional (filtfilt), impossibilitando avaliar se o método funciona em tempo real.
2. **Datasets Fantasma:** Publicações que utilizam bases privadas não compartilhadas e alegam acurácias mirabolantes sem permitir auditoria independente de vazamento de dados.

## O Que a Próxima Sala Assume
A próxima sala (`nt-checkpoint-project`) — **Ritual fatia de projeto** — consolida a fatia prática executável de engenharia conectando hardware, software e validação estatística.

## Artigos de Apoio e Leituras Recomendadas
- [Singh et al. MI-BCI review (Sensors 2021, PMC8003721) — CP-MI map](https://pmc.ncbi.nlm.nih.gov/articles/PMC8003721/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Padfield et al. EEG-MI techniques (PMC6471241)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Yger et al. HAL — CP-Riemann figure](https://inria.hal.science/hal-01394253/document) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
