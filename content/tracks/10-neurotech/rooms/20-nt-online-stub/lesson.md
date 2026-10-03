# Lição — Online stub

## Objetivos

Descrever o loop; medir latency; obter a runa online.

## Passos

1. Escreva o pseudo-loop completo.
2. Defina W e hop compatíveis com `fs`.
3. Rode o emulator; anote latências.
4. Compare miss vs hit sob deadline da Sala.
Para destravar o lab, abra [Blankertz et al. — The Berlin Brain-Computer Interface (Frontiers OA, PMC5116473)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5116473/) e leia como Blankertz separa o loop online (janela, decisão, tempo) do replay offline, para as coordenadas de sliding_windows caberem no deadline.


## Lab

Tabela: window_id | latency_ms | hit/miss.

## Checklist

- [ ] Loop claro
- [ ] Deadline explícito
- [ ] Runa online

## Caderno (domínio)

Escreva 1 página: (1) diagrama desta sala, (2) 3 números com unidade, (3) honesty note, (4) ligação à sala anterior e seguinte do PEDAGOGICAL path. Isto conta como Estuda completo antes da Sala.

## Leitura e ponte (feche o Estuda)

Relacione esta sala ao mapa: pilares → espinha decode → online → research.
Cite um DOI/PMC dos resources do `room.yaml` em uma frase Methods-style.
Declare explicitamente o que *não* está coberto (limites) para não overclaim na Sala.
Calcule um número extra além da task (mesmo estimativa de ordem de grandeza) e anote a unidade.
Só então abra a Sala / FLAG.

## Nota final
O stub online é a ponte entre κ offline e closed-loop: sem ele, latência e underrun ficam teoria. Complete o Estuda, rode o emulator, e só então busque a runa.
