# Conceito — Conversão A/D e a Spec de Resolução LSB contra 10 µV

O sinal bioelétrico de EEG no escalpo humano é uma grandeza analógica microscópica: flutua tipicamente entre $5\ \mu\text{V}$ e $50\ \mu\text{V}$ pico a pico. O conversor analógico-digital (ADC) precisa transformar essa voltagem contínua em números inteiros sem que o sinal desapareça no erro de quantização.

## 1. O Fundamento da Spec do ADC

### Resolução de Menor Bit Significativo (LSB)
Para um conversor diferencial bipolar com faixa simétrica $[-V_{\text{ref}}/\text{PGA}, +V_{\text{ref}}/\text{PGA}]$ codificado em $N$ bits com amplificador de ganho programável (PGA):
$$\text{LSB}_{\mu\text{V}} = \frac{V_{\text{ref}}}{2^{N-1} \times \text{PGA}} \times 10^6$$

### O Confronto Crítico: Microcontrolador Comum vs. AFE de 24 Bits
1. **O ADC de 12 bits de um microcontrolador padrão (ex: STM32 ou ESP32):**
   - $V_{\text{ref}} = 3.3\text{ V}$, $N = 12$ bits, $\text{PGA} = 1$:
     $$\text{LSB} = \frac{3.3}{2^{11} \times 1} \times 10^6 = \frac{3.3}{2048} \times 10^6 \approx 1611.3\ \mu\text{V} \approx 1.61\text{ mV}$$
   - Um sinal cortical de $10\ \mu\text{V}$ representa apenas $\frac{10}{1611.3} \approx 0.006$ LSB.
   - O sinal biológico inteiro fica dentro do chão de quantização de um único bit. O registrador digital lê apenas ruído constante ou zeros.
2. **O ADC Delta-Sigma de 24 bits de biopotenciais (TI ADS1299):**
   - $V_{\text{ref}} = 2.4\text{ V}$, $N = 24$ bits, $\text{PGA} = 24$:
     $$\text{LSB} = \frac{2.4}{2^{23} \times 24} \times 10^6 = \frac{2.4}{8.388.608 \times 24} \times 10^6 \approx 0.0119\ \mu\text{V}$$
   - Um sinal de $10\ \mu\text{V}$ é amostrado com mais de 840 degraus de quantização discretos, garantindo resolução sub-microvolt e fidelidade total na reconstrução da forma de onda.

## 2. Unidades e Grandezas
- **Tensão de Referência ($V_{\text{ref}}$):** Volts ($2.4\text{ V}$ ou $3.3\text{ V}$).
- **Resolução ($N$):** Bits inteiros ($12, 16, 24$).
- **LSB:** $\mu\text{V}$ por nível digital.
- **Sinal de interesse:** $10\ \mu\text{V}$. Spec mínima exige $\text{LSB} \le 2.0\ \mu\text{V}$ (idealmente $\le 0.1\ \mu\text{V}$).

## 3. Modo de Falha na Engenharia
Alimentar a entrada de um ADC de 10 ou 12 bits diretamente com o sinal do eletrodo sem um pré-amplificador analógico de alto ganho ($G \ge 1000$). O firmware compila, o código lê valores inteiros do registrador, mas o desenvolvedor está amostrando apenas ruído de quantização e offset térmico.

## O Que a Próxima Sala Assume
A próxima sala (`nt-elec-antialias`) — **Elétrica — Nyquist e anti-alias** — projeta filtros analógicos passa-baixa anti-aliasing para garantir que componentes acima de Nyquist não dobrem sobre os ritmos cerebrais.

## Artigos de Apoio e Leituras Recomendadas
- [OpenBCI Cyton](https://docs.openbci.com/GettingStarted/Boards/CytonGS/) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Texas Instruments — ADS1299 datasheet (EEG AFE reference)](https://www.ti.com/lit/ds/symlink/ads1299.pdf) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
