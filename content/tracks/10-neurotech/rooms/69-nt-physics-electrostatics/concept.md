# Conceito — Eletrostática Biofísica: Potencial, Gradiente e Campo Elétrico

Em eletrofisiologia quasistática, as variações de potenciais bioelétricos geram campos elétricos e fluxos de corrente iônica descritos pelas leis fundamentais de Maxwell e da eletrostática.

## 1. Relação entre Campo Elétrico e Potencial
O campo elétrico $\vec{E}$ (em Volts por metro, $\text{V/m}$) é o gradiente negativo do potencial eletrostático escalar $V$ (em Volts):
$$\vec{E} = -\nabla V = -\left( \frac{\partial V}{\partial x} \hat{i} + \frac{\partial V}{\partial y} \hat{j} + \frac{\partial V}{\partial z} \hat{k} \right)$$
Em uma dimensão ao longo da direção que conecta dois pontos com potenciais $V_1$ e $V_2$ separados por uma distância $d$:
$$E = -\frac{V_2 - V_1}{d} = \frac{V_1 - V_2}{d}$$

## 2. Unidades do Sistema Internacional (SI)
- **Potencial Elétrico ($V$):** Volt ($\text{V}$) ou Joule por Coulomb ($\text{J/C}$). Em biopotenciais: microvolts ($\mu\text{V}$).
- **Campo Elétrico ($E$):** Volts por metro ($\text{V/m}$) ou Newtons por Coulomb ($\text{N/C}$).
- **Capacitância ($C$):** Farad ($\text{F}$) ou Coulomb por Volt ($\text{C/V}$).

## 3. Densidade de Corrente e Lei de Ohm Microscópica
Nos tecidos biológicos condutores (líquor, substância cinzenta e couro cabeludo), a densidade de corrente volúmica $\vec{J}$ (em $\text{A/m}^2$) é diretamente proporcional ao campo elétrico através da condutividade $\sigma$ (em $\text{S/m}$):
$$\vec{J} = \sigma \vec{E} = -\sigma \nabla V$$
Essa relação fundamenta o problema direto de EEG (forward problem) para resolução da Equação de Poisson no encéfalo.

## 4. Modos de Falha na Prática de Engenharia
1. **Inversão de Sinal:** Omitir o sinal negativo do gradiente, concluindo erroneamente que correntes positivas fluem no sentido de potencial crescente sem fonte externa ativa.
2. **Incompatibilidade de Unidades:** Misturar milímetros com metros ao calcular o gradiente de campo, gerando erros de três ordens de magnitude ($10^3$).

## O Que a Próxima Sala Assume
A próxima sala (`nt-dipole-scalp`) — **Dipolo → potencial de escalpo** — aplica o campo elétrico na modelagem de dipolos equivalentes de corrente e calcula o decaimento com a distância até os eletrodos de escalpo.

## Artigos de Apoio e Leituras Recomendadas
- [Michel & Brunet — EEG source imaging (PMC6700197)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6700197/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
