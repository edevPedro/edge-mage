# História — O Ciclo de Clock que Não Volta

No laboratório de sistemas embarcados, uma equipe de engenharia desenvolve um dispositivo vestível de monitoramento neural em tempo real. O hardware é baseado em um microcontrolador ARM Cortex-M4 operando a 64 MHz, sem sistema operacional, com apenas 64 KB de memória SRAM. A placa deve receber amostras do conversor ADS1299 via interrupção SPI a 250 Hz e aplicar um filtro digital FIR para filtrar a banda sensoriomotora antes de transmitir os pacotes via rádio Bluetooth Low Energy.

Durante os testes de osciloscópio, o sinal transmitido apresenta falhas periódicas: pacotes corrompidos e jitter violento no intervalo entre amostras.

O arquiteto de firmware conecta uma sonda de analisador lógico aos pinos de debug do microcontrolador:
— Observem o pino de teste que colocamos no início e no fim da Rotina de Serviço de Interrupção (ISR) — explica o arquiteto. — A cada 4 milissegundos, a interrupção do conversor dispara. A ISR foi escrita em C utilizando aritmética de ponto flutuante de precisão dupla (`double`) de 64 bits para calcular o filtro FIR de 64 coeficientes:
```c
// Erro grave de firmware: float de 64 bits em interrupção rápida
for (int i = 0; i < 64; i++) {
    acc += (double)taps[i] * (double)history[i];
}
```

O microcontrolador Cortex-M4 possui apenas uma FPU de precisão simples (32 bits). Ao utilizar `double`, o compilador insere rotinas de emulação de software que consomem milhares de ciclos de clock por amostra. A ISR estava levando 3.8 milissegundos para concluir, consumindo 95% do tempo da CPU e bloqueando outras interrupções críticas do stack de comunicação sem fio.

— Em firmware de baixa potência para neurotecnologia, a ISR de aquisição deve ser ultrarrápida: ler o registrador via DMA e sair em menos de vinte microssegundos — determina o arquiteto. — O processamento de filtragem deve ser executado no loop principal usando aritmética de ponto fixo Q15 com instruções SIMD dedicadas de multiplicação e acumulação com saturação (`SMLABB` / `SSAT`).

A equipe reescreve o pipeline: o filtro passa a utilizar aritmética de ponto fixo Q15, com coeficientes escalados por $2^{15} = 32768$ e acumulador protegido contra overflow. O tempo de cálculo por amostra despenca de 3800 microssegundos para menos de 4 microssegundos, liberando o microcontrolador para operar com folga determinística.
