# História — O Falso Triunfo do Piscar de Olhos

Em uma apresentação de progresso em um centro de reabilitação motora, um grupo de bolsistas celebrava um resultado aparentemente espetacular: seu novo classificador de imagética motora havia alcançado 98.4% de acurácia na separação entre as classes de movimento imaginado da mão direita e repouso. O resultado superava os melhores benchmarks da literatura internacional.

O engenheiro de instrumentação do hospital, experiente em eletrofisiologia clínica, aproximou-se do osciloscópio digital que monitorava a linha de sinal bruta dos voluntários.

— O protocolo experimental de vocês apresenta um estímulo visual com contraste brilhante na tela quando o sujeito deve iniciar a imagética, correto? — perguntou ele.

Os pesquisadores confirmaram. O engenheiro pediu para carregar o traçado bruto temporal do canal frontal $Fp1$ e dos canais centrais $C3$ e $C4$.

— Observem a escala vertical — apontou ele. — O sinal de EEG sensoriomotor autêntico varia entre $10$ e $40\ \mu\text{V}$. No momento exato em que a tela acende, o eletrodo frontal registra uma deflexão parabólica gigantesca de quase $300\ \mu\text{V}$, que se propaga por condução de volume até os eletrodos parietais e centrais. O voluntário involuntariamente pisca toda vez que a seta luminosa surge.

O engenheiro explicou a biofísica do artefato: o globo ocular é um dipolo elétrico permanente, com a córnea positiva em relação à retina. Quando a pálpebra desce e sobe durante a piscada, ela atua como um condutor deslizante que desvia o campo elétrico do olho, injetando centenas de microvolts no couro cabeludo (Eletrooculograma - EOG).

— O algoritmo de vocês não aprendeu imagética motora. Ele aprendeu a classificar se o voluntário piscou ou não — concluiu o engenheiro. — Se filtrarmos ou rejeitarmos os ensaios com amplitudes espúrias acima de $100\ \mu\text{V}$, a acurácia do modelo desaba para 54%.

O grupo compreendeu a lição mais dura da neuroengenharia: em biopotenciais de microvolts, qualquer sistema de validação que não implemente rotinas estritas de detecção e rejeição de artefatos biológicos e ambientais é um gerador de ilusões estatísticas.
