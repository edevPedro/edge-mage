# Vetores 2D e 3D

Um vetor **v** = `(vx, vy)` (ou 3D com `vz`) representa magnitude + direção.

## Operações

- Soma: componente a componente
- Produto escalar: `a·b = ax·bx + ay·by (+ az·bz)`
- Norma: `‖v‖ = √(vx² + vy² + …)`
- Ângulo: `cos φ = (a·b) / (‖a‖ ‖b‖)`

## No edge

Embeddings, normals de superfície, e deslocamentos de robô são vetores.
Normalizar (`v / ‖v‖`) é rotina em pipelines de sensores.
