# História — A Maldição dos Milhões de Parâmetros

Em um hackathon de inovação em inteligência artificial, uma equipe de cientistas de dados decide criar um decodificador de BCI utilizando um modelo Transformer com 50 milhões de parâmetros, treinado a partir do zero. A base de dados disponível consistia em 160 ensaios de calibração coletados em um único voluntário durante uma tarde.

Após duas horas de treinamento em uma GPU de alta potência, a função de perda no conjunto de treino atingiu zero absoluto: acurácia de treino de 100%. Porém, ao submeter o modelo ao conjunto de teste oculto da bancada de avaliação, a acurácia colapsou para 49.5% — pior que um chute aleatório.

O pesquisador sênior de machine learning neural aproximou-se da equipe com uma folha de papel:
— Em visão computacional ou processamento de linguagem natural, nós temos bilhões de amostras para milhões de parâmetros ($N \gg D$). Em neuroengenharia de BCI, a realidade é o oposto exato: nós temos poucos ensaios e altíssima dimensionalidade de ruído ($N \ll D$) — explicou o pesquisador. — Quando você coloca 50 milhões de parâmetros para aprender 160 ensaios, a rede neural memoriza as flutuações microscópicas de impedância eletroquímica do couro cabeludo do sujeito naquele minuto específico.

Ele apresentou as diretrizes da arquitetura EEGNet (Lawhern et al., 2018):
— Redes neurais em BCI só funcionam quando incorporam o conhecimento da física de sinais diretamente na sua arquitetura (inductive bias). A EEGNet utiliza convoluções temporais seguidas de convoluções em profundidade espaciais (depthwise spatial convolutions), imitando rigorosamente a decomposição em bancos de filtros e CSP. O modelo completo possui menos de 3.000 parâmetros!

A equipe realizou o cálculo formal de contagem de parâmetros (`eegnet_params_count`). Com um modelo compacto, fortemente regularizado com Dropout e restrições de norma nas camadas convolucionais, o overfitting desapareceu e o modelo superou com folga o classificador linear tradicional em dados não vistos.
