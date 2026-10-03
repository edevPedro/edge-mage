# Conceito — Layout de PCB, EMC e Acoplamento por Área de Loop Magnético

Em placas de circuito impresso para biopotenciais, trilhas de sinal analógico de alta impedância convivem no mesmo substrato com microcontroladores rápidos, conversores DC-DC chaveados e rádios Wi-Fi/Bluetooth.

## 1. O Fundamento da Spec de Área de Loop (Lei de Faraday)

### A Tensão Induzida por Campo Magnético AC
Sempre que dois condutores (por exemplo, a trilha do eletrodo $C3$ e a trilha de retorno/referência) formam um laço fechado no espaço de área $A$, qualquer variação temporal no fluxo magnético ambiente $\Phi_B = \iint \vec{B} \cdot d\vec{A}$ induz uma força eletromotriz parasita:
$$V_{\text{ind}} = -\frac{d\Phi_B}{dt} = -A \times \frac{dB}{dt}$$

Para um campo senoidal de $60\text{ Hz}$ com amplitude $B(t) = B_{\text{peak}} \sin(2\pi f t)$:
$$\left(\frac{dB}{dt}\right)_{\max} = 2\pi f B_{\text{peak}}$$
$$V_{\text{ind, pico}} = A \times 2\pi f B_{\text{peak}}$$

Convertendo para microvolts ($\mu\text{V}$) com área em centímetros quadrados ($1\text{ cm}^2 = 10^{-4}\text{ m}^2$) e campo em microtesla ($1\ \mu\text{T} = 10^{-6}\text{ T}$):
$$V_{\text{ind, } \mu\text{V}} = (\text{Area}_{\text{cm}^2} \times 10^{-4}) \times (2\pi f \times B_{\mu\text{T}} \times 10^{-6}) \times 10^6 = \text{Area}_{\text{cm}^2} \times 10^{-4} \times 2\pi f \times B_{\mu\text{T}}$$

### A Catástrofe dos Cabos Não Trançados
- Campo ambiente comum próximo a transformadores de bancada: $B = 1.0\ \mu\text{T}$ a $60\text{ Hz}$.
- Se os fios do eletrodo e da referência forem conduzidos abertos pelo ambiente, formando um loop de $25\text{ cm} \times 20\text{ cm}$ ($A = 500\text{ cm}^2$):
  $$V_{\text{ind}} = 500 \times 10^{-4} \times 2\pi \times 60 \times 1.0 \approx 18.85\ \mu\text{V}$$
- O biopotencial cortical de interesse é de apenas $10\text{--}15\ \mu\text{V}$. A indução magnética no laço aberto é **maior que o próprio sinal biológico**!
- Ao trançar os cabos (par trançado / twisted pair) ou rotear as trilhas da PCB sobre um plano de terra contínuo com separação mínima ($A = 5\text{ cm}^2$):
  $$V_{\text{ind}} = 5 \times 10^{-4} \times 2\pi \times 60 \times 1.0 \approx 0.188\ \mu\text{V}$$
  O ruído cai para menos de $1\%$ do sinal, permitindo decodificação estável.

## 2. Unidades e Grandezas
- **Área de loop ($A$):** $\text{cm}^2$ ou $\text{m}^2$.
- **Densidade de fluxo magnético ($B$):** $\mu\text{T}$ ($1\ \mu\text{T} = 10^{-6}\text{ T}$).
- **Frequência ($f$):** $50\text{ Hz}$ ou $60\text{ Hz}$.
- **Tensão induzida ($V_{\text{ind}}$):** $\mu\text{V}$.

## 3. Modo de Falha na Engenharia
Separar os cabos dos eletrodos ou rotear trilhas analógicas sensíveis ao redor de planos de corte na PCB, criando grandes áreas de retorno de corrente. O campo magnético penetra o laço e gera tensões diferenciais que nenhum amplificador diferencial consegue rejeitar, pois a tensão é induzida diretamente em série com a entrada.

## 4. O que a Próxima Sala Assume
A sala seguinte ([`nt-elec-shield-power`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/74-nt-elec-shield-power/room.yaml)) assume que você compreende as leis de acoplamento magnético e elétrico para especificar blindagens Faraday ativas (guard shields) e filtragem de alimentação de ultra-baixo ruído.

## 5. Ponto de Destrave do Lab
Para diretrizes de layout físico em placas de sinais mistos analógico/digital para eletrofisiologia, consulte a seção de layout e roteamento do datasheet do [Texas Instruments ADS1299](https://www.ti.com/lit/ds/symlink/ads1299.pdf).
