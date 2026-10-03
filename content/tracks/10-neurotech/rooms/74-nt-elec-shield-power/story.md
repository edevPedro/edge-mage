# História — O Ritmo que Veio da Fonte

Na bancada de testes de compatibilidade eletromagnética, um time de firmware e hardware comemorava o primeiro sinal digitalizado de um capacete de EEG sem fio alimentado por bateria de íons de lítio.

O engenheiro de software exibia a tela do computador onde uma oscilação sinusoidal rítmica e quase perfeita preenchia os canais parietais e occipitais.

"Conseguimos sincronização de fase espetacular," celebrava o desenvolvedor. "O sujeito mal começou o protocolo de olhos fechados e já estamos observando uma onda de amplitude enorme, na casa de cem microvolts."

A engenheira de sistemas de potência do laboratório olhou para o gráfico, franziu o cenho e perguntou qual era a frequência exata da oscilação.

"Cerca de noventa e oito quilohertz, mas o conversor analógico-digital com filtro sinc decima o sinal para duzentos e cinquenta hertz e faz aliasing dobrando essa energia exatamente na faixa de dez hertz," respondeu ela, pegando uma ponta de prova ativa do osciloscópio.

Ela encostou a ponta de prova diretamente no pino de alimentação analógica AVDD do chip ADS1299. No osciloscópio, o trilho de três vírgula três volts pulsava com trinta milivolts de ripple de comutação gerados pelo conversor buck DC-DC da bateria.

"O regulador chaveado comuta a cerca de cem quilohertz para economizar energia," explicou a engenheira. "Nessa frequência, a rejeição de fonte de alimentação do chip cai para cinquenta decibéis — um fator de atenuação de trezentas e dezesseis vezes. Trinta milivolts divididos por trezentos e dezesseis resultam em noventa e cinco microvolts injetados diretamente na entrada analógica."

O desenvolvedor de software empalideceu. O sinal que ele achava ser ritmo alfa era simplesmente a fonte de alimentação vomitando ripple no conversor.

"Seu cérebro biológico gera dez microvolts," concluiu a especialista. "A sua fonte está injetando noventa e cinco. O que você decodificou não foi imagética motora nem relaxamento; foi o ciclo de carga e descarga do indutor da bateria. Sem um regulador linear LDO de altíssimo PSRR e planos de terra separados, você estará sempre digitalizando a sua própria fonte."
