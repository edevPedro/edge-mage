# História — Os Olhos Espaciais do Córtex Motor

Na bancada de análise de algoritmos de BCI, uma desenvolvedora observa o mapa de 64 eletrodos de escalpo de um voluntário durante a imagética motora da mão direita versus mão esquerda. Quando ela calcula a potência de banda diretamente nos eletrodos individuais $C3$ e $C4$, a sobreposição de distribuições é grande: a condução de volume do crânio borra o sinal elétrico e mistura os ritmos dos dois hemisférios, degradando o classificador linear.

O pesquisador de aprendizado de máquina senta-se ao terminal e abre a decomposição em Padrões Espaciais Comuns (Common Spatial Patterns - CSP):
— Em vez de confiar em eletrodos físicos individuais, podemos combinar linearmente todos os 64 canais simultaneamente usando um vetor de pesos espaciais $w \in \mathbb{R}^{64}$ — explica o pesquisador. — O objetivo do CSP é encontrar um filtro espacial linear $s = w^T X$ tal que a variância do sinal filtrado seja maximizada para a Classe 1 (mão direita) e, ao mesmo tempo, minimizada para a Classe 2 (mão esquerda).

Ele demonstra a formulação matemática elegante do problema de autovalores generalizados:
$$\Sigma_1 w = \lambda \Sigma_2 w$$
Onde $\Sigma_1$ e $\Sigma_2$ são as matrizes médias de covariância espacial das duas classes. Os autovetores correspondentes aos maiores autovalores $\lambda$ destacam a atividade motora da mão direita atenuando a mão esquerda; os autovetores correspondentes aos menores autovalores realizam o inverso exato.

— A característica final não é o sinal filtrado no tempo, mas a log-variância do sinal projetado: $f = \log_{10}(\text{Var}(w^T X))$ — orienta o pesquisador. — E atenção redobrada: o CSP deve ser treinado *exclusivamente* com os dados do fold de treino. Se você calcular as matrizes de covariância CSP usando todo o dataset antes da validação cruzada, você vazará a estrutura espacial do teste e invalidará toda a sua pesquisa!

A desenvolvedora implementa a projeção espacial e o cálculo da log-variância (`spatial_filter_logvar`). Quando os dois primeiros filtros CSP são aplicados, as classes separam-se com contraste geométrico perfeito, elevando o Cohen's Kappa para além de 0.70.
