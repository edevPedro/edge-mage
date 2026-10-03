# Conceito — Métricas Rigorosas de BCI, Anti-Vazamento e Taxa de Wolpaw

A avaliação offline de classificadores neurais exige protocolos de validação herméticos contra vazamento de dados e métricas ajustadas pelo nível de chance probabilístico.

## 1. Vazamento de Dados (Data Leakage) em BCI
Ocorre vazamento de dados sempre que qualquer informação estatística do conjunto de teste contamina a fase de calibração ou treino. Principais manifestações:
1. **Vazamento por Pré-Processamento Global:** Calcular média, desvio-padrão, filtros espaciais (CSP) ou ICA utilizando a sessão inteira antes da separação de folds.
2. **Vazamento por Sobreposição Temporal:** Embaralhar janelas deslizantes (sliding windows) de forma que janelas contíguas com dados compartilhados caiam simultaneamente no treino e no teste.
3. **Vazamento por Deslocamento de Baseline:** Treinar e testar no mesmo bloco de poucos minutos, ignorando a não-estacionariedade e deriva eletroquímica de impedância entre blocos.

## 2. Coeficiente Kappa de Cohen ($\kappa$)
Mede a concordância inter-observador ajustada pela probabilidade de acerto ao acaso:
$$\kappa = \frac{p_o - p_e}{1 - p_e}$$
Onde $p_o$ é a acurácia observada e $p_e = \sum_{k=1}^K P(y=k) P(\hat{y}=k)$ é a probabilidade esperada de concordância aleatória. Em problemas balanceados com $K$ classes, $p_e = 1/K$.

## 3. Taxa de Transferência de Informação (Wolpaw ITR)
A métrica canônica proposta por Jonathan Wolpaw quantifica a velocidade de transmissão de informação útil em bits por minuto (bpm):
$$B = \log_2(N) + P \log_2(P) + (1 - P) \log_2\left(\frac{1 - P}{N - 1}\right)$$
$$\text{ITR} = B \times M$$
Onde:
- $N$: Número de classes de escolha.
- $P$: Acurácia do decodificador ($0 < P < 1$). Se $P = 1$, $B = \log_2(N)$.
- $M$: Número de decisões ou ensaios por minuto ($M = 60 / T_{\text{trial}}$).

## 4. Modos de Falha na Prática de Engenharia
1. **Comparações sem Nível de Acaso Declarado:** Relatar 60% de acurácia em 20 ensaios como "resultado significativo", ignorando que pela distribuição binomial exata o limiar de significância a $\alpha = 0.05$ é superior a 70%.
2. **Ignorar Custo Temporal no ITR:** Obter 95% de acurácia com janelas de 10 segundos ($M = 6\text{ ensaios/min}$) gerando um ITR muito inferior a um sistema com 80% de acurácia operando a cada 1.5 segundo ($M = 40\text{ ensaios/min}$).

## O Que a Próxima Sala Assume
A próxima sala (`nt-ml-neural`) — **ML para dados neurais** — explora modelos de aprendizado profundo compactos voltados para dados eletrofisiológicos (como EEGNet) frente a métodos lineares clássicos.

## Artigos de Apoio e Leituras Recomendadas
- [Padfield et al. (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Singh et al. MI-BCI review (Sensors 2021, PMC8003721)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8003721/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Schlögl et al. — Characterization of four-class MI EEG (JNE 2005; κ in BCI)](https://doi.org/10.1088/1741-2560/2/4/L02) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [sklearn — cohen_kappa_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [sklearn — LinearDiscriminantAnalysis](https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.LinearDiscriminantAnalysis.html) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [MNE-Python documentation](https://mne.tools/stable/index.html) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
