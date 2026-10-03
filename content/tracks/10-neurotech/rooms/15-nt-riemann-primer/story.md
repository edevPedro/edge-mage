# História — A Curvatura do Espaço de Covariâncias

Em um seminário de processamento estatístico de sinais, um doutorando em engenharia biomédica apresenta sua tentativa de interpolar e calcular distâncias euclidianas convencionais entre matrizes de covariância multicanal de EEG. Para construir um protótipo de média móvel temporal, ele somou linearmente duas matrizes de covariância $\Sigma_1$ e $\Sigma_2$ e dividiu por dois: $\bar{\Sigma} = (\Sigma_1 + \Sigma_2) / 2$.

O professor de geometria de dados interrompe a apresentação e projeta no telão os autovalores da matriz resultante:
— Observe o determinante de $\bar{\Sigma}$ — aponta o professor. — Ao utilizar a média euclidiana plana, o determinante da matriz resultante é significativamente maior do que o determinante de ambas as matrizes de entrada. Esse efeito perverso é conhecido na literatura como o "inchaço" euclidiano (swelling effect). Matrizes de covariância de sinais não vivem em um espaço vetorial plano $\mathbb{R}^{C \times C}$; elas residem no cone não-linear de matrizes Simétricas Positivas Definidas (SPD).

O professor desenha no quadro o cone SPD e explica que a soma euclidiana ignora a geometria intrínseca das potências e correlações biológicas:
— Se dois eletrodos estão fortemente correlacionados, a matriz de covariância tem autovalores próximos de zero em certas direções ortogonais. A distância euclidiana direta $\|\Sigma_1 - \Sigma_2\|_F$ pode considerar próximas duas matrizes que possuem orientações fisiológicas opostas, e pode até extrapolar para matrizes com autovalores negativos (não-físicos).

Ele introduz então a Métrica Riemanniana Afim-Invariante (AIRM). Em vez de medir distâncias em linha reta através do vazio não-positivo, a métrica de Rao e Fisher mede o comprimento da curva geodésica mais curta que permanece estritamente dentro do cone de matrizes SPD:
$$\delta_R(P_1, P_2) = \|\log(P_1^{-1/2} P_2 P_1^{-1/2})\|_F$$

Para o caso pedagógico de matrizes diagonais de variância, a distância simplifica-se elegantemente para a raiz da soma dos quadrados das diferenças dos logaritmos das variâncias: $\sqrt{\sum (\ln(a_i / b_i))^2}$.

O estudante implementa a métrica geodésica. As distâncias tornam-se invariantes a transformações lineares invertíveis dos canais, o inchaço desaparece, e os classificadores baseados em centroides Riemannianos (MDM) superam o LDA clássico sem necessidade de ajustes manuais de filtros espaciais.
