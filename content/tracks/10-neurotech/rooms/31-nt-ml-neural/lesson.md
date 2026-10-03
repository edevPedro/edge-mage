# Desafio — Contagem de Parâmetros e Arquitetura EEGNet

## 1. Objetivo do Desafio
Implementar a rotina de cálculo analítico da quantidade de parâmetros treináveis da arquitetura compacta EEGNet, compreendendo como convoluções depthwise e separáveis restringem a capacidade do modelo para prevenir overfitting em $N \ll D$.

## 2. Especificação Técnica e Formulação
Dadas as dimensões de entrada e hiperparâmetros canônicos: número de canais `n_channels`, número de amostras temporais `n_samples`, número de classes `n_classes`, e os filtros $F_1$, $D$, e $F_2 = F_1 \times D$:
- Implemente a função `eegnet_params_count(n_channels, n_samples, n_classes, f1, d, f2)` calculando a soma analítica dos pesos das camadas convolucionais e da camada linear densa de saída.
- Para a configuração padrão de referência ($C = 64, F_1 = 8, D = 2, F_2 = 16, \text{classes} = 4$), o total de parâmetros deve situar-se estritamente na faixa de $1.500\text{ a } 3.500$ parâmetros.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que a contagem inclua os biases de cada camada convolucional e densa.
- Lembre-se: em neuroengenharia, o modelo mais elegante é aquele que atinge a máxima precisão com o mínimo de parâmetros livres.
