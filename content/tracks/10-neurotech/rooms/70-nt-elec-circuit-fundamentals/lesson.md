# Lição — Ohm, Kirchhoff e Circuitos DC/AC no AFE

## 1. Do Resistor Ideal ao Modelo de Interface Eletrodo-Amplificador
1. **A Interface Resistiva em DC**:
   $$V_{\text{meas}} = V_{\text{source}} \cdot \frac{R_{\text{in}}}{R_{\text{skin}} + R_{\text{in}}}$$
   Com $R_{\text{in}} = 1\text{ G}\Omega$ e $R_{\text{skin}} = 10\text{ k}\Omega$, a perda é inferior a $0.001\%$.

2. **A Reatância Capacitiva em AC**:
   Cabos e trilhas de circuito impresso possuem capacitância parasita distribuída $C_{\text{cabo}}$. A reatância capacitiva:
   $$X_C = \frac{1}{2\pi f C_{\text{cabo}}}$$
   atua em paralelo com a entrada do amplificador.
   A amplitude AC medida torna-se:
   $$V_{\text{meas}} = V_{\text{source}} \cdot \frac{X_C}{\sqrt{R_{\text{skin}}^2 + X_C^2}}$$
   Em eletrodos secos com $R_{\text{skin}} \ge 1\text{ M}\Omega$, cabos com capacitância de $\sim 1\text{ nF}$ provocam atenuação superior a $15\text{--}20\%$ em frequências biológicas e de rede.

## 2. As Ferramentas de Código Desta Sala
- `measured_voltage(v_source, r_skin, r_in)`: Calcula o divisor resistivo clássico em DC.
- `audit_ac_cable_shunting(v_source_uv, r_skin_kohm, c_cable_pf, freq_hz, max_loss_pct)`: Calcula a impedância reativa AC do cabo e audita a porcentagem de perda de sinal, alertando se ultrapassar a margem permitida ($\le 5.0\%$).

Para destravar o lab, abra [TI ADS1299 datasheet (contexto AFE)](https://www.ti.com/lit/ds/symlink/ads1299.pdf) e leia a seção de características elétricas do ADS1299 (entrada, referência) para a lei de Ohm do lab usar a grandeza do AFE e não um resistor genérico.
