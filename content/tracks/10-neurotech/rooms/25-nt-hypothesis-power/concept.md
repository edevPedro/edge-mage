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

## O Que a Próxima Sala Assume
A próxima sala (`nt-cv-leakage`) — **CV aninhado e vazamento de trial** — previne vazamento de dados (data leakage) e superestimação de desempenho utilizando validação cruzada aninhada.

## Artigos de Apoio e Leituras Recomendadas
- [Combrisson & Jerbi 2015 — statistical testing MEG/EEG](https://doi.org/10.1016/j.jneumeth.2015.03.034) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Belmont Report (OHRP)](https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/index.html) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
