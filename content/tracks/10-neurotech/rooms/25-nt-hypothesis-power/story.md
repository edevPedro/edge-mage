# História — A Armadilha das Comparações Múltiplas

Em uma sessão de análise de biomarcadores em um laboratório de neurociência computacional, um estudante apresenta um gráfico radiante: ele analisou 64 canais de EEG particionados em 8 bandas de frequência diferentes (totalizando 512 combinações espectro-espaciais) procurando diferenças estatísticas entre a condição de repouso e a imagética de movimento.

— Encontrei 25 canais e bandas com $p < 0.05$! — comemora o estudante. — Temos mais de vinte biomarcadores neurais significativos!

O coordenador do grupo de pesquisa puxa uma cadeira e abre uma planilha em branco:
— Se você realizar 512 testes de hipóteses estatísticas independentes utilizando um limiar de significância de $\alpha = 0.05$, quantas vezes você espera encontrar $p < 0.05$ puramente por ruído aleatório em dados onde não existe efeito algum?

O estudante calcula: $512 \times 0.05 = 25.6$.

— Exatamente vinte e cinco — diz o professor calmamente. — Seus 25 "biomarcadores descobertos" são rigorosamente a quantidade esperada de falsos positivos que a lei das probabilidades garante que aparecerão ao testar centenas de hipóteses sem correção. Esse fenômeno é conhecido como a armadilha do p-hacking ou "pescaria de hipóteses" (data dredging).

O professor introduz as duas salvaguardas metodológicas essenciais da ciência séria:
1. **Controle da Taxa de Falso Positivo (FWER / FDR):** Aplicar a correção conservadora de Bonferroni, ajustando o limiar de decisão para $\alpha' = \alpha / M = 0.05 / 512 \approx 0.000097$, ou o controle da taxa de falsa descoberta de Benjamini-Hochberg.
2. **Tamanho de Efeito e Poder Estatístico:** Calcular o $d$ de Cohen ($d = (\mu_1 - \mu_2) / \sigma_{\text{pooled}}$) para verificar se a diferença encontrada tem magnitude fisiológica relevante ($d > 0.5$) ou se é apenas uma oscilação microscópica artificial.

O estudante recalcula sua análise aplicando a correção de Bonferroni. Das 25 supostas descobertas, apenas duas resistem ao crivo estatístico: exatamente os eletrodos $C3$ e $C4$ na banda $\mu$. A ilusão evapora, dando lugar a uma descoberta científica sólida e replicável.
