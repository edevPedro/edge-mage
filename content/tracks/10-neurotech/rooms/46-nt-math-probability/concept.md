# Conceito — Probabilidade, Distribuição Gaussiana e Nível de Acaso (Chance Level)

Em avaliação de interfaces cérebro-computador, a acurácia bruta de classificação é uma métrica enganosa se desacompanhada do tamanho amostral ($N$) e do nível de significância estatística do acaso.

## 1. O Fundamento Matemático do Lab

### Densidade Gaussiana Unidimensional
O ruído biofísico de fundo em canais de EEG e as projeções de features em classificadores lineares tendem assintoticamente a uma distribuição Normal pelo Teorema Central do Limite:
$$f(x; \mu, \sigma) = \frac{1}{\sigma \sqrt{2\pi}} \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)$$

### O Limiar de Acaso Binomial (Combrisson & Jerbi, 2015)
Em um paradigma com 2 classes perfeitamente balanceadas ($p = 0.5$), um classificador aleatório que joga cara-ou-coroa acerta $k$ trials em $N$ tentativas segundo a distribuição Binomial $B(N, 0.5)$.

Para que um sistema de BCI comprove que decodificou intenção neural genuína e não sorte aleatória com nível de confiança de 95% ($\alpha = 0.05$), a acurácia observada deve superar o percentil 95 da distribuição binomial. Pela aproximação normal com $z_{0.95} = 1.645$:
$$\text{Limiar}_{95\%} = p_{\text{chance}} + 1.645 \sqrt{\frac{p_{\text{chance}}(1 - p_{\text{chance}})}{N}}$$

- Para $N = 100$ trials: o limiar é $50\% + 1.645 \sqrt{0.25/100} = 50\% + 8.2\% = 58.2\%$.
- Para $N = 20$ trials: o limiar é $50\% + 1.645 \sqrt{0.25/20} = 50\% + 18.4\% = 68.4\%$.
- Se o seu modelo obtém $65\%$ de acurácia em 20 trials, seu BCI **falhou** ($p > 0.05$).

## 2. Unidades e Grandeza Física
- **Acurácia e Probabilidade:** Adimensionais, variando no intervalo fechado $[0, 1]$ (ou expressos em porcentagem $0\text{--}100\%$).
- **Densidade gaussiana:** Inverso da unidade da feature ($\mu\text{V}^{-1}$).

## 3. Modos de Falha na Prática de Engenharia
1. **A Falácia do "60% é Maior que 50%":** Testar um decodificador com poucas epochs ($N < 30$) e comemorar uma taxa de acerto de 60%, ignorando que a dispersão de Bernoulli em amostras pequenas atinge 65% facilmente por puro ruído.
2. **Classes Desbalanceadas:** Se 80% dos trials forem da Classe 0 e 20% da Classe 1, o nível de chance trivial é 80% (basta um classificador burro predizer sempre 0). Nesses casos, o limiar teórico se desloca e a acurácia deve ser abandonada em favor do Cohen's Kappa ($\kappa$).

## 4. O que a Próxima Sala Assume
A sala seguinte ([`nt-math-estimation`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/47-nt-math-estimation/room.yaml)) assume que você entende como o tamanho amostral $N$ rege o erro-padrão de estimadores de média e covariância ($SE = \sigma/\sqrt{N}$).

## 5. Ponto de Destrave do Lab
Para sanar dúvidas na modelagem estatística de significância em neurociência computacional, consulte o paper de referência de [Combrisson & Jerbi (2015, DOI 10.1016/j.jneumeth.2015.03.034)](https://doi.org/10.1016/j.jneumeth.2015.03.034) e a análise de Cohen's Kappa em BCI por [Schlögl et al. (DOI 10.1088/1741-2560/2/4/L02)](https://doi.org/10.1088/1741-2560/2/4/L02).
