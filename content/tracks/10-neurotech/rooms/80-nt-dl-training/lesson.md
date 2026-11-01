# Desafio — Softmax + Cross-entropy estáveis

## 1. Objetivo do Desafio
Implementar softmax numericamente estável e cross-entropy, as pernas da loss de
classificação que toda rede (incluindo as de EEG) usa.

## 2. Especificação Técnica e Formulação
- `softmax(logits)` → `p_i = exp(z_i − m) / Σ exp(z_j − m)` com `m = max(logits)`
  (estabilidade — evita `exp(1000)`).
- `cross_entropy(logits, y_true)` → média de `−Σ_i y_i·log(p_i)` sobre exemplos,
  onde `y_true` é lista de one-hot e `p = softmax(logits)`.
- `log(0.0)` deve ser tratado como `-inf` / grande — não pode quebrar.

## 3. Critérios de Validação e Armadilhas
- Softmax com logits iguais → distribuição uniforme (dica dos testes).
- CE de logits [10, 0] na classe 0 deve ser ~0 (confiança alta correta);
  CE de [0, 10] na classe 0 deve ser > 1 (confiança alta errada é cara).
- Use `math.log`, não `log` de outro namespace.