# História — A Saturação do Primeiro Estágio

Em um protótipo de placa de aquisição de biopotenciais desenhada para testes de bancada, um projetista de firmware resolve otimizar o SNR analógico antes da digitalização. Sabendo que o sinal de EEG é minúsculo ($15\text{--}30\ \mu\text{V}$), ele ajusta o resistor de ganho $R_G$ do amplificador de instrumentação para fornecer um ganho analógico $G = 100$.

A placa é alimentada pela linha de $3.3\text{ V}$ do barramento USB. Ao conectar os eletrodos de prata/cloreto de prata na pele de um voluntário, o conversor A/D lê apenas valores travados no teto digital máximo de $3.3\text{ V}$.

O engenheiro de hardware sênior conecta a ponta de prova do multímetro diretamente nos terminais diferenciais de entrada antes do chip. Ele constata um potencial estático contínuo de $+48\text{ mV}$ entre os dois eletrodos, resultante das reações químicas espontâneas entre a pele e o gel eletrolítico. Multiplicados pelo ganho de cem, esses $48\text{ mV}$ resultam em uma tensão de saída teórica de $4.8\text{ V}$ — impossível de ser gerada por um circuito alimentado em $3.3\text{ V}$.

O amplificador de instrumentação estava colado no trilho de saturação superior. O desenvolvedor é instruído a recalibrar o ganho do estágio analógico para valores moderados ($G \le 12$) ou implementar o circuito de realimentação de perna direita (DRL) para absorver o modo comum e acomodar o offset galvânico dentro da janela linear dinâmica.
