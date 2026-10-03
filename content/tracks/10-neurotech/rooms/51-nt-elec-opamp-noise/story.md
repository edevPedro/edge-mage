# História — O Amplificador de Cinco Centavos

Na bancada de prototipagem rápida de hardware, um estagiário de engenharia montava um amplificador caseiro para EEG em uma matriz de contatos. Para economizar no custo de lista de materiais, ele havia substituído o front-end analógico integrado por um amplificador operacional genérico duplo, daqueles encontrados em fontes de alimentação comerciais.

"O circuito tem ganho de dez mil vezes," dizia ele, apontando para o osciloscópio. "A voltagem na saída balança entre zero e três volts toda vez que eu fecho os olhos."

O engenheiro eletrônico sênior da equipe aproximou-se, conectou um analisador de espectro à bancada e desconectou os eletrodos da cabeça do estagiário, substituindo-os por resistores fixos de dez quilo-ohms para medir o ruído intrínseco. A forma de onda continuava oscilando com picos gigantescos.

"Olhe para o datasheet do componente que você escolheu," disse o sênior, abrindo o PDF na tela. "A densidade espectral de ruído de tensão na entrada é de quarenta nanovolts por raiz de hertz, e a corrente de polarização é de cinquenta nanoamperes. Em uma largura de banda de cem hertz, o ruído do amplificador somado ao ruído térmico Johnson dos seus eletrodos já passa de meio microvolt antes mesmo de encostar na pele."

O engenheiro fez a conta rápida no papel: com dez mil de ganho, meio microvolt de ruído vira cinco milivolts na saída. E os cinquenta nanoamperes de corrente de fuga fluindo por uma resistência de contato de dez quilo-ohms geram um offset de quinhentos microvolts na entrada, que multiplicado por dez mil resulta em cinco volts — saturando imediatamente os trilhos de alimentação do chip.

"O que você estava vendo no osciloscópio não era ritmo alfa," explicou o sênior. "Era o próprio amplificador saturando e oscilando no seu próprio piso de ruído térmico. Em sinais de microvolts, você não escolhe componentes pelo ganho da malha; você escolhe pela densidade de ruído na entrada e pela corrente de fuga."
