# Conceito — Processamento Digital de Sinais em Microcontroladores (Cortex-M e Q15)

Dispositivos de BCI vestíveis e implantáveis operam sob restrições estritas de consumo energético e processamento em hardware embarcado de 32 bits (famílias ARM Cortex-M0+, M4 e M7).

## 1. Arquitetura de Processamento Embarcado
O pipeline clássico de firmware para neurotecnologia divide-se em:
1. **Aquisição por DMA (Direct Memory Access):** O periférico SPI transfere as amostras do ADC diretamente para um buffer de RAM sem intervenção da CPU.
2. **ISR Ultracurta:** A interrupção apenas sinaliza a conclusão do bloco de amostras (Half-Transfer ou Transfer-Complete) e retorna imediatamente ($< 10\ \mu\text{s}$).
3. **Loop de Processamento (Foreground/Thread):** O filtro digital e a extração de características são processados fora da interrupção, prevenindo bloqueio do sistema.

## 2. Aritmética de Ponto Fixo Q15
Microcontroladores sem unidade de ponto flutuante (FPU) utilizam formatos fracionários de ponto fixo. No formato **Q15**:
- O inteiro com sinal de 16 bits (`int16_t`) representa valores no intervalo $[-1.0, 1.0 - 2^{-15}]$.
- O bit 15 é o sinal, e os 15 bits restantes representam a fração.
- A conversão de um número real $x \in [-1.0, 1.0]$ para Q15 é:
  $$x_{\text{Q15}} = \text{clamp}\left(\text{round}(x \times 32768), -32768, 32767\right)$$

### Operação de Multiplicação e Acumulação (MAC)
Ao multiplicar dois números Q15, o resultado é um número Q30 com dois bits de sinal. Para acumular sem perda de precisão e prevenir overflow catastrófico (onde um valor positivo ultrapassa 32767 e inverte para negativo), utiliza-se acumulador de 32 ou 64 bits com saturação estrita (`SSAT`).

## 3. Modos de Falha na Prática de Engenharia
1. **Overflow Sem Saturação:** Em aritmética modular padrão, $32000 + 2000 = -31536$. Em um sinal de biopotencial, isso inverte bruscamente a polaridade da onda, gerando uma espícula de alta frequência artificial que dispara falsos alarmes no decodificador.
2. **Excesso de Taps no Filtro:** Projetar um filtro FIR com 256 coeficientes em um MCU de 64 MHz amostrando a 1 kHz consome 256 ciclos de clock por canal a cada milissegundo, sobrecarregando o orçamento térmico e a bateria do dispositivo.

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-latency-budget`) formaliza o orçamento de latência ponta a ponta (aquisição $\to$ filtragem $\to$ decodificação $\to$ atuação) contra deadlines rígidos de controle em tempo real.

## 5. Ponto de Destrave do Lab
Para o estudo da biblioteca oficial de processamento de sinais em ARM Cortex-M, consulte a documentação do [CMSIS-DSP Filtering Functions](https://arm-software.github.io/CMSIS_5/DSP/html/group__groupFilters.html).
