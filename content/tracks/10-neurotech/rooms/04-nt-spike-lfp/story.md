# História — O Mito do Spike no Escalpo

No laboratório de instrumentação eletrofisiológica, um novo engenheiro de software debruçava-se sobre a bancada com um osciloscópio digital e um conversor ADS1299 configurado para amostragem em 16 kSPS. Ele havia soldado um pré-amplificador de baixíssimo ruído e colocado eletrodos secos sobre o escalpo em C3 e C4.

"Se aumentarmos a taxa de amostragem e aplicarmos um filtro passa-altas em 300 Hz," explicava ele com entusiasmo à equipe, "vamos conseguir isolar os potenciais de ação individuais das células piramidais do córtex motor e fazer spike sorting em tempo real no microcontrolador."

A pesquisadora sênior aproximou-se da bancada, pegou uma caneta e desenhou duas esferas concêntricas no quadro branco.

"Um potencial de ação gera uma corrente transmembrana na casa de picoamperes," disse ela calmamente. "A vinte micrômetros do soma celular, um microeletrodo de tungstênio afiado enxerga cerca de cem microvolts. Mas o seu eletrodo de escalpo está a dois centímetros de distância — vinte mil micrômetros. Calcule a atenuação geométrica quadrática do meio condutor."

O engenheiro pegou a calculadora: a relação $(20 / 20.000)^2$ resultou em $10^{-6}$. Os cem microvolts do spike foram reduzidos a um décimo de nanovolt — cem picovolts. Enquanto isso, o ruído térmico Johnson do próprio eletrodo de prata ultrapassava um microvolt.

"Você precisaria de um piso de ruído mil vezes menor que as leis da termodinâmica permitem para enxergar esse spike isolado," concluiu ela. "O que o escalpo enxerga não são cliques individuais de neurônios. É a sinfonia macroscópica de milhões de potenciais pós-sinápticos dendríticos disparando em sincronia: o Potencial de Campo Local. Se quiser spikes, você precisa de um implante de silício penetrante. Se estiver no escalpo, seu objeto de trabalho são os ritmos de LFP."
