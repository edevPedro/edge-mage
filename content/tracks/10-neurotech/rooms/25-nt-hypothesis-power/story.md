# História — O d de Cohen e o alfa fatiado

Antes de caçar banda, o guardião exige tamanho de efeito. Duas médias de laboratório: `m1 = 10`, `s1 = 2`, `m2 = 8`, `s2 = 2`. `cohens_d` é `(m1 − m2) / sqrt((s1² + s2²) / 2)`.

Numerador: 2. Dentro da raiz: `(4 + 4) / 2 = 4`, raiz 2. `d = 2 / 2 = 1`. Trocar o desvio pooled por uma soma sem o `/2` entrega `2/sqrt(8)` e não passa. Unidade: adimensional, não µV.

Na mesma mesa, Bonferroni: `α = 0,05`, `m = 10` testes, `α' = 0,005`. Potência é `1 − β`, a chance de rejeitar H0 quando H1 é verdadeira — a palavra do fill, não um percentual decorativo. Pré-registrar a família de testes é o freio; o synth não vira evidência clínica porque `d` deu 1 num vetor de brinquedo.

Fase F8, nt-hypothesis-power: cohens_d(10, 2, 8, 2) vale 1, e α' com 10 testes a 0,05 vale 0,005. O fill da potência é a palavra potência (1−β), não o valor de d.
