# Conceito — Eletrostática, Quase-Estática e Potencial no Meio Condutor

## 1. Fundamento Físico: Do Vácuo ao Meio Condutor Biológico
Na física clássica do vácuo, cargas elétricas pontuais $q$ (em Coulombs) criam um campo elétrico $\mathbf{E}$ e potencial eletrostático $V = \frac{q}{4\pi \epsilon_0 r}$.

Entretanto, o tecido biológico (cérebro, líquor, crânio e couro cabeludo) **não** é o vácuo nem um dielétrico perfeito: é um condutor de volume contendo água e eletrólitos dissolvidos ($Na^+$, $K^+$, $Cl^-$) com condutividade volumétrica média $\sigma \approx 0.33\text{ S/m}$.

### O Regime Quase-Estático de Maxwell
Nas frequências biológicas de interesse em EEG ($f < 1000\text{ Hz}$):
1. O comprimento de onda eletromagnético $\lambda = c / f$ excede $300\text{ km}$, incomparavelmente maior do que as dimensões da cabeça humana ($\sim 0.2\text{ m}$).
2. Os termos de derivada temporal das equações de Maxwell ($\frac{\partial \mathbf{B}}{\partial t}$ e a corrente de deslocamento $\epsilon \frac{\partial \mathbf{E}}{\partial t}$) são ordens de grandeza menores do que as correntes ôhmicas de condução $\mathbf{J} = \sigma \mathbf{E}$.
3. Sob a **aproximação quase-estática**:
   $$\nabla \times \mathbf{E} \approx 0 \implies \mathbf{E} = -\nabla V$$
   $$\nabla \cdot \mathbf{J} = 0 \implies \nabla \cdot (\sigma \nabla V) = -I_v$$

Onde $I_v$ representa fontes de corrente biológica por unidade de volume.

### O Dipolo de Corrente no Condutor de Volume
Como a corrente não se acumula no meio condutor, qualquer injeção de corrente positiva (*source*) em um ponto da membrana neuronal é balanceada por uma retirada equivalente (*sink*) em outro ponto, separada por uma distância $d$.

Para um dipolo de corrente com momento dipolar $p = I \cdot d$ (expresso em Amperes-metro, $\text{A}\cdot\text{m}$), o potencial $V$ a uma distância $r$ e ângulo $\theta$ em um meio homogêneo de condutividade $\sigma$ é:

$$V(r, \theta) = \frac{p \cdot \cos(\theta)}{4\pi \sigma r^2}$$

- **Alinhamento Radial ($\theta = 0$)**: Quando o dipolo aponta diretamente para o eletrodo no escalpo ($\cos(0) = 1$), para um macro-dipolo cortical de $p = 100\text{ nA}\cdot\text{m} = 10^{-7}\ \text{A}\cdot\text{m}$ a uma distância de $r = 3\text{ cm} = 0.03\text{ m}$:
  $$V = \frac{10^{-7} \cdot 1.0}{4\pi \cdot 0.33 \cdot (0.03)^2} \approx 26.79\ \mu\text{V}$$
  Esse valor corresponde com exatidão física às amplitudes registradas em traçados clínicos de EEG.
- **Cancelamento Tangencial ($\theta = \pi/2$)**: Se o dipolo está orientado perpendicularmente ao vetor posição do eletrodo ($\cos(\pi/2) = 0$), o potencial gerado na superfície é nulo ($V = 0$).

Essa formulação é a pedra angular do imageamento de fontes cerebrais ([Michel & Brunet, PMC6700197](https://pmc.ncbi.nlm.nih.gov/articles/PMC6700197/)).

## 2. Modos de Falha Operacionais
1. **Confundir Eletrostática Estática com Correntes Contínuas**: Tentar calcular voltagens cerebrais usando a permissividade do vácuo $\epsilon_0$ e cargas estáticas em Coulombs. No cérebro, cargas livres são imediatamente blindadas pela nuvem de íons da solução salina (comprimento de Debye de sub-nanômetros). O que sustenta o potencial é a circulação ativa de correntes geradas por bombas e canais iônicos transmembrana.
2. **Ignorar a Orientação Espacial ($\cos\theta$)**: Supor que a amplitude de um sinal no escalpo depende exclusivamente da força da ativação neuronal. Se uma população neuronal ativa-se nos sulcos corticais com orientação puramente tangencial em relação ao eletrodo radial superior, o potencial projetado no topo da cabeça colapsa para zero.

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-dipole-scalp`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/03-nt-dipole-scalp/room.yaml)) assume que você compreende a equação do dipolo em condutor de volume e aplica essa geometria tridimensional para modelar a atenuação de fontes piramidais orientadas radialmente no córtex até o escalpo.
