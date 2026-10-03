# Conceito — Dinâmica Celular de Membrana e a Escala Populacional

## 1. O Modelo Biofísico de Hodgkin-Huxley
Em 1952, Alan Hodgkin e Andrew Huxley formalizaram a geração do potencial de ação (*action potential* - AP) através de equações diferenciais acopladas representando a membrana neuronal como um circuito elétrico equivalente:

$$C_m \frac{dV}{dt} = - g_{Na}(V, m, h)(V - E_{Na}) - g_K(V, n)(V - E_K) - g_L(V - E_L) + I_{inj}$$

Onde:
- $C_m \approx 1\ \mu\text{F/cm}^2$: Capacitância da bicamada lipídica.
- $g_{Na}$: Condutância ativa de sódio, responsável pela despolarização rápida e regenerativa (*upstroke* positivo).
- $g_K$: Condutância de potássio dependente de voltagem, responsável pela repolarização e hiperpolarização.
- $g_L$: Condutância de vazamento passivo (*leakage*), mantendo o potencial de repouso ($V_{rest} \approx -70\text{ mV}$).

## 2. A Abstração Leaky Integrate-and-Fire (LIF)
Para processamento computacional em larga escala e simulação em tempo real, aproxima-se a dinâmica sub-limiar por um circuito RC linear com mecanismo explícito de reset:

$$\tau_m \frac{dV}{dt} = -(V - V_{rest}) + R_m I_{inj}$$

Integrando por Euler explícito com passo de tempo $\Delta t$:
$$V(t + \Delta t) = V(t) + \frac{\Delta t}{\tau_m} \left( -(V(t) - V_{rest}) + R_m I_{inj}(t) \right)$$

Se $V(t + \Delta t) \ge V_{thresh}$, o neurônio emite um spike ($fire = \text{True}$) e o potencial é forçado instantaneamente de volta ao repouso: $V(t + \Delta t) \leftarrow V_{rest}$.

## 3. Por Que o EEG de Escalpo Não Enxerga o Spike Celular
Engenheiros convencionais frequentemente cometem o erro de buscar picos de potencial de ação no EEG superficial:
1. **Duração Temporal:** O spike dura $\sim 1\text{ ms}$ ($300\text{--}3000\text{ Hz}$). A dispersão de condução axonal faz com que spikes vizinhos ocorram assincronamente, cancelando-se por interferência destrutiva.
2. **Decaimento Espacial:** O spike axonal atua como um quadrupolo elétrico de corrente, cujo potencial decai com $1/r^3$. A $2\text{--}3\text{ cm}$ de distância no escalpo, sua amplitude cai para menos de nano-volts.
3. **Origem do Macropotencial:** O EEG reflete potenciais pós-sinápticos (PSPs), que duram de $10\text{ a }100\text{ ms}$ (banda $<100\text{ Hz}$) e geram dipolos de corrente abertos que decaem apenas com $1/r^2$.

## O Que a Próxima Sala Assume
A próxima sala (`nt-neuro-synapse`) — **Neurociência — Sinapses e PSP** — transita da excitação celular axonal para a dinâmica lenta dos potenciais pós-sinápticos (PSPs) que originam o sinal de EEG.

## Artigos de Apoio e Leituras Recomendadas
- [Hodgkin & Huxley 1952](https://doi.org/10.1113/jphysiol.1952.sp004764) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
