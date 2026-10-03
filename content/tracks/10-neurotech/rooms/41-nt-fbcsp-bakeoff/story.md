# História — O log que junta os bancos

Bake-off honesto usa o mesmo split nos dois métodos. Antes disso, a Sala pede o vetor FBCSP: `fbcsp_features` recebe potências por sub-banco, aqui `[[10], [100]]`, e concatena `ln(p + 1e-6)`.

Primeiro banco: `ln(10 + 1e-6)`. Segundo: `ln(100 + 1e-6)`. Não é `ln(10)` pelado se o código soma o epsilon — a diferença é minúscula, mas o teste mede contra `log(p + 1e-6)`. Não é a potência crua 10 e 100: sem o log, a escala de um banco domina o outro.

FBCSP é filter-bank mais CSP, não “a rede que ganhou”. O ln é a feature; a comparação com Riemann vem depois, no mesmo protocolo. Dois números de brinquedo não são κ de competição. Esquecer um banco entrega vetor de comprimento 1 e a Sala corta o bake-off antes de qualquer gráfico.

Eletivo nt-fbcsp-bakeoff: o vetor começa em ln(10+1e-6) e ln(100+1e-6). FBCSP é filter-bank mais CSP; comparar método sem o mesmo split não é bake-off, é poster.
