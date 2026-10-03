# Conceito — Filtros Digitais Causais: Biquads IIR, Estabilidade e Atraso de Grupo

## 1. Fundamento Matemático: Projeto Causal via Transformada Bilinear
Em sistemas de decodificação neural em tempo real (Closed-Loop BCI), o sinal de EEG bruto que chega do conversor analógico-digital precisa ser filtrado para isolar as bandas oscilatórias de imagética motora ($\mu$: $8\text{--}12\text{ Hz}$, $\beta$: $16\text{--}24\text{ Hz}$) com causalidade estrita.

### A Transformada Bilinear com Pre-Warping
Para mapear um filtro analógico contínuo de Butterworth de 2ª ordem ($s$-plane) para o domínio discreto ($z$-plane) sem sofrer distorção não-linear de frequência (*frequency warping*), aplicamos a substituição:

$$s = \frac{2}{T_s} \frac{1 - z^{-1}}{1 + z^{-1}} = 2 f_s \frac{1 - z^{-1}}{1 + z^{-1}}$$

Com pré-deformação da frequência de corte analógica $\omega_c = 2\pi f_c$:
$$K = \tan\left(\frac{\pi f_c}{f_s}\right)$$

Para uma seção biquad de passa-baixas com fator de qualidade Butterworth $Q = 1/\sqrt{2}$:
$$b_0 = \frac{K^2}{1 + \sqrt{2}K + K^2}, \quad b_1 = 2 b_0, \quad b_2 = b_0$$
$$a_1 = \frac{2(K^2 - 1)}{1 + \sqrt{2}K + K^2}, \quad a_2 = \frac{1 - \sqrt{2}K + K^2}{1 + \sqrt{2}K + K^2}$$

A equação em diferenças causal executada a cada nova amostra $x[n]$ é:
$$y[n] = b_0 x[n] + b_1 x[n-1] + b_2 x[n-2] - a_1 y[n-1] - a_2 y[n-2]$$

A documentação canônica de projeto de filtros IIR e FIR encontra-se em [scipy.signal.firwin](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.firwin.html) e na arquitetura de biquads do [CMSIS-DSP da Arm](https://github.com/ARM-software/CMSIS-DSP).

### O Critério de Estabilidade de Jury para Biquads
Para que o filtro não exploda numericamente (estabilidade BIBO), os polos da equação característica $A(z) = z^2 + a_1 z + a_2 = 0$ devem residir estritamente dentro do círculo unitário complexo:
$$|z_{\text{polo}}| < 1.0$$
Pelo critério de estabilidade de Jury para 2º grau:
1. $|a_2| < 1$
2. $1 + a_1 + a_2 > 0 \implies a_1 > -(1 + a_2)$
3. $1 - a_1 + a_2 > 0 \implies a_1 < (1 + a_2)$

Se $a_2 \ge 1.0$ ou $|a_1| \ge 1 + a_2$, as raízes ultrapassam o círculo unitário e qualquer oscilação de microvolts dispara para infinito em poucos passos.

## 2. Modos de Falha Operacionais
1. **O Erro do `filtfilt` em Tempo Real**: Usar filtragem bidirecional de fase zero (`scipy.signal.filtfilt`) em loops de tempo real. O `filtfilt` processa o vetor inteiro para a frente e depois para trás, o que requer conhecer o futuro do sinal. Em tempo real, qualquer filtro DEVE ser causal de passagem única ($y[n]$ depende apenas de amostras passadas e presentes), aceitando um atraso de grupo (*group delay*) determinístico.
2. **Atraso de Grupo Excessivo em FIR**: Projetar um filtro FIR de fase linear com $N = 129$ taps em $f_s = 250\text{ Hz}$. O atraso de grupo puro de um FIR simétrico é:
   $$\tau_g = \frac{N - 1}{2 f_s} = \frac{128}{500} = 0.256\text{ s} = 256\text{ ms}$$
   Um atraso de $256\text{ ms}$ consome sozinho todo o orçamento de latência do closed-loop sensorial ($<100\text{ ms}$), tornando o neurofeedback inútil para o córtex motor. Biquads IIR de 2ª ordem entregam seletividade espectral equivalente com atraso inferior a $15\text{ ms}$.

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-features-bandpower`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/13-nt-features-bandpower/room.yaml)) assume que as séries temporais dos canais sensório-motores C3 e C4 foram filtradas causalmente na banda de interesse, prontas para que sua variância em janelas móveis seja convertida em vetores de potência logarítmica (log-bandpower).
