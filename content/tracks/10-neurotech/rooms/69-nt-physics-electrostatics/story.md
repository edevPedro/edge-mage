# História — A Carga que Não Existia

Na sala de simulação física de um laboratório de neuroengenharia, um recém-graduado em ciência da computação apresentava seu primeiro motor de propagação de campo elétrico cerebral. Ele havia modelado os neurônios como esferas de metal carregadas estaticamente com cargas pontuais na casa de picocoulombs, aplicando a lei de Coulomb com a permissividade elétrica do vácuo.

"O algoritmo calcula as forças eletrostáticas par a par usando árvores de Barnes-Hut," explicava ele com orgulho. "Mas quando eu rodo a simulação para o crânio, os potenciais calculados explodem na casa de milhares de volts."

O físico do laboratório aproximou-se da tela, deu uma risada amigável e pediu para o jovem engenheiro olhar para uma garrafa de soro fisiológico sobre a bancada.

"O interior do crânio não é o espaço sideral," explicou o físico. "É uma solução eletrolítica densa de cloreto de sódio e potássio, com condutividade de cerca de 0,33 Siemens por metro. Qualquer carga eletrostática líquida colocada na água salgada é neutralizada em picossegundos pela redistribuição iônica — o comprimento de Debye aqui é de menos de um nanômetro."

Ele pegou uma caneta e escreveu no quadro a equação da aproximação quase-estática de Maxwell para meios condutores.

"O que gera o campo elétrico do EEG não são cargas isoladas paradas; são correntes iônicas em fluxo contínuo saindo dos dendritos e retornando ao soma," continuou o professor. "O gerador fundamental é um dipolo de corrente, medido em Amperes-metro. Quando você aplica $V = (p \cos\theta) / (4\pi \sigma r^2)$ para um momento dipolar de cem nanoamperes-metro a três centímetros de distância, você obtém exatamente vinte e seis microvolts — a amplitude real do EEG."

O programador olhou para os vinte e seis microvolts calculados e para a equação no quadro. A física havia transformado um modelo fictício de milhares de volts em um instrumento de medição preciso.
