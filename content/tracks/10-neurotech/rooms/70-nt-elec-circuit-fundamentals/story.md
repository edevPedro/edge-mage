# História — O Cabo Fantasma

No teste de bancada de um sistema vestível de EEG de baixa densidade, a equipe enfrentava um comportamento desconcertante. Nos testes com simulador sintético e cabos curtos de dez centímetros, o sinal analógico de microvolts era digitalizado com fidelidade impecável pelo chip ADS1299.

Entretanto, quando o desenvolvedor conectava o chicote final de cabos de um metro e meio para alcançar a touca com eletrodos secos, a amplitude das ondas beta despencava pela metade e o ruído de rede elétrica de sessenta hertz subia exponencialmente.

"A resistência de entrada do chip é de um giga-ohm em corrente contínua," argumentava o desenvolvedor de software, com o multímetro na mão. "A pele do sujeito tem dois mega-ohms. O divisor de tensão em DC deveria transferir mais de noventa e nove por cento da voltagem. O problema só pode ser um bug no firmware do microcontrolador."

A engenheira eletrônica sênior pegou uma ponte LCR de precisão e mediu a capacitância entre o condutor central do cabo e a malha externa aterrada. O display indicou mil picofarads — um nanofarad.

"Seu multímetro mede em zero hertz," disse ela calmamente. "Mas o EEG é um sinal alternado. A sessenta hertz, a reatância capacitiva desse cabo de um nanofarad é de apenas dois vírgula seis mega-ohms. Essa reatância fica em paralelo com a entrada do chip, formando um divisor de tensão AC direto com a resistência de dois mega-ohms do seu eletrodo seco."

O desenvolvedor calculou a impedância equivalente e viu que a tensão medida no pino do conversor caía mais de vinte por cento, além de introduzir defasagem severa.

"Sem um buffer seguidor de tensão ativo colado diretamente na base do eletrodo," concluiu a engenheira, "a capacitância distribuída do cabo devora o microvolt antes mesmo de ele chegar à placa. Circuitos reais não obedecem apenas à lei de Ohm em DC; eles obedecem à impedância reativa em frequência."
