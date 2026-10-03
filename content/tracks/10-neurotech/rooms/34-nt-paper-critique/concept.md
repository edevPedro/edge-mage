# Conceito — Avaliação Crítica de Literatura em BCI e Detecção de Red Flags

A capacidade de avaliar criticamente a literatura científica internacional é o pré-requisito indispensável para evitar desperdício de meses de pesquisa tentando replicar alegações espúrias.

## 1. As Principais "Red Flags" Metodológicas em BCI
Ao analisar qualquer publicação na área de interfaces cérebro-computador, audite imediatamente:
1. **Vazamento de Dados por Sobreposição Temporal:** Particionamento aleatório (`shuffle=True`) de janelas deslizantes contíguas, inflacionando artificialmente a acurácia.
2. **Normalização Pré-Split:** Aplicação de Z-score, PCA ou ICA sobre o conjunto de dados completo antes da divisão dos folds de treino e teste.
3. **Falta de Reprodutibilidade:** Ausência de link permanente com identificador de objeto digital (DOI) para dados abertos e código-fonte documentado.
4. **Overclaims de Generalização:** Afirmações bombásticas de "leitura da mente" ou "controle universal sem calibração" baseadas em apenas 3 a 5 participantes sem validação cruzada entre sessões (cross-session).
5. **Métricas Não-Ajustadas:** Reportar apenas acurácia simples sem informar o coeficiente Kappa de Cohen ($\kappa$) ou a concordância esperada pelo acaso para classes desbalanceadas.

## 2. A Ficha Estruturada de Leitura Crítica
Uma crítica técnica estruturada deve registrar:
- **DOI / URL Permanente:** Referência imutável do estudo analisado.
- **Tamanho da Amostra e Tarefa:** Número de voluntários, canais de EEG e paradigma (MI, P300, SSVEP).
- **Pipeline Declarado:** Algoritmos exatos de filtragem, extração de features e classificação.
- **Pontos Fortes e Fraquezas Metodológicas:** O que o artigo comprova legitimamente e quais alegações carecem de suporte experimental.

## O Que a Próxima Sala Assume
A próxima sala (`nt-research-proposal`) — **Proposta de pesquisa (mini)** — redige uma proposta formal de dissertação com hipótese falseável, plano experimental e cronograma de pesquisa.

## Artigos de Apoio e Leituras Recomendadas
- [Singh et al. Sensors 2021 MI-BCI](https://doi.org/10.3390/s21062173) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Padfield et al. Sensors 2019 EEG-MI](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
