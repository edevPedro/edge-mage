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

## 5. O que a Próxima Sala Assume
A próxima sala (`nt-stream-buffer`) passa da análise offline para a engenharia de tempo real, construindo a estrutura de dados de buffer circular (ring buffer) para suportar fluxos contínuos de dados.

## 6. Ponto de Destrave do Lab
Para a formulação da métrica ITR e avaliação padronizada de BCI, consulte o trabalho clássico de [Wolpaw et al. (IEEE TBME 2000)](https://doi.org/10.1109/10.841380) e [Schlögl et al. (J Neural Eng 2005, Characterization of four-class MI)](https://doi.org/10.1088/1741-2560/2/4/L02).
