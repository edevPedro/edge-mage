# Lição — Semicondutores, Proteção ESD e Polarização

## 1. Diodos de Proteção e Correntes de Fuga
1. **O Mecanismo de Clamping ESD**:
   Para limitar sobretensões destrutivas induzidas no corpo humano ou nos cabos de eletrodo, diodos conectam a entrada analógica a $V_{DD}$ e $V_{SS}$:
   $$V_{\text{clamp, max}} = V_{DD} + V_{\text{diodo}}$$
   $$V_{\text{clamp, min}} = V_{SS} - V_{\text{diodo}}$$

2. **A Corrente de Fuga Reversa ($I_{\text{leak}}$)**:
   Diodos em bloqueio conduzem uma corrente reversa finita $I_{\text{leak}}$.
   Ao fluir através da resistência de contato da pele $R_{\text{pele}}$, essa corrente gera um offset DC espúrio:
   $$V_{\text{offset}} = I_{\text{leak}} \cdot R_{\text{pele}}$$
   Em circuitos integrados de instrumentação dedicados (TI ADS1299), $I_{\text{leak}} \le 200\text{ pA}$, mantendo o offset DC abaixo de $5\ \mu\text{V}$. Diodos discretos convencionais ($I_{\text{leak}} \ge 20\text{ nA}$) produzem offsets na casa de milivolts, saturando os estágios de ganho subsequentes.

## 2. As Funções de Laboratório Desta Sala
- `esd_clamp(v_in, v_pos, v_neg, v_diode)`: Modela a saturação não-linear dos diodos de proteção contra sobretensões transitórias.
- `audit_diode_leakage_offset(i_leak_na, r_skin_kohm, max_offset_uv)`: Calcula numericamente a tensão contínua induzida pela corrente de fuga através da impedância de pele, auditando se o offset gerado permanece dentro do orçamento de segurança ($\le 500\ \mu\text{V}$).

Para destravar o lab, abra [TI ADS1299 datasheet](https://www.ti.com/lit/ds/symlink/ads1299.pdf) e leia o que o datasheet do ADS1299 fixa sobre proteção de entrada e fuga, para a tensão de offset do diodo não passar do teto da auditoria.
