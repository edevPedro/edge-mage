# Conceito — Testes de Tempo Real, Análise de Jitter e Violação de Prazos

## 1. Determinismo Temporal em Sistemas de Tempo Real
Em interfaces cérebro-computador conectadas a atuadores físicos (cadeiras de rodas, próteses, exoesqueletos, estimuladores neurais):
- Não basta que o algoritmo compute o comando correto; o resultado deve ser entregue dentro de uma janela temporal estrita.
- **Intervalo Alvo ($T_{target}$):** O período nominal de amostragem ou de atualização do laço de controle. Exemplo: para $f_s = 250\text{ Hz}$, $T_{target} = 1/250 = 0.004\text{ s}$ ($4\text{ ms}$).

## 2. Definição Formal de Jitter Temporal
Sejam $t_0, t_1, \dots, t_{N-1}$ os instantes de tempo absolutos (timestamps em segundos) nos quais amostras ou eventos sucessivos foram processados.

O intervalo observado entre dois eventos consecutivos $i$ e $i+1$ é:
$$\Delta t_i = t_{i+1} - t_i, \quad \text{para } i = 0, \dots, N-2$$

O jitter absoluto instantâneo é o desvio em módulo em relação ao intervalo alvo:
$$\text{jitter}_i = |\Delta t_i - T_{target}|$$

A média de jitter ao longo dos $N-1$ intervalos observados é dada por:
$$\overline{\text{jitter}} = \frac{1}{N - 1} \sum_{i=0}^{N-2} |\Delta t_i - T_{target}|$$

## 3. Detecção de Violações de Prazo (*Misses*)
Uma violação de prazo (*timing miss*) ocorre sempre que o jitter instantâneo excede uma tolerância máxima pré-estabelecida ($max\_jitter$):

$$\text{miss}_i = \begin{cases} 1, & \text{se } |\Delta t_i - T_{target}| > max\_jitter \\ 0, & \text{caso contrário} \end{cases}$$

O total de violações é $count_{misses} = \sum_{i=0}^{N-2} \text{miss}_i$.

## 4. Consequências de Jitter Elevado em Malha Fechada
- **Distorção Espectral:** Jitter na amostragem equivale a modulação espúria de fase, criando bandas laterais de ruído artificial no espectro do EEG (*sampling jitter noise*).
- **Instabilidade no Controle:** Atuadores robóticos alimentados com comandos desiguais no tempo sofrem solavancos mecânicos e podem entrar em oscilações instáveis perigosas.

## O Que a Próxima Sala Assume
A próxima sala (`nt-filter-bank`) — **Banco de filtros EEG** — inicia o processamento digital de sinais estruturando bancos de filtros passa-faixa causais para isolar bandas fisiológicas de interesse.

## Artigos de Apoio e Leituras Recomendadas
- [Varoquaux et al. — CV pitfalls](https://doi.org/10.1016/j.neuroimage.2016.10.038) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
