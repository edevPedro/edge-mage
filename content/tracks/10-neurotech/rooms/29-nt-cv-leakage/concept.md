# Conceito — Validação Cruzada em Blocos (Blocked CV) e Auditoria Anti-Vazamento

A natureza contínua e autocorrelacionada no tempo dos sinais de EEG torna a validação cruzada ingênua uma das maiores fontes de publicações não-reproduzíveis em neurotecnologia.

## 1. O Mecanismo do Vazamento por Sobreposição Temporal
Se janelas temporais deslizantes de tamanho $W$ e passo $S < W$ forem divididas aleatoriamente:
$$\text{Sobreposição} = \frac{W - S}{W} \times 100\%$$
Uma janela no conjunto de teste compartilha quase todas as suas amostras físicas com uma janela no conjunto de treino. O classificador atinge acurácia artificialmente inflacionada porque atua como uma tabela de consulta (lookup table) de ruído correlacionado.

## 2. Validação Cruzada em Blocos (Blocked / Group CV)
Para garantir separabilidade estrita:
1. **Split por Ensaios Inteiros (Trial-Level Split):** Todas as janelas pertencentes ao ensaio $k$ são mantidas no mesmo fold.
2. **Split por Blocos de Sessão (Run-Level Split / Leave-One-Run-Out):** Se o protocolo gravou 4 blocos de 10 minutos, o modelo é treinado em 3 blocos e testado no bloco restante, expondo o algoritmo à deriva real de impedância e estado cognitivo.
3. **Validação Aninhada (Nested CV):** Otimização de hiperparâmetros (como penalidade $C$ do SVM ou regularização de covariância) deve ocorrer exclusivamente dentro de uma malha interna de validação cruzada (inner fold).

## 3. Modos de Falha na Prática de Engenharia
1. **Fit de Scaler Global:** Ajustar `StandardScaler` sobre a matriz inteira antes de dividir os folds.
2. **Treinar e Testar no Mesmo Ponto de Baseline:** Usar o início do próprio trial de teste para normalizar o teste sem protocolo causal.

## O Que a Próxima Sala Assume
A próxima sala (`nt-decode-mvp`) — **Decode MVP (labels → LDA → κ)** — integra o primeiro pipeline completo de decodificação supervisionada com classificador Linear Discriminant Analysis (LDA).

## Artigos de Apoio e Leituras Recomendadas
- [Lotte et al. JNE 2007](https://doi.org/10.1088/1741-2560/4/2/R01) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Varoquaux et al. 2017 — assessing prediction](https://doi.org/10.1016/j.neuroimage.2016.10.038) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
