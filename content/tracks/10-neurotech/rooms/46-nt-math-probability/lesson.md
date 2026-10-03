# Desafio — Função Densidade de Probabilidade Gaussiana (PDF)

## 1. Objetivo do Desafio
Implementar a função densidade de probabilidade (PDF) da distribuição normal univariada em Python puro sem dependências externas.

## 2. Especificação Técnica e Formulação
Dado um ponto escalar $x$, a média $\mu$ e o desvio-padrão $\sigma > 0$:
- Implemente a função `gaussian_pdf(x, mu, sigma)`:
  $$\text{pdf} = \frac{1}{\sigma \sqrt{2\pi}} \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)$$
- Utilize as constantes matemáticas `math.pi` e a função `math.exp`.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que $\sigma > 0$. Se $\sigma \le 0$, levante `ValueError("sigma deve ser positivo")`.
- Para $x = 0, \mu = 0, \sigma = 1$, o retorno deve ser aproximadamente $0.398942$.
