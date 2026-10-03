# História — A Tempestade de Interrupções

A bancada de testes de firmware de uma touca de biopotenciais estava operando em alta carga. Uma placa microcontroladora ARM Cortex-M4 recebia dados de um front-end analógico ADS1299 configurado para 8 canais a 1000 amostras por segundo. A cada milissegundo, o pino de Data Ready (`/DRDY`) do conversor caía para nível lógico baixo, disparando uma linha de interrupção externa (EXTI).

O firmware havia sido escrito por um programador de aplicações: dentro da rotina de interrupção (ISR), o código executava um loop SPI para ler 27 bytes, convertia os inteiros de 24 bits para float e aplicava um filtro notch digital.

O engenheiro sênior de sistemas embarcados conectou uma sonda de osciloscópio no pino de debug e observou o sinal:

— "Sua CPU passa 85% do tempo presa dentro da rotina de interrupção. A pilha de rádio Bluetooth perdeu pacotes de conexão porque o handler da UART foi preempcionado indefinidamente. Cada amostra individual gera uma tempestade de contexto (*context switch*), salvando e restaurando registradores do núcleo dezenas de milhares de vezes por segundo."

O arquiteto de firmware puxou o manual do controlador de DMA (Direct Memory Access):

— "Em aquisição de biossinais, uma ISR nunca processa dados pesados. Nós configuramos o periférico SPI em modo escravo ou mestre com DMA em buffer circular (*ping-pong double buffer*). O hardware de DMA transfere os bytes do ADC diretamente para a memória SRAM sem intervenção do processador. O microcontrolador só é interrompido duas vezes por bloco: na metade da transferência (Half Transfer - HT) para processar o bloco 'ping', e no término do buffer (Transfer Complete - TC) para processar o bloco 'pong'. A CPU fica livre para o processamento de sinais e o jitter cai a zero."
