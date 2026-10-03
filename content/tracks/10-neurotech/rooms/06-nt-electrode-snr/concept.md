# Conceito — Eletrodo, Impedância de Contato e a Spec de Impedância de Entrada

O biopotencial de escalpo é gerado por correntes iônicas e transmitido ao circuito eletrônico através de uma interface eletroquímica transdutora (eletrodos de $\text{Ag/AgCl}$ com gel condutor ou eletrodos secos).

```text
       Tecido / Pele              Interface Eletrodo           Front-End Analógico (AFE)
[ Fonte Neural V_bio ] ---> [ Impedância Z_electrode ] ----+----> [ R_in (Impedância de Entrada) ] ---> GND
                                                            |
                                                            +----> V_in (Tensão medida no amplificador)
```

## 1. O Fundamento da Spec Elétrica

### O Divisor de Tensão de Entrada
A impedância de contato do eletrodo ($Z_{\text{electrode}}$) e a impedância de entrada do amplificador ($R_{\text{in}}$) formam um divisor de tensão elétrico inevitável:
$$V_{\text{in}} = V_{\text{bio}} \times \frac{R_{\text{in}}}{Z_{\text{electrode}} + R_{\text{in}}}$$

A perda percentual de sinal por atenuação resistiva é:
$$\text{Erro}_{\text{atenuacao}}\ (\%) = \frac{Z_{\text{electrode}}}{Z_{\text{electrode}} + R_{\text{in}}} \times 100$$

### Por que a Spec do Amplificador Exige $R_{\text{in}} \ge 1\text{ G}\Omega$
- Em eletrodos de escalpo convencionais, a impedância típica varia entre $5\text{ k}\Omega$ e $50\text{ k}\Omega$ (eletrodos secos podem ultrapassar $100\text{ k}\Omega$).
- Se utilizarmos um amplificador operacional comum de uso geral com $R_{\text{in}} = 1\text{ M}\Omega$ ($10^6\ \Omega$):
  $$\text{Erro} = \frac{50\text{ k}\Omega}{50\text{ k}\Omega + 1000\text{ k}\Omega} \times 100 \approx 4.76\%$$
  Quase $5\%$ do microvoltagem cerebral é perdido antes mesmo de entrar no chip, além de degradar drasticamente o CMRR (Common Mode Rejection Ratio).
- Em AFEs dedicados a biopotenciais (como o Texas Instruments ADS1299), a spec impõe $R_{\text{in}} = 1\text{ G}\Omega$ ($10^9\ \Omega$):
  $$\text{Erro} = \frac{50\text{ k}\Omega}{50\text{ k}\Omega + 1\text{ G}\Omega} \times 100 \approx 0.005\%$$
  A atenuação é virtualmente nula, garantindo que a spec de erro fique bem abaixo do teto aceitável de $1.0\%$.

### Relação Sinal-Ruído (SNR) em Decibéis
$$\text{SNR}_{\text{dB}} = 10 \log_{10}\left( \frac{P_{\text{sinal}}}{P_{\text{ruido}}} \right) = 20 \log_{10}\left( \frac{V_{\text{RMS, sinal}}}{V_{\text{RMS, ruido}}} \right)$$
Um sinal típico de $10\ \mu\text{V}$ com ruído de fundo de $5\ \mu\text{V}$ possui apenas $6.02\text{ dB}$ de SNR. Qualquer atenuação por casamento de impedância ruim empurra o sinal para baixo do assoalho de ruído térmico Johnson-Nyquist ($v_n = \sqrt{4 k_B T R \Delta f}$).

## 2. Unidades e Grandezas
- **Impedância de eletrodo ($Z_{\text{electrode}}$):** $\text{k}\Omega$ ($5\text{--}50\text{ k}\Omega$ úmido; até $500\text{ k}\Omega$ seco).
- **Impedância de entrada do AFE ($R_{\text{in}}$):** $\text{G}\Omega$ ($10^9\ \Omega$ em FET-input / CMOS bio-AFEs).
- **Potência do sinal e ruído:** $\mu\text{V}^2$ ou linear.

## 3. Modo de Falha na Engenharia
Conectar eletrodos de alta impedância (especialmente eletrodos secos ou gel desidratado) em circuitos com impedância de entrada moderada ($< 100\text{ M}\Omega$). O divisor de tensão atenua o sinal, e pequenas variações na impedância do eletrodo modulam o ganho aparente do canal, gerando artefatos de movimento que imitam oscilações neurais.

## 4. O que a Próxima Sala Assume
A sala seguinte (`nt-ground-ref` (Terra, referência, 50/60 Hz)) assume que você entende como o desbalanceamento de impedância entre dois eletrodos ($\Delta Z = |Z_1 - Z_2|$) converte tensão de modo comum de $60\text{ Hz}$ em ruído diferencial.

## 5. Ponto de Destrave do Lab
Para checar os limites recomendados de impedância na preparação de sujeitos e a física da interface eletroquímica, consulte a documentação oficial da [OpenBCI EEG Setup](https://docs.openbci.com/GettingStarted/Biosensing-Setups/EEGSetup/) e o estudo clínico de impedâncias de escalpo por [Tallgren et al. (DOI 10.1016/j.clinph.2004.07.016)](https://doi.org/10.1016/j.clinph.2004.07.016).
