# História — O Sinal que Inverteu de Repente

O protótipo de um fone de ouvido inteligente para monitoramento contínuo de fadiga em operadores industriais estava em fase de homologação. O circuito era alimentado por uma pequena bateria recarregável e utilizava um microcontrolador ARM Cortex-M0+ operando a 32 MHz.

O programador havia portado o algoritmo de detecção de ritmo alfa utilizando números `float` padrão. No primeiro teste de autonomia, a bateria esgotou-se em menos de três horas: como o Cortex-M0+ não possui unidade de ponto flutuante em hardware (FPU), cada multiplicação `float` exigia dezenas de instruções da biblioteca de software emulada, mantendo o núcleo em 100% de ocupação e impedindo a entrada nos modos de baixo consumo (*deep sleep*).

— "Vamos converter todos os filtros para aritmética inteira de ponto fixo Q15", anunciou o líder técnico. "Processamento em 16 bits de ciclo único com a biblioteca CMSIS-DSP."

O código foi reescrito. A ocupação da CPU despencou para 4%, e a bateria duraria mais de quarenta horas.

Porém, durante os testes, o operador tocou a haste do eletrodo para ajustar o fone. O artefato estático gerou um pico de tensão de 1,2 V na entrada. Instantaneamente, o indicador de potência espectral, que deveria indicar valor máximo, despencou para o menor valor possível negativo, acionando um falso alarme de crise neurológica.

O engenheiro de firmware abriu o osciloscópio do emulador e apontou a causa:

— "Vejam o registrador de 16 bits em complemento de dois: o valor escalonado tentou ultrapassar $+32767$. Em aritmética modular pura de microcontrolador, $32767 + 1$ vira $-32768$! Vocês tiveram um *overflow* de sinal sem saturação (*clamping*). O maior pico positivo de entrada virou o maior pico negativo instantaneamente, corrompendo toda a filtragem. Em ponto fixo de segurança crítica, a saturação aritmética estrita é mandatória: qualquer valor acima de $+1.0$ deve ser rigidamente cravado em $+32767$ e abaixo de $-1.0$ em $-32768$."
