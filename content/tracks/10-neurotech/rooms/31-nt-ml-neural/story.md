# História — Os pesos das duas primeiras camadas

N é pequeno; a rede não é o primeiro reflexo. Ainda assim a Sala pede a conta de parâmetros, para ver o descompasso. `eegnet_params_first_layers(16, 8, 2, 64)`: 16 canais, `F1 = 8`, profundidade `D = 2`, kernel temporal 64.

Temporal: `F1 * kernel_len = 8 * 64 = 512`. Espacial depthwise: `F1 * D * C = 8 * 2 * 16 = 256`. Soma: `512 + 256 = 768`. Esquecer o termo espacial entrega 512; usar `C = 64` como se canal fosse kernel entrega outro milhar.

768 pesos só nestas duas fatias, antes do classificador, contra poucos trials por classe: daí a ordem MSc-prep — regularizar, baseline linear, não “deep porque sim”. O 768 é contagem de parâmetros, não acurácia e não evidência clínica. Lotte fica como freio de revisão, não como selo de que a conta reproduz um benchmark.

Fase F8, nt-ml-neural: 8×64 mais 8×2×16 fecha em 768 parâmetros. Esse inteiro é tamanho de hipótese, não taxa de acerto — com poucos trials ele é o argumento para regularizar antes de aprofundar a rede.
