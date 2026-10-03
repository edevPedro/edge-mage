# História — O Vetor que Revelou o Movimento

Na bancada de análise de dados de um ensaio de Imagética Motora, dois pesquisadores tentavam treinar um classificador linear simples para distinguir entre a imaginação do movimento da mão direita e da mão esquerda. Os sinais de EEG dos eletrodos C3 e C4 haviam passado com sucesso pelos filtros biquads na faixa do ritmo mu, entre oito e doze hertz.

Contudo, ao plotar a potência pura $P$ calculada como a média dos quadrados das amostras em cada ensaio, o classificador linear apresentava convergência errática e uma taxa de acerto que oscilava aleatoriamente em torno de cinquenta por cento.

"A potência nos dois canais varia de zero vírgula um microvolt ao quadrado até dez mil microvolts ao quadrado toda vez que o voluntário pisca ou ajusta a postura," explicava o programador, mostrando um gráfico de dispersão com caudas pesadas e outliers extremos que puxavam a fronteira de decisão para longe da região útil.

A cientista de dados sênior sentou-se ao terminal e abriu o artigo clássico de Fabien Lotte sobre classificação de sinais de EEG.

"A potência espectral em biopotenciais segue uma distribuição assimétrica exponencial," explicou ela. "Um classificador linear baseado em dispersão gaussiana sofre horrores com distribuições de cauda longa. Você precisa aplicar a transformação logarítmica $\log_{10}(P)$ para comprimir a faixa dinâmica e simetrizar a distribuição."

Ela pegou os dados de um ensaio de mão direita: em C3, a potência era de dez microvolts ao quadrado; em C4, a potência era de cem microvolts ao quadrado.

"Calcule as coordenadas," pediu ela. O programador calculou: $\log_{10}(10) = 1.0$ e $\log_{10}(100) = 2.0$. No ensaio de mão esquerda, o inverso acontecia: $\log_{10}(100) = 2.0$ e $\log_{10}(10) = 1.0$.

Ao projetar os pares bidimensionais $[\log_{10}(P_{C3}), \log_{10}(P_{C4})]$, as duas classes separaram-se nitidamente em dois agrupamentos gaussianos compactos através da diagonal principal.

"A física da dessincronização neuronal agora virou geometria linear tratável," concluiu a pesquisadora. "Sem o logaritmo, os outliers governam seu modelo. Com o logaritmo, a fisiologia do córtex motor governa a fronteira."
