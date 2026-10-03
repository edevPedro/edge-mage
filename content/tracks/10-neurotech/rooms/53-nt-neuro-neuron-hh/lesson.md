# Desafio — Integração Numérica de Membrana Neuronal

## 1. Objetivo do Desafio
Implementar um passo de integração temporal de Euler explícito para o modelo Leaky Integrate-and-Fire (LIF). Você deverá atualizar o potencial de membrana, avaliar se o limiar de disparo regenerativo foi superado, acionar o evento de disparo e realizar o reset estrito ao repouso.

## 2. Especificação Técnica
Implemente a função `lif_step(v, i_inj, dt=0.001, v_rest=-70.0, r=10.0, tau=0.02, v_thresh=-55.0)`:
- Calcule o incremento temporal linear:
  $$\Delta V = \frac{dt}{\tau} \left( -(v - v_{rest}) + r \cdot i_{inj} \right)$$
  $$v_{next} = v + \Delta V$$
- Avalie o limiar:
  - Se $v_{next} \ge v_{thresh}$, retorne a tupla `(v_rest, True)`.
  - Caso contrário, retorne `(v_next, False)`.

## 3. Critérios de Validação e Armadilhas
- **Reset Imediato:** Quando ocorre o disparo, o valor retornado de voltagem deve ser estritamente $v_{rest}$, e não o potencial excedente extrapolado.
- **Unidades Físicas:** Respeite a escala biológica (milivolts e milissegundos). Não confunda esse modelo celular pontual com o potencial de campo captado no escalpo.
