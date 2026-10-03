# Conceito — Teoria de Probabilidades em BCI: Variáveis Aleatórias e Distribuição Gaussiana

A modelagem de incerteza estocástica é a base da teoria da decisão e inferência bayesiana em interfaces neurais.

## 1. A Distribuição Normal (Gaussiana) Univariada
Uma variável aleatória contínua $X \sim \mathcal{N}(\mu, \sigma^2)$ é parametrizada pela média $\mu$ (esperança matemática) e variância $\sigma^2$ (dispersão):
$$f(x) = \frac{1}{\sigma \sqrt{2\pi}} \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)$$

Propriedades fundamentais:
- **Simetria:** A curva é perfeitamente simétrica em torno de $\mu$ (onde atinge o pico máximo $1 / (\sigma \sqrt{2\pi})$).
- **Regra Empírica:** $68.27\%$ da massa probabilística situa-se em $[\mu - \sigma, \mu + \sigma]$, e $95.45\%$ situa-se em $[\mu - 2\sigma, \mu + 2\sigma]$.
- **Integral Unitária:** A área total sob a curva é rigorosamente $1.0$: $\int_{-\infty}^{\infty} f(x)dx = 1$.

## 2. Nível de Acaso em Decisão Binária
Em um problema de escolha forçada entre duas classes mutuamente exclusivas e equiprováveis ($K = 2$), a probabilidade de acerto ao acaso em cada ensaio independente é:
$$P(\text{acerto}) = p_e = 0.5$$
A variância de uma variável Bernoulli com $p = 0.5$ é $\text{Var} = p(1 - p) = 0.25$.

## 3. Modos de Falha na Prática de Engenharia
1. **Desvio-Padrão Nulo ou Negativo:** Tentar avaliar a densidade com $\sigma \le 0$, provocando divisão por zero.
2. **Dados Fortemente Assimétricos:** Ajustar uma gaussiana em potências lineares brutas sem transformação logarítmica prévia, distorcendo os limiares de decisão bayesiana.

## O Que a Próxima Sala Assume
A próxima sala (`nt-math-estimation`) — **Math — Estimação e erro-padrão** — ensina o cálculo de intervalos de confiança e erro-padrão da média (SEM) em ensaios eletrofisiológicos com variância biológica.

## Artigos de Apoio e Leituras Recomendadas
- [Schlögl et al. κ in BCI](https://doi.org/10.1088/1741-2560/2/4/L02) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
