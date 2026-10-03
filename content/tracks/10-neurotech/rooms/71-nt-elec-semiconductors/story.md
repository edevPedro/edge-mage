# História — O Choque Eletrostático de Dez Mil Volts

Em uma tarde de inverno seco em um laboratório de neuroengenharia, uma técnica caminha sobre o carpete isolante sintético da sala. Ao estender a mão para conectar o cabo de eletrodos à placa de aquisição de biopotenciais, uma faísca azul salta de sua ponta do dedo diretamente no conector do canal 1 com um estalo seco: uma descarga eletrostática (ESD) de quase dez mil volts.

O estudante que observava a cena coloca as mãos na cabeça:
— Queimamos os amplificadores operacionais ultra-sensíveis de microvolts! — teme ele.

O engenheiro de hardware sênior conecta a placa ao computador e executa a rotina de auto-teste do conversor:
— A placa está intacta e funcionando perfeitamente — anuncia o engenheiro com tranquilidade.

Ele abre o esquemático do circuito impresso e aponta para o par de diodos semicondutores de proteção posicionados logo na entrada de cada pino:
— O corpo humano pode acumular cargas eletrostáticas que ultrapassam $15.000\text{ V}$ em dias secos. Nenhuma junção de silício microscópica de um pré-amplificador resiste a essa tensão sem ser destruída por ruptura dielétrica instantânea. Por isso, toda entrada biológica possui diodos semicondutores de grampeamento de ESD (ESD Clamping Diodes) conectados em antiparalelo entre o pino de sinal e os trilhos de alimentação positiva e negativa.

Ele explica o funcionamento semicondutor do grampo:
— Em operação normal de EEG ($V \approx 50\ \mu\text{V}$), os diodos permanecem reversamente polarizados, comportando-se como circuitos abertos ideais com corrente de fuga minúscula ($< 1\text{ pA}$). No instante em que a descarga de 10.000 volts atinge o pino, o diodo superior polariza-se diretamente em 0.7 V quando a tensão supera o trilho positivo ($V_{CC} + V_D$), e o diodo inferior conduz quando a tensão cai abaixo do trilho negativo ($V_{EE} - V_D$). A energia destrutiva da faísca é desviada com segurança para a terra através dos trilhos, limitando a tensão no chip a um valor inofensivo.

A equipe implementa a função `esd_clamp`. A compreensão da física de semicondutores consolida o projeto de dispositivos médicos resistentes ao manuseio humano cotidiano.
