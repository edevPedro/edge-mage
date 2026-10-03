# Lição — Eletrostática, Quase-Estática e Potencial no Meio Condutor

## 1. O Regime Quase-Estático em Biologia
Nas frequências do eletroencefalograma ($0.1\text{--}100\text{ Hz}$), os efeitos indutivos e as correntes de deslocamento de Maxwell são desprezíveis em comparação com a condução ôhmica. O campo elétrico é conservativo e deriva de um potencial escalar:
$$\mathbf{E} = -\nabla V$$
A equação que governa o potencial no meio condutor com fontes de corrente $I_v$ é a equação de Poisson para condução volumétrica:
$$\nabla \cdot (\sigma \nabla V) = -I_v$$

## 2. A Equação do Dipolo de Corrente
Para um dipolo pontual de corrente com momento dipolar $p = I \cdot d$ em um meio homogêneo e infinito com condutividade $\sigma$:
$$V(r, \theta) = \frac{p \cos(\theta)}{4\pi \sigma r^2}$$
- **$p$**: Momento dipolar elétrico (em $\text{A}\cdot\text{m}$).
- **$\sigma$**: Condutividade volumétrica do meio (em $\text{S/m}$, tipicamente $\sim 0.33\text{ S/m}$ para tecido cerebral e couro cabeludo).
- **$r$**: Distância do dipolo ao ponto de medição (em metros).
- **$\theta$**: Ângulo entre o eixo do dipolo e a linha que conecta o dipolo ao eletrodo. Quando $\theta = 0$, o potencial é máximo; quando $\theta = \pi/2$, o potencial se anula por cancelamento simétrico.

## 3. As Funções de Laboratório Desta Sala
- `electric_field(q, r, k)`: Calcula a magnitude do campo elétrico eletrostático no vácuo segundo a lei de Coulomb.
- `audit_quasistatic_volume_potential(p_current_dipole_am, distance_m, sigma_s_per_m, theta_rad)`: Calcula o potencial biológico em condutor de volume em $\mu\text{V}$, avaliando se o sinal atinge magnitude mensurável no escalpo ($\ge 1.0\ \mu\text{V}$) e auditando a orientação espacial (radial vs tangencial).

Para destravar o lab, abra [Michel & Brunet — EEG source imaging (PMC6700197)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6700197/) e leia a aproximação de dipolo no review de Michel e Brunet para o potencial cair com a geometria e não com um ganho livre.
