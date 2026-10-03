# História — A Matriz Quase Singular

Na bancada de decodificação neural, uma desenvolvedora tentava calibrar o classificador para um voluntário que realizava imagética motora pela primeira vez. Por restrições de tempo e fadiga cognitiva, o protocolo de calibração havia gravado apenas oito ensaios de cada classe: oito ensaios imaginando o movimento da mão direita e oito da mão esquerda.

Os vetores de características bidimensionais $[\log_{10}(P_{C3}), \log_{10}(P_{C4})]$ foram computados com sucesso. No entanto, ao tentar ajustar o Discriminante Linear de Fisher tradicional, o script gerou um erro de álgebra linear: determinante nulo, matriz singular.

"A matriz de dispersão intra-classes tem dois canais que covariam quase perfeitamente devido à condução de volume do crânio," explicava o programador júnior, tentando forçar a inversão adicionando uma constante arbitrária minúscula. "Quando inverto a matriz, os pesos calculados para os eletrodos sobem para a casa de dez mil, e o classificador erra todos os ensaios de teste."

O engenheiro de aprendizado de máquina aproximou-se da tela e abriu o algoritmo de encolhimento de Ledoit-Wolf.

"Em conjuntos pequenos de calibração de EEG," disse o sênior, "a matriz amostral empírica subestima a variância das direções ortogonais e sofre com instabilidade extrema. Você não deve inventar números arbitrários; você aplica regularização de encolhimento, o *shrinkage*."

Ele pegou a matriz de covariância empírica $\Sigma$ e adicionou uma fração da matriz identidade proporcional ao traço médio: $\Sigma_{\text{reg}} = (1 - \gamma)\Sigma + \gamma (\text{tr}(\Sigma)/2) \mathbf{I}$, com $\gamma = 0.1$.

O determinante da matriz estabilizou-se instantaneamente longe de zero. Ao calcular o vetor de pesos ótimo $w = \Sigma_{\text{reg}}^{-1}(\mu_1 - \mu_0)$ e o bias bayesiano, os pesos assumiram magnitudes físicas coerentes, com polaridades opostas para C3 e C4.

No teste independente dos ensaios seguintes, o classificador acertou as intenções motoras com clareza matemática.

"Regularização de encolhimento não é um paliativo," concluiu o engenheiro. "É o fundamento que permite que modelos lineares funcionem com poucos ensaios em hardware de baixa potência sem colapsar."
