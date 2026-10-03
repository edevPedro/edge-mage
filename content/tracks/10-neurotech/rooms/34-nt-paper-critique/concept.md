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

## 3. O que a Próxima Sala Assume
A próxima sala (`nt-research-proposal`) desafia o estudante a formular sua própria proposta formal de pesquisa de mestrado baseada em uma pergunta científica legítima e testável.

## 4. Ponto de Destrave do Lab
Consulte as diretrizes internacionais de transparência e reprodutibilidade em neuroimagem de [Poldrack et al. (Nature 2017)](https://doi.org/10.1038/s41562-016-0017) e o manifesto de [Ioannidis (PLoS Med 2005, Why most published research findings are false)](https://doi.org/10.1371/journal.pmed.0020124).
