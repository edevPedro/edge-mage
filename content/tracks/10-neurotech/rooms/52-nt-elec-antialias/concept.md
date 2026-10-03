# Conceito — Nyquist, Teorema de Shannon e Filtro Anti-Aliasing Analógico

A discretização temporal de qualquer biopotencial contínuo deve respeitar o Teorema de Amostragem de Nyquist-Shannon: a frequência de amostragem ($f_s$) deve ser estritamente maior que o dobro da frequência máxima presente no sinal ($f_s > 2 f_{\max}$).

## 1. O Fundamento da Spec do Filtro Anti-Aliasing (AAF)

### A Irreversibilidade do Aliasing Digital
Se um sinal analógico contiver componentes de alta frequência $f > f_s/2$ (ruído eletromiográfico muscular de $150\text{ Hz}$, ruído de comutação de reguladores DC-DC chaveados de $200\text{ Hz}$, etc.), essas frequências sofrem **aliasing**: elas rebatem no espectro espelhado em torno de $f_N = f_s/2$, reaparecendo exatamente dentro da faixa fisiológica do EEG ($0.5\text{--}40\text{ Hz}$).
$$f_{\text{aparente}} = |f_{\text{sinal}} - k \cdot f_s|$$

Uma vez que o sinal entra no ADC sem anti-aliasing analógico prévio, o ruído de $200\text{ Hz}$ vira um sinal espúrio de $50\text{ Hz}$ idêntico a uma oscilação neural. **Nenhum filtro digital em software (FIR ou IIR) consegue remover esse ruído**, pois ele já foi indistinguivelmente dobrado no domínio digital.

### A Spec de Corte e Atenuação em Nyquist
Um filtro anti-alias analógico passa-baixas (típico Butterworth de ordem $n$) deve ser inserido **obrigatoriamente antes do ADC**:
$$|H(f)|^2 = \frac{1}{1 + \left(\frac{f}{f_c}\right)^{2n}}$$

A atenuação na frequência de Nyquist ($f_N = f_s/2$) em decibéis é:
$$\text{Atenuação}_{\text{dB}} = 10 \log_{10}\left( 1 + \left(\frac{f_N}{f_c}\right)^{2n} \right)$$

- Se $f_s = 250\text{ Hz}$ ($f_N = 125\text{ Hz}$) e o projetista escolhe $f_c = 110\text{ Hz}$ com filtro de 2ª ordem:
  $$\text{Atenuação} = 10 \log_{10}\left(1 + (125/110)^4\right) = 10 \log_{10}(1 + 1.66) \approx 4.25\text{ dB}$$
  O ruído de alta frequência passa quase intacto pelo filtro! A spec falha redondamente.
- Se o projetista dimensiona $f_c = 40\text{ Hz}$ (preservando toda a banda mu e beta) com $n = 2$:
  $$\text{Atenuação} = 10 \log_{10}\left(1 + (125/40)^4\right) = 10 \log_{10}(1 + 95.37) \approx 19.84\text{ dB}$$
  O filtro atenua em dez vezes a potência do ruído na borda de Nyquist, garantindo que componentes espúrios fiquem suprimidos.

## 2. Unidades e Grandezas
- **Frequência de amostragem ($f_s$):** Hertz ($\text{Hz}$, tipicamente $250\text{--}1000\text{ Hz}$).
- **Frequência de Nyquist ($f_N$):** $f_s / 2$ ($\text{Hz}$).
- **Frequência de corte ($f_c$):** $\text{Hz}$ (ponto de $-3\text{ dB}$).
- **Atenuação:** Decibéis ($\text{dB}$).

## 3. Modo de Falha na Engenharia
Supor que um conversor ADC amostrando a 250 Hz pode dispensar componentes analógicos externos porque o firmware implementará "filtros digitais avançados no microcontrolador". Ruído de alta frequência amostrado vira ruído de baixa frequência irreversível.

## 4. O que a Próxima Sala Assume
A sala seguinte ([`nt-elec-pcb-emc`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/73-nt-elec-pcb-emc/room.yaml)) assume que você compreende as frequências de corte do AAF para posicionar os componentes passivos próximos aos pinos de entrada no layout da PCB sem criar antenas de ruído.

## 5. Ponto de Destrave do Lab
Para entender a matemática da dizimação e reamostragem em tempo discreto, consulte a documentação oficial do [SciPy signal decimate](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.decimate.html).
