# História — A Antena Involuntária na Placa de Circuito

Em um laboratório de prototipagem rápida de hardware biomédico, uma equipe de engenharia recebe a primeira revisão física de uma placa de circuito impresso (PCB) projetada para um módulo de EEG de 8 canais. O esquemático elétrico estava impecável: amplificadores de baixíssimo ruído, conversor ADS1299 e filtros analógicos corretos.

No entanto, assim que a placa é ligada na bancada, todos os canais registram interferência severa de 60 Hz e ruído de alta frequência induzido pelo microcontrolador digital:
— O esquemático elétrico não garante nada se o layout físico da PCB for mal projetado — sentencia a engenheira sênior de compatibilidade eletromagnética (EMC).

Ela coloca a placa sob a lupa esteriloscópica e aponta para as trilhas de cobre:
— Observem o traçado das trilhas de entrada dos eletrodos: vocês rotearam o sinal do eletrodo pela face superior da placa e o retorno de terra por uma trilha fina dando a volta pelo outro lado da placa, cercando uma área aberta de quase vinte centímetros quadrados! Pela Lei da Indução Eletromagnética de Faraday, qualquer laço fechado condutor que envolve uma área $A$ imersa em um campo magnético variável $B$ gera uma tensão induzida proporcional à área e à frequência:
$$V_{\text{induzido}} = 2\pi f B A$$
Um laço aberto de $20\text{ cm}^2$ no ambiente urbano atua como uma antena receptora perfeita de ruído magnético de transformadores e fiação, gerando microvolts de interferência diretamente na entrada do conversor!

Ela detalha as regras de ouro de layout para biopotenciais:
1. **Plano de Terra Contínuo:** Utilizar um stackup de pelo menos 4 camadas com um plano de terra sólido interno ininterrupto (Solid Ground Plane), minimizando a área de todos os loops de corrente de retorno.
2. **Separação Analógica/Digital:** Particionar a placa fisicamente em uma zona analógica pura (AFE) e uma zona digital rápida (MCU/SPI), impedindo que correntes de comutação digital atravessem os planos sensíveis de microvolts.

A equipe implementa a rotina de cálculo de tensão induzida em loop (`induced_voltage_loop`). O layout é corrigido com planos contínuos e trilhas diferenciais emparelhadas, eliminando a captação magnética espúria.
