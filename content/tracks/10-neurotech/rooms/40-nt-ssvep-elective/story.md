# História — A Luz que Faz o Córtex Cantar

Em uma sala escura de experimentação visual, um voluntário senta-se diante de uma tela onde quatro alvos piscam simultaneamente em frequências ópticas rigorosamente distintas: 10 Hz, 12 Hz, 13.5 Hz e 15 Hz. Sobre o couro cabeludo na região occipital ($Oz, O1, O2$), eletrodos de cloreto de prata capturam as oscilações cerebrais.

O desenvolvedor júnior observa o espectro na tela enquanto o voluntário fixa o olhar no alvo de 12 Hz:
— Olha o que está acontecendo em 12 Hz — diz o desenvolvedor. — Não há necessidade de o voluntário imaginar movimento algum ou aprender modulação cinestésica! Uma espícula espectral afiada e potente eleva-se exatamente em 12 Hz, acompanhada de um segundo harmônico perfeitamente visível em 24 Hz!

O engenheiro de visão computacional e biossinais do laboratório explica o fenômeno:
— Este é o paradigma dos Potenciais Evocados Visuais de Estado Estável (SSVEP) — ensina o especialista. — Quando a retina recebe pulsos de luz em uma taxa repetitiva, as populações neuronais do córtex visual primário (área V1) são arrastadas pela estimulação e passam a disparar em fase, ressoando na mesma frequência do estímulo e em seus harmônicos inteiros.

Ele detalha a arquitetura do detector:
— Enquanto a imagética motora exige treinamento do voluntário para aprender a desincronizar ritmos, o SSVEP é um paradigma de alta taxa de transferência de informação (ITR) quase imediata. Para decodificar qual alvo o usuário está olhando, nós não precisamos de redes profundas: basta verificar se a densidade espectral no canal $Oz$ na frequência do estímulo ultrapassa um limiar estrito em relação à banda vizinha (`ssvep_detect`), ou aplicar Análise de Correlação Canônica (CCA).

A equipe testa o detector: ao desviar o olhar para o alvo de 15 Hz, a espícula de 12 Hz apaga-se e o pico de 15 Hz ergue-se com precisão instantânea, ativando o comando na tela em menos de meio segundo.
