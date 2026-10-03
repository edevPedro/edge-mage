# Desafio — Modelagem Analítica da Condutância Pós-Sináptica

## 1. Objetivo do Desafio
Implementar a função de condutância pós-sináptica baseada na formulação analítica alfa de Rall, simulando a resposta transitória de um canal iônico estimulado por neurotransmissores.

## 2. Especificação Técnica
Implemente a função `alpha_conductance(t, tau=0.005, g_peak=1.0)`:
- Para $t < 0$, a condutância deve ser estritamente $0.0$.
- Para $t \ge 0$, calcule a condutância utilizando a fórmula exponencial normalizada:
  $$g(t) = g_{peak} \cdot \left(\frac{t}{\tau}\right) \cdot \exp\left(1 - \frac{t}{\tau}\right)$$
- Utilize a biblioteca `math.exp` para a exponenciação contínua.

## 3. Critérios de Validação e Armadilhas
- **Pico em $\tau$:** Verifique se em $t = \tau$, o valor retornado corresponde exatamente a $g_{peak}$.
- **Causalidade Estrita:** Garanta que tempos negativos não gerem exceções matemáticas ou valores de condutância espúrios.
