# Desafio — Detecção de Picos Harmônicos em SSVEP

## 1. Objetivo do Desafio
Implementar a rotina de detecção de frequência em paradigma SSVEP, verificando se a densidade de potência na frequência alvo supera o limiar de magnitude em relação ao ruído de fundo.

## 2. Especificação Técnica e Formulação
Dado um dicionário de densidades espectrais `psd_dict` (onde as chaves são frequências em float/int e os valores são potências em $\mu\text{V}^2/\text{Hz}$), uma frequência alvo `target_freq` e um limiar escalar `threshold`:
- Implemente a função `ssvep_detect(psd_dict, target_freq, threshold)`:
  - Extraia a potência na frequência alvo $P_{\text{target}} = \text{psd\_dict.get(target\_freq, 0.0)}$.
  - Retorne `True` se $P_{\text{target}} \ge \text{threshold}$, e `False` caso contrário.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de lidar com a ausência da chave no dicionário retornando `False`.
- Lembre-se: esta sala é uma matéria eletiva e não bloqueia a progressão obrigatória para o Mago Supremo.
