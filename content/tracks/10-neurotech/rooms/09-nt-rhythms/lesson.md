# Desafio — Mapeamento e Identificação de Ritmos Cerebrais

## 1. Objetivo do Desafio
Identificar com precisão os intervalos de frequência característicos das bandas fisiológicas de EEG, reconhecer os ritmos centrais para paradigmas de imagética motora e implementar um algoritmo para seleção do ritmo espectral dominante.

## 2. Especificação Técnica e Formulação
Dada uma estrutura contendo a potência estimada em cada faixa de frequência de um canal de EEG:
- **Faixas Canônicas:** Alfa ($8	ext{--}12	ext{ Hz}$), Beta ($12	ext{--}30	ext{ Hz}$), Gama ($> 30	ext{ Hz}$).
- **Ritmo Dominante:** Desenvolva a função `dominant_rhythm(powers_dict)` que recebe um dicionário mapeando nomes de bandas em valores de potência (flutuantes positivos) e retorna o nome da banda de maior magnitude espectral:
  $$\text{banda dominante} = \arg\max_{b} P(b)$$

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que a função lida corretamente com empates ou valores em escala linear/logarítmica.
- Nunca confunda ritmos sensoriomotores $\mu/eta$ com ritmos visuais occipitais em aplicações de decodificação motora.
