# Derivadas (intuição)

O **gradiente** é a generalização da derivada. Antes de descer a loss, entenda a taxa de variação.

## Em 1D

Se `f(x)` é suave, a derivada `f'(x)` diz quanto `f` muda por unidade de `x`:

- `f'(x) > 0` → f cresce quando x aumenta
- `f'(x) < 0` → f decresce quando x aumenta
- `f'(x) = 0` → ponto estacionário (candidato a mínimo/máximo)

Aproximação: `f'(x) ≈ (f(x+h) − f(x)) / h` com h pequeno (diferença finita).

## Regras que você vai usar

- `(xⁿ)' = n xⁿ⁻¹`
- `(eˣ)' = eˣ`
- `(ln x)' = 1/x` (x > 0)
- `(af + bg)' = a f' + b g'`

## Regra da cadeia

Se `y = f(g(x))`, então `dy/dx = f'(g(x)) · g'(x)`.

Em redes: a loss depende da saída, que depende de Wx+b, que depende de W.
O **backprop** é a regra da cadeia aplicada camada a camada.

## Ligação com descida

Queremos **diminuir** f. Em 1D: ande no sentido **oposto** ao sinal de f':

`x ← x − η f'(x)`

Em várias dimensões, troque f' pelo vetor gradiente ∇f.
