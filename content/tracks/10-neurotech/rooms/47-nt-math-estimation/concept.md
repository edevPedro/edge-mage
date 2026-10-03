# Conceito — Estimação Amostral, Erro-Padrão e Correção de Bessel

A calibragem de algoritmos de BCI frequentemente ocorre em condições de poucos dados: sessões curtas de gravação de apenas 10 a 40 epochs por classe. Em regimes de pequena amostragem, a escolha entre estimadores enviesados e não enviesados altera diretamente a estabilidade numérica dos modelos lineares.

## 1. O Fundamento Matemático do Lab

### O Estimador de Média e Erro-Padrão
Para $N$ observações independentes e identicamente distribuídas com variância $\sigma^2$:
$$\bar{x} = \frac{1}{N}\sum_{i=1}^N x_i, \quad SE = \frac{\sigma}{\sqrt{N}}$$
Para reduzir o erro-padrão pela metade, é necessário quadruplicar o número de trials ($N \to 4N$).

### O Viés da Variância Amostral (Correção de Bessel)
O estimador ingênuo de máxima verossimilhança (MLE) divide a soma dos desvios quadráticos por $N$:
$$S^2_{\text{biased}} = \frac{1}{N} \sum_{i=1}^N (x_i - \bar{x})^2$$

Como a média verdadeira $\mu$ é desconhecida e substituída pela média amostral $\bar{x}$, as amostras estão mais próximas de $\bar{x}$ do que de $\mu$. O valor esperado desse estimador é:
$$\mathbb{E}[S^2_{\text{biased}}] = \frac{N - 1}{N} \sigma^2$$
O estimador subestima sistematicamente a variância verdadeira por um fator de $(N-1)/N$.

Para eliminar esse viés, a **Correção de Bessel** utiliza o divisor $N - 1$:
$$S^2_{\text{unbiased}} = \frac{1}{N - 1} \sum_{i=1}^N (x_i - \bar{x})^2, \quad \mathbb{E}[S^2_{\text{unbiased}}] = \sigma^2$$

A razão entre o estimador enviesado e o não enviesado é analiticamente exata:
$$\text{bias\_factor} = \frac{S^2_{\text{biased}}}{S^2_{\text{unbiased}}} = \frac{N - 1}{N}$$
Para $N = 4$ amostras, o estimador ingênuo entrega apenas $75\%$ da dispersão real (um viés massivo de $-25\%$).

## 2. Unidades e Grandeza Física
- **Média ($\bar{x}$):** $\mu\text{V}$ (microvolts).
- **Variância e Covariância ($S^2, \Sigma$):** $\mu\text{V}^2$.
- **Fator de Viés:** Adimensional, no intervalo $[0.5, 1.0)$ para $N \ge 2$.

## 3. Modos de Falha na Prática de Engenharia
1. **Calibração com $1/N$ em Janelas Curtas:** Ao estimar a matriz de dispersão de ruído intrínseco com $N=8$ epochs em uma rotina de calibração rápida, dividir por $N$ reduz a variância estimada em $12.5\%$, superestimando a confiança das fronteiras de decisão do LDA e causando falsos positivos em tempo real.
2. **Matriz de Covariância Multidimensional:** Na covariância entre canais, o mesmo divisor $N-1$ é estritamente obrigatório para manter a propriedade não enviesada: $\Sigma = \frac{1}{N-1}\sum (x_i - \bar{x})(x_i - \bar{x})^T$.

## 4. O que a Próxima Sala Assume
A sala seguinte ([`nt-math-gd-lite`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/48-nt-math-gd-lite/room.yaml)) assume que você compreende gradientes e erros de estimação ao calcular atualizações de pesos que minimizam a perda empírica.

## 5. Ponto de Destrave do Lab
Para aprofundar nos testes de hipótese e poder estatístico em eletrofisiologia humana, consulte o paper de referência de [Combrisson & Jerbi (2015, DOI 10.1016/j.jneumeth.2015.03.034)](https://doi.org/10.1016/j.jneumeth.2015.03.034).
