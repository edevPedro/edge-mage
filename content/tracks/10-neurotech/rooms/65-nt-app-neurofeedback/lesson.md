# Desafio — Função de Recompensa de Neurofeedback Retificada

## 1. Objetivo do Desafio
Implementar a rotina de mapeamento de recompensa sensorial em malha fechada para um protocolo de neurofeedback de ritmo alfa, aplicando retificação estrita para garantir reforço positivo sem sinais espúrios negativos.

## 2. Especificação Técnica
Implemente a função `nfb_reward(current_alpha, baseline_alpha, scale=10.0)`:
- Calcule a diferença entre a potência alfa observada e a potência de referência da linha de base:
  $$\Delta P = current\_alpha - baseline\_alpha$$
- Aplique o escalonamento multiplicativo e a retificação não-negativa:
  $$\text{recompensa} = \max(0.0, \Delta P \times scale)$$
- Retorne o valor numérico float resultante.

## 3. Casos de Teste Canônicos
```python
# Acima da baseline: (15.0 - 10.0) * 10.0 = 50.0
assert abs(nfb_reward(15.0, 10.0, 10.0) - 50.0) < 1e-5

# Abaixo da baseline: (8.0 - 10.0) * 10.0 = -20.0 -> retifica para 0.0
assert nfb_reward(8.0, 10.0, 10.0) == 0.0
```

## 4. Critérios de Validação e Armadilhas
- Certifique-se de que qualquer valor de potência atual menor ou igual à linha de base retorne exatamente `0.0`.
