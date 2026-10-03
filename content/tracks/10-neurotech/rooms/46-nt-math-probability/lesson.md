# Lição — Probabilidade e Limiar de Chance em BCI

## 1. Contexto Operacional
Na literatura científica de neurociência e BCI, nunca se avalia a acurácia de um decodificador de forma isolada do número de testes $N$. Em amostras pequenas, a variância do estimador amostral de acurácia é tão grande que altas taxas de acerto ocorrem frequentemente por puro ruído estocástico.

## 2. Passo a Passo Matemático

### Função Densidade Gaussiana 1D
$$f(x) = \frac{1}{\sigma \sqrt{2\pi}} \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)$$
Em Python, use `math.exp`, `math.sqrt` e `math.pi`.

### Limiar de Chance Binomial (Aproximação Normal)
Para $n$ trials e probabilidade base de acaso $p_{\text{chance}} = 0.5$ com nível de significância de $95\%$ ($\alpha = 0.05$ e $z = 1.645$):
1. Valide se $n_{\text{trials}} > 0$. Se não for, levante `ValueError`.
2. Calcule o desvio-padrão da proporção amostral:
   $$\sigma_p = \sqrt{\frac{p_{\text{chance}}(1 - p_{\text{chance}})}{n_{\text{trials}}}}$$
3. O limiar mínimo para rejeitar a hipótese nula é:
   $$\text{threshold} = p_{\text{chance}} + 1.645 \times \sigma_p$$

Para destravar o lab, abra [Schlögl et al. κ in BCI](https://doi.org/10.1088/1741-2560/2/4/L02) e leia como Schlögl separa acurácia de κ no dado de MI, para o limiar binomial do lab não ser lido como prova de decodificação.
