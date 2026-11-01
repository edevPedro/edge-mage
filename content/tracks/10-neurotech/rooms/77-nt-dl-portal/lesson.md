# Desafio — Mapa do Módulo Deep Learning & Inference

## 1. Objetivo do Desafio
Localizar no mapa (roadmap.sh/inference-engineering) os quatro blocos que vamos
percorrer (Deep Learning, Geração, Otimização, Serviço) e implementar a regra
didática de decisão N≫D vs N≪D que abre o módulo.

## 2. Especificação Técnica e Formulação
Implemente `suggest_approach(n_samples, n_dims, ratio_threshold=10.0)`:
- Se `n_samples / n_dims ≥ ratio_threshold`, retorne `"dl"` (regime rico em dados);
- Caso contrário retorne `"classic"` (N≪D — baseline linear/CSP primeiro).

## 3. Critérios de Validação e Armadilhas
- Divisão por zero / `n_dims == 0`: trate como `"classic"` (sem dados o bastante).
- A regra é didática — o veredito no mundo real mistura pipeline, validação e
  orçamento de latência, não só a razão de amostras.