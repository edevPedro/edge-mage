# História — Do Domínio do Tempo à Energia do Sinal

No laboratório de machine learning neural, um programador tenta treinar um classificador linear alimentando diretamente os valores instantâneos de tensão em microvolts amostrados no tempo dos eletrodos $C3$ e $C4$. A cada ensaio, a série temporal oscila rapidamente em torno de zero, e os pesos do classificador oscilam sem convergir: ora um ponto tem valor positivo, ora negativo, dependendo da fase instantânea da onda no momento do corte do epoch.

O pesquisador de neurocomputação senta-se ao lado do programador e abre o gráfico de dispersão das amostras temporais brutas:

— Se você alimentar valores de amplitude instantânea $x[n]$, o classificador tentará ajustar hiperplanos baseando-se na fase da oscilação — explica o pesquisador. — Mas o cérebro humano não modula a fase absoluta de cada ciclo da onda senoidal de $10\text{ Hz}$; ele modula a *energia média* da população neuronal disparando em sincronia. O que define a intenção motora é a variância da oscilação ao longo de uma janela temporal de observação.

O pesquisador orienta o desenvolvedor a calcular a potência média de banda: elevar cada amostra filtrada ao quadrado, computar a média na janela de tempo e aplicar a transformação logarítmica:
$$P = \frac{1}{N} \sum_{n=0}^{N-1} x[n]^2, \quad f = \log_{10}(P)$$

Quando os dois novos valores escalares $[f_{C3}, f_{C4}]$ são plotados no plano cartesiano bidimensional, a nuvem de pontos correspondente à imagética da mão direita separa-se com limpidez da classe da mão esquerda:
- Na mão direita, $C3$ apresenta queda acentuada de energia (ERD contralateral), deslocando os pontos para a esquerda do gráfico.
- Na mão esquerda, $C4$ apresenta queda de energia, deslocando os pontos para a parte inferior do gráfico.

— A potência de banda transforma uma forma de onda senoidal de média zero e fase caótica em um ponto estável em um espaço de características estritamente separável — conclui o pesquisador.
