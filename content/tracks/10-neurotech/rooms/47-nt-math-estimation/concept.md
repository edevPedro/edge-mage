# Conceito — Estimação de Parâmetros, Erro Padrão e Correção de Bessel

A estimação estatística transforma observações amostrais ruidosas em inferências confiáveis sobre a população geradora de biopotenciais.

## 1. O Erro Padrão da Média (Standard Error - SE)
O desvio-padrão $\sigma$ mede a dispersão dos dados individuais em torno da média. Já o Erro Padrão da Média (SE) quantifica a incerteza associada à própria estimativa da média amostral:
$$\text{SE} = \frac{\sigma}{\sqrt{N}}$$
- Para reduzir o erro da estimativa pela metade (fator de $2$), é estritamente necessário quadruplicar o número de ensaios ($4N$).

## 2. A Correção de Bessel e o Viés Amostral
Ao estimar a covariância a partir de $T$ amostras com a média estimada a partir dos próprios dados:
- O estimador ingênuo $\frac{1}{T} X X^T$ subestima a verdadeira dispersão da população porque os desvios são calculados em relação à média amostral (que minimiza a soma dos quadrados por definição).
- O estimador não-viesado (unbiased estimator) aplica a correção de Bessel dividindo por graus de liberdade $T - 1$:
  $$\Sigma_{\text{unbiased}} = \frac{1}{T - 1} \sum_{t=1}^T (x[t] - \bar{x})(x[t] - \bar{x})^T$$

## 3. Modos de Falha na Prática de Engenharia
1. **Subdimensionamento Amostral:** Coletar poucos ensaios e acreditar que a média observada é um número exato sem margem de erro.
2. **Confundir Desvio-Padrão com Erro Padrão:** Publicar barras de erro com SE (que é menor) para fazer os dados parecerem menos ruidosos do que são.

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-math-gd-lite`) introduz os fundamentos de otimização contínua via Gradiente Descendente para ajuste de modelos neurais.

## 5. Ponto de Destrave do Lab
Consulte o tratamento clássico de estimação não-viesada em [Wasserman (All of Statistics, Springer)](https://link.springer.com/book/10.1007/978-0-387-21736-9).
