# Lição — Stats BCI

## Objetivos

Calcular κ; declarar chance level; evitar accuracy solitária.

## Passos

1. Matriz de confusão 2×2 → `p_o`.
2. `p_e` para classes balanceadas vs desbalanceadas.
3. κ numérico (Sala).
4. Escreva frase Methods: “reportamos κ ± … com CV trial-wise; chance …”

Para destravar o lab, abra [Schlögl et al. JNE 2005 — κ / 4-class MI](https://doi.org/10.1088/1741-2560/2/4/L02) e leia a fórmula de κ em Schlögl para não reportar p_o cru no lugar de (p_o − p_e)/(1 − p_e) nem um p de permutação sem o 1+.

## Labs

**Numeric.** 60/80 acertos, 2 classes eq. → `p_o`, κ.

**Critique.** Paper com 92% sem N nem chance — o que pedir no review?

## Caderno (domínio)

Escreva 1 página: (1) diagrama desta sala, (2) 3 números com unidade, (3) honesty note, (4) ligação à sala anterior e seguinte do PEDAGOGICAL path. Isto conta como Estuda completo antes da Sala.

## Leitura e ponte (feche o Estuda)

Relacione esta sala ao mapa: pilares → espinha decode → online → research.
Cite um DOI/PMC dos resources do `room.yaml` em uma frase Methods-style.
Declare explicitamente o que *não* está coberto (limites) para não overclaim na Sala.
Calcule um número extra além da task (mesmo estimativa de ordem de grandeza) e anote a unidade.
Só então abra a Sala / FLAG.
