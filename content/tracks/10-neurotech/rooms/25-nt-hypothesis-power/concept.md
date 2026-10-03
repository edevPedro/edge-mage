# Conceito — Poder Estatístico, Tamanho de Efeito (d de Cohen) e Múltiplos Testes

A busca por padrões em séries temporais de alta densidade neural expõe o pesquisador ao risco massivo de inflação de falsos positivos devido à multiplicidade de testes.

## 1. A Inflação do Erro Tipo I em Comparações Múltiplas
Ao realizar $M$ testes estatísticos independentes, cada um ao nível de significância $\alpha$:
$$\text{Probabilidade de pelo menos um falso positivo} = 1 - (1 - \alpha)^M$$
Para $M = 20$ testes a $\alpha = 0.05$, a probabilidade de falso alarme sobe para $1 - 0.95^{20} \approx 64\%$. Para $M = 100$, ela atinge $99.4\%$.

### Correção de Bonferroni
Ajusta o limiar de rejeição para cada teste individual de forma estrita:
$$\alpha_{\text{Bonferroni}} = \frac{\alpha}{M}$$
Garante que a taxa de erro global da família de testes (FWER) permaneça $\le \alpha$.

## 2. Tamanho de Efeito: O $d$ de Cohen
O valor-p informa apenas se um efeito é improvável sob a hipótese nula, mas não sua relevância prática. O tamanho de efeito $d$ de Cohen padroniza a magnitude da diferença entre duas médias:
$$d = \frac{\mu_1 - \mu_2}{s_{\text{pooled}}}, \quad s_{\text{pooled}} = \sqrt{\frac{s_1^2 + s_2^2}{2}}$$
- $|d| < 0.2$: Efeito desprezível.
- $|d| \approx 0.5$: Efeito moderado.
- $|d| \ge 0.8$: Efeito grande (robusto para classificação de BCI).

## 3. Poder Estatístico ($1 - \beta$)
É a probabilidade de rejeitar corretamente a hipótese nula quando um efeito real existe. Em BCI, estudos com baixo poder estatístico sofrem da maldição do vencedor (winner's curse): efeitos superestimados que nunca se repetem na replicação.

## 4. Modos de Falha na Prática de Engenharia
1. **P-Hacking por Seleção Pós-Hoc:** Varrer dezenas de bandas e selecionar apenas a frequência que atingiu $p < 0.05$ sem reportar a quantidade total de tentativas exploratórias.
2. **Confundir Significância com Utilidade:** Encontrar $p = 0.001$ com um tamanho de efeito minúsculo ($d = 0.05$) em um dataset massivo, descobrindo que o modelo é inútil para controle em tempo real.

## 5. O que a Próxima Sala Assume
A próxima sala (`nt-dsp-welch`) aprofunda na estimação de densidade espectral de potência (PSD) via método de Welch e na prevenção de vazamento espectral.

## 6. Ponto de Destrave do Lab
Consulte o guia clássico sobre tamanho de efeito e poder estatístico em [Cohen (Statistical Power Analysis for the Behavioral Sciences, 1988)](https://doi.org/10.4324/9780203771587) e [Benjamini & Hochberg (J R Stat Soc B 1995, Controlling the False Discovery Rate)](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
