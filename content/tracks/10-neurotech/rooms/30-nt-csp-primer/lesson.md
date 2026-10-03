# Desafio — Filtragem Espacial e Cálculo de Log-Variância (CSP Feature)

## 1. Objetivo do Desafio
Implementar a rotina de projeção espacial de um ensaio multicanal de EEG através de um vetor de filtro espacial e computar a log-variância resultante como característica discriminante.

## 2. Especificação Técnica e Formulação
Dado um ensaio multicanal `epoch` representado como um array bidimensional com $C$ linhas (canais) e $T$ colunas (amostras temporais), e um vetor de pesos espaciais $w$ de comprimento $C$:
- Implemente a função `spatial_filter_logvar(epoch, w)`:
  1. Calcule a projeção linear temporal: $s[t] = \sum_{c=0}^{C-1} w[c] \times \text{epoch}[c, t]$ para cada instante $t = 0, \dots, T-1$.
  2. Calcule a variância amostral de $s$:
     $$V = \frac{1}{T} \sum_{t=0}^{T-1} (s[t] - \bar{s})^2$$
  3. Retorne a log-variância na base 10:
     $$f = \log_{10}(V + 10^{-10})$$
     (Onde $10^{-10}$ atua como piso de regularização para prevenir $\log(0)$).

## 3. Critérios de Validação e Armadilhas
- Certifique-se de subtrair a média do sinal projetado $\bar{s}$ antes de elevar os desvios ao quadrado.
- A dimensionalidade de $w$ deve ser rigorosamente igual ao número de canais $C$ da matriz de entrada.
