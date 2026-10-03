# Conceito — Metodologia de Bake-Off: FBCSP vs. Classificadores Riemannianos

A comparação justa e reprodutível de pipelines de aprendizado de máquina (Bake-Off) exige paridade estrita em todas as etapas anteriores à extração de características.

## 1. Arquitetura do FBCSP (Filter Bank CSP)
1. **Decomposição em Sub-Bandas:** O sinal multicanal é filtrado em múltiplas bandas de frequência (ex. 9 bandas de $4\text{ Hz}$ de largura cobrindo de $4\text{ a } 40\text{ Hz}$: $4\text{--}8\text{ Hz}, 8\text{--}12\text{ Hz}, \dots$).
2. **Filtragem Espacial CSP por Banda:** Para cada banda $k$, ajustam-se $2m$ filtros espaciais CSP.
3. **Extração de Log-Variância:** Extraem-se características $f_{k, j} = \log_{10}(\text{Var}(w_{k, j}^T X_k))$.
4. **Seleção de Características e Classificação:** Algoritmos como Mutual Information Best Individual Features (MIBIF) selecionam os pares mais discriminantes para alimentar um classificador LDA.

## 2. Arquitetura Riemanniana (Tangent Space)
1. **Covariância Espacial:** Calcula-se a matriz de covariância amostral regularizada $\Sigma \in \mathbb{R}^{C \times C}$ no sinal passa-faixa amplo ($8\text{--}30\text{ Hz}$).
2. **Média de Fréchet e Projeção Tangente:** Calcula-se a média geométrica Riemanniana $\bar{\Sigma}$ e projetam-se as matrizes no espaço tangente euclidiano:
   $$v = \text{vect}(\log(\bar{\Sigma}^{-1/2} \Sigma \bar{\Sigma}^{-1/2}))$$
3. **Classificação Linear:** O vetor tangente euclidiano $v$ de dimensão $C(C+1)/2$ é alimentado diretamente a um classificador linear com regularização $L_2$ ou ElasticNet.

## 3. Modos de Falha em Benchmarks Competitivos
1. **Hiperparâmetros Otimizados no Teste:** Otimizar as sub-bandas do FBCSP olhando a pontuação do conjunto de teste, gerando overfitting e superioridade artificial sobre o modelo rival.
2. **Diferenças Ocultas de Pré-Processamento:** Usar filtros de ordens diferentes ou intervalos temporais desiguais entre os dois modelos.

## O Que a Próxima Sala Assume
A próxima sala (`nt-openbci-path`) — **Eletivo: caminho OpenBCI (stub)** — aprofunda o protocolo de comunicação serial, decodificação de pacotes binários de 24 bits e montagem de bancada com OpenBCI Cyton.

## Artigos de Apoio e Leituras Recomendadas
- [Ang et al. FBCSP](https://doi.org/10.1109/IJCNN.2008.4634130) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Barachant et al. Riemannian MDM](https://doi.org/10.1109/TBME.2011.2172210) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Yger et al. HAL review](https://inria.hal.science/hal-01394253/document) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
