# História — O Offset que Cegou a Covariância

Em um protótipo experimental de decodificação motora de dois canais ($C3$ e $C4$), um engenheiro de software precisa gerar matrizes de covariância para classificar epochs de repouso contra epochs de movimento imaginado. O algoritmo deve estimar a matriz $\Sigma$ para cada janela de 1 segundo adquirida a 250 Hz.

O desenvolvedor escreve uma rotina direta que multiplica o buffer bruto por sua transposta, dividindo por $T-1$. Quando o gráfico da matriz de covariância é renderizado no dashboard de telemetria, todos os valores aparecem na casa dos milhares de microvolts ao quadrado, e as diagonais são praticamente idênticas em repouso e durante a tarefa motora.

O líder de instrumentação eletrofisiológica inspeciona o sinal e detecta um potencial de offset contínuo de eletrodo de $+45\ \mu\text{V}$ em $C3$ e $-30\ \mu\text{V}$ em $C4$, causado pela interface química gel-pele. Sem a subtração da média temporal antes da multiplicação matricial, o produto não calculava a covariância do sinal cerebral, mas sim o quadrado estático da tensão de polarização galvânica dos eletrodos.

O desenvolvedor precisa implementar uma rotina robusta: calcular a média temporal de cada canal, centrar os dados no zero e, somente então, computar a matriz de dispersão $\frac{1}{T-1}\tilde{X}\tilde{X}^T$, revelando a verdadeira dinâmica espectral do córtex motor.
