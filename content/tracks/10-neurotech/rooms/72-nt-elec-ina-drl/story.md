# História — O Cancelamento Ativo do Zumbido de Sessenta Hertz

Na bancada de testes de um eletroencefalógrafo clínico, uma pesquisadora e um engenheiro de instrumentação biomédica tentam registrar sinais de EEG sem gaiola de Faraday em uma sala comercial comum. Assim que o voluntário senta-se na cadeira, a forma de onda nos canais $C3$ e $C4$ satura nos trilhos de alimentação: um bloco sólido de onda senoidal de 60 Hz com quase dois volts de amplitude esmaga o biopotencial de microvolts.

O desenvolvedor tenta sugerir um filtro digital notch mais agressivo, mas a pesquisadora balança a cabeça:
— Se o ruído de 60 Hz estiver saturando o amplificador analógico nos trilhos de alimentação ($+2.5\text{ V}$ e $-2.5\text{ V}$), o conversor analógico-digital digitalizará uma onda quadrada ceifada. Nenhum filtro digital do mundo consegue restaurar informação de um sinal que sofreu ceifamento analógico (clipping) — adverte ela. — O ruído precisa ser eliminado no domínio analógico antes da digitalização!

O engenheiro sênior abre a arquitetura clássica de dois pilares da instrumentação biomédica:
1. **O Amplificador de Instrumentação (INA):** Uma topologia clássica de três amplificadores operacionais onde o ganho diferencial é configurado por um único resistor externo $R_G$:
   $$A_v = 1 + \frac{2 R_1}{R_G}$$
   O INA rejeita tensões que aparecem simultaneamente nos dois eletrodos, com CMRR superior a 110 dB.
2. **O Circuito Driven Right Leg (DRL):**
   — O corpo do paciente atua como uma grande placa capacitiva que acopla corrente de deslocamento da rede elétrica residencial — explica o engenheiro. — O DRL extrai a tensão de modo comum nos dois eletrodos através de resistores de alta impedância, inverte a fase da onda em 180 graus com um amplificador inversor e injeta essa corrente em oposição de fase de volta no corpo do paciente através de um eletrodo de referência na perna direita ou na orelha.

A equipe implementa o circuito DRL e calcula o resistor de ganho do INA (`ina_gain`). No momento em que o eletrodo DRL toca a pele do voluntário, a interferência de 60 Hz colapsa em mais de 40 dB: a onda gigantesca de 2 volts encolhe para menos de 10 microvolts, permitindo que os biopotenciais do córtex motor surjam na tela com estabilidade perfeita.
