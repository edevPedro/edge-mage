# História — A Lição de Berlim

No anfiteatro de computação científica, um estudante de mestrado preparava-se para defender seu trabalho preliminar sobre classificação de eletroencefalografia motora. Para demonstrar a eficácia de sua rede neural profunda, ele havia inventado perfis hipotéticos de pacientes em seu código: *"Paciente A com lesão medular C5", "Paciente B em reabilitação de AVC"*.

O professor titular interrompeu a apresentação antes do segundo slide:

— "De onde saíram os dados desses 'pacientes'? Qual foi o protocolo aprovado pelo comitê de ética institucional? Qual é o identificador de registro do ensaio clínico?"

O estudante confessou, constrangido:

— "Eu gerei os dados aleatoriamente no NumPy e inventei as histórias dos pacientes para contextualizar o modelo..."

O professor apontou para o projetor:

— "Em ciência da engenharia biomédica, inventar participantes ou diagnósticos fictícios é uma infração gravíssima de integridade científica. Quando nós desenvolvemos algoritmos educacionais ou pipelines sintéticos, nós fazemos **emulação metodológica** baseada estritamente em paradigmas e dados abertos publicados pela comunidade científica internacional — como os célebres trabalhos do Berlin BCI liderados por Blankertz, Müller e Curio."

O professor abriu o artigo clássico do Berlin BCI:

— "O grupo de Berlim revolucionou o campo ao demonstrar que uma calibração rápida de 20 minutos de imagética motora permite controle em tempo real robusto. O núcleo biofísico do paradigma de Berlim é a assimetria hemisférica contralateral do ritmo mu: quando o sujeito imagina a mão direita, o canal C3 (hemisfério esquerdo) sofre dessincronização profunda, enquanto o canal C4 permanece estável. A razão de potência $C3/C4$ torna-se menor que 1.0. Se a imagética for da mão esquerda, $C4$ dessincroniza e a razão $C3/C4$ supera 1.0. É essa elegância biofísica que nós estudamos, citando a fonte com DOI e declarando claramente os limites da nossa emulação didática."
