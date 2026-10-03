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

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-csp-primer`) introduz o método clássico de Common Spatial Patterns (CSP), onde o vazamento de dados por ajuste global é particularmente fatal.

## 5. Ponto de Destrave do Lab
Para o estudo do impacto de vazamento temporal e boas práticas de validação cruzada em BCI, consulte [Varoquaux (NeuroImage 2018, Cross-validation failure in predictive neuroimaging)](https://doi.org/10.1016/j.neuroimage.2017.06.061) e [Lemm et al. (NeuroImage 2011, Introduction to machine learning for BCI)](https://doi.org/10.1016/j.neuroimage.2010.11.004).
