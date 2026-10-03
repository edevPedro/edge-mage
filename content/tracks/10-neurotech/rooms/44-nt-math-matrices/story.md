# História — A Geometria das Conexões Corticais

No centro de processamento de dados cerebrais, um pesquisador analisa uma matriz contendo 8 canais de biopotenciais gravados ao longo de 1000 amostras temporais ($X \in \mathbb{R}^{8 \times 1000}$). Para verificar a sincronização de fase e a integridade da gravação, ele precisa calcular a matriz de covariância espacial amostral $\Sigma = \frac{1}{T - 1} X X^T$.

O pesquisador executa um loop em Python aninhado de três níveis para calcular os produtos: o script demora vários segundos por época e consome ciclos excessivos de memória.

O arquiteto de algoritmos numéricos senta-se ao terminal e abre a formulação matricial:
— Em computação neural, matrizes não são meras listas de listas; são operadores de transformação linear espacial — ensina o arquiteto. — A multiplicação de matriz por vetor $y = A x$ mapeia uma configuração instantânea de potenciais de eletrodos em um novo espaço de sensores virtuais. A multiplicação de matrizes $X X^T$ integra instantaneamente a correlação cruzada de todos os pares de canais ao longo do tempo.

Ele demonstra a equivalência matricial: a diagonal principal da matriz de covariância contém a variância (energia) individual de cada eletrodo, enquanto os elementos fora da diagonal contêm a covariância mútua gerada pela condução de volume e pelo acoplamento neural.

O pesquisador implementa a rotina vetorizada de multiplicação matriz-vetor (`matvec`) e a estimativa de covariância amostral sem viés (`sample_covariance`). A matriz resultante é estritamente simétrica e positiva semi-definida, pavimentando o caminho para os algoritmos de autovalores de CSP e filtragem espacial ótima.
