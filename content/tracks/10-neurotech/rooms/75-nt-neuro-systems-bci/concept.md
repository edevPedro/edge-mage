# Conceito — Ritmos Sensoriomotores (SMR), ERD e ERS

## 1. O Complexo Sensorimotor (S1/M1) e Alças Talamocorticais
O córtex sensoriomotor exibe oscilações eletroencefalográficas características em repouso, conhecidas genericamente como Ritmos Sensoriomotores (*Sensorimotor Rhythms* - SMR):
- **Ritmo $\mu$ (Mu):** Centrado na faixa de $8\text{--}12\text{ Hz}$, originado na área somatossensorial primária (S1) e córtex motor (M1).
- **Ritmo $\beta$ (Beta):** Centrado na faixa de $13\text{--}30\text{ Hz}$, associado à estabilidade postural e inibição motora corticoespinhal.

Esses ritmos refletem a atividade de alças oscilatórias de retroalimentação entre o tálamo (núcleo ventral lateral e ventral póstero-lateral) e as camadas piramidais corticais.

## 2. Dessincronização e Sincronização Relacionadas a Eventos
Conforme estabelecido pela literatura pioneira de Pfurtscheller & Lopes da Silva (1999):

1. **ERD (Event-Related Desynchronization):**
   - Redução da potência espectral em uma banda de frequência específica associada à ativação funcional ou planejamento motor.
   - Ocorre no córtex contralateral à parte do corpo imaginada ou movida.
2. **ERS (Event-Related Synchronization):**
   - Aumento da potência espectral em uma banda de frequência, associado à desativação ou inibição ativa de uma área cortical.
   - Tipicamente observado após o término de um movimento (*beta rebound*).

## 3. Formulação Matemática Padrão do ERD/ERS
A variação percentual de potência relativa à potência de uma época de repouso (*baseline*) é formalmente definida como:

$$\text{ERD}\% = \left( \frac{P_{baseline} - P_{task}}{P_{baseline}} \right) \times 100$$

Convenção adotada:
- **$\text{ERD}\% > 0$:** Dessincronização (a potência na tarefa $P_{task}$ é menor que na linha de base $P_{baseline}$).
- **$\text{ERD}\% < 0$:** Sincronização (a potência na tarefa superou a linha de base).
- Se $P_{task} = P_{baseline}$, a variação é $0\%$.
- Se a banda for completamente atenuada ($P_{task} = 0$), o ERD atinge seu limite máximo de $+100\%$.

## 4. O Sistema em Malha Fechada
O EEG de escalpo reflete o somatório populacional de correntes corticais. Em um BCI funcional de imagética motora, o usuário recebe feedback visual ou tátil derivado dessa estimativa de ERD, permitindo que o sistema biológico e o decodificador computacional convirjam gradualmente para um controle robusto.

## O Que a Próxima Sala Assume
A próxima sala (`nt-cs-complexity`) — **CS — Complexidade e budget de compute** — abre o pilar de ciência da computação avaliando a complexidade de algoritmos espaciais e orçamentos temporais de execução.

## Artigos de Apoio e Leituras Recomendadas
- [Singh et al. — MI-BCI review (PMC8003721)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8003721/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Wolpaw — BCI principles](https://doi.org/10.1016/j.clinph.2012.01.010) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
