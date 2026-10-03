# História — O Laço Invisível de Faraday

Na bancada de prototipagem rápida de uma startup de dispositivos vestíveis, um desenvolvedor monta um protótipo de BCI em uma matriz de contato (protoboard). Dois fios longos de jumper — um vindo do eletrodo de escalpo em $C4$ e outro da referência no mastoide — são conectados à entrada do chip amplificador. Os fios correm soltos sobre a mesa, formando um laço aberto de aproximadamente 500 centímetros quadrados.

Mesmo alimentando o circuito por uma bateria isolada de lítio e ativando todos os filtros digitais disponíveis, o sinal registrado exibe uma onda senoidal de $19\ \mu\text{V}$ em 60 Hz. A equipe não consegue entender de onde vem o ruído, já que o sistema está galvanicamente desconectado da rede elétrica predial.

O engenheiro de compatibilidade eletromagnética (EMC) aproxima uma sonda de campo magnético e demonstra o princípio de indução de Faraday: a corrente que alimenta o monitor e a luminária da bancada gera um campo magnético oscilante de $1\ \mu\text{T}$ no ar. Esse fluxo corta perpendicularmente o laço formado pelos fios abertos dos eletrodos, induzindo quase $19\ \mu\text{V}$ de força eletromotriz em série direta com a entrada do amplificador.

O desenvolvedor aprende a regra de ouro de EMC para biopotenciais: torcer os fios em par trançado e desenhar a PCB com plano de terra contínuo reduz a área do laço para menos de 5 centímetros quadrados, derrubando a indução magnética para frações inaudíveis de microvolt.
