# História — O Limite Térmico da Prata

Na bancada de instrumentação de sinais de baixíssimo ruído, um engenheiro eletrônico projeta o pré-amplificador analógico para um novo eletroencefalógrafo portátil. Ele seleciona um amplificador operacional comercial comum e conecta um eletrodo com impedância de contato de $10\text{ k}\Omega$ sobre o escalpo. Na tela do analisador de espectro analógico, o traçado de ruído de fundo da entrada atinge $15\ \mu\text{V}_{\text{RMS}}$ — afogando completamente os $20\ \mu\text{V}$ de sinal de EEG útil.

O especialista em compatibilidade eletromagnética e front-ends biológicos senta-se ao lado da bancada com a equação de Nyquist e Johnson:
— Em eletrônica de biopotenciais, você luta contra a física fundamental da termodinâmica — adverte o especialista. — Em qualquer condutor em temperatura absoluta $T$, o movimento browniano dos elétrons livres gera o ruído térmico Johnson-Nyquist:
$$V_{\text{RMS}} = \sqrt{4 k_B T R \Delta f}$$
Onde $k_B$ é a constante de Boltzmann ($1.38 \times 10^{-23}\text{ J/K}$), $T$ é a temperatura em Kelvin, $R$ é a resistência em ohms e $\Delta f$ é a largura de banda.

Ele calcula o piso teórico inegociável:
— Para um eletrodo com $R = 10\text{ k}\Omega$ à temperatura corporal ($310\text{ K}$) em uma banda de $100\text{ Hz}$, o ruído térmico inevitável da física do eletrodo é de aproximadamente $0.13\ \mu\text{V}_{\text{RMS}}$. Se o seu amplificador está medindo 15 microvolts, o ruído não vem do eletrodo; vem do seu amplificador operacional inadequado!

O especialista analisa as especificações do circuito integrado:
— Você escolheu um amplificador com densidade de ruído de tensão referida à entrada de $e_n = 45\text{ nV}/\sqrt{\text{Hz}}$ e taxa de rejeição de modo comum (CMRR) de apenas 70 dB. Para biopotenciais de microvolts, você precisa de um amplificador de instrumentação biomédico com $e_n < 8\text{ nV}/\sqrt{\text{Hz}}$ e CMRR superior a 110 dB para cancelar a interferência de modo comum da rede de 60 Hz.

A equipe substitui o chip pelo front-end de instrumentação de precisão e implementa a função `johnson_noise_v_rms`. O piso de ruído do circuito cai para menos de um microvolt, permitindo a visualização cristalina dos ritmos sensoriomotores.
