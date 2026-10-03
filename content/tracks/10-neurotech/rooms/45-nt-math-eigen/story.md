# História — O Eixo da Maior Variância

No laboratório de inteligência artificial biomédica, um pesquisador analisa a matriz de covariância espacial $2 \times 2$ gerada por dois eletrodos centrais adjacentes: $C3$ e $Cz$. Os dados covariam intensamente devido à condução de volume craniana: quando $C3$ sobe, $Cz$ também sobe, gerando uma nuvem elíptica inclinada no plano cartesiano.

O pesquisador quer encontrar a direção espacial na qual o sinal exibe a maior oscilação de potência, para posicionar um filtro espacial ideal sem testar ângulos manualmente.

O professor de matemática aplicada abre o conceito de autovalores e autovetores:
— A equação fundamental da mecânica e do processamento de sinais é $A v = \lambda v$ — ensina o professor. — Quando uma matriz de covariância opera sobre a maioria dos vetores, ela altera tanto o comprimento quanto a direção do vetor. Mas existem direções especiais no espaço vetorial — os autovetores $v$ — que, ao serem transformados pela matriz, sofrem apenas um escalonamento linear puro pelo fator escalar $\lambda$ (o autovalor), sem mudar de direção!

Ele demonstra o clássico método computacional da Iteração de Potência (Power Iteration):
1. Iniciar com um vetor aleatório $b_0$.
2. Multiplicar repetidamente pela matriz de covariância: $b_{k+1} = A b_k / \|A b_k\|_2$.
3. A cada iteração, as componentes ortogonais decaem proporcionalmente à razão de autovalores $(\lambda_2 / \lambda_1)^k$, e o vetor colapsa de forma matematicamente inevitável sobre o autovetor dominante associado ao maior autovalor $\lambda_1$.
4. O autovalor correspondente é extraído pelo quociente de Rayleigh: $\lambda = v^T A v$.

O pesquisador implementa a iteração de potência (`power_iteration`). Em menos de dez multiplicações matriciais, o vetor converge para o eixo maior da elipse de covariância. Essa direção revela o autovetor principal que fundamenta a Análise de Componentes Principais (PCA) e a decomposição espacial de CSP.
