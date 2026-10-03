# História — A Capacitância Oculta da Membrana

No laboratório de biofísica computacional, dois pesquisadores discutiam a simulação de um circuito equivalente de neurônio piramidal. Um programador recém-chegado do desenvolvimento web havia implementado um modelo estático de condutância usando apenas a lei de Ohm: resistências em série e paralelo representando o meio intracelular, a membrana e o fluido intersticial.

"O código roda em menos de um milissegundo por passo temporal," dizia o programador, "mas quando injeto pulsos de alta frequência de um quilohertz simulando disparos axônicos rápidos, o potencial se propaga pela árvore dendrítica inteira quase sem perda de amplitude. Os biólogos disseram que o modelo está errado."

A física responsável pelo laboratório sentou-se ao lado dele no terminal e abriu o arquivo de constantes biofísicas.

"Você tratou a membrana celular como uma resistência pura de mil ohms," apontou ela. "Mas uma membrana biológica é uma bicamada lipídica isolante de quatro nanômetros de espessura cercada por soluções eletrolíticas salinas. Isso é a definição exata de um capacitor de placas paralelas. A capacitância específica é de cerca de um microfarad por centímetro quadrado."

Ela pediu para ele calcular a frequência de corte $f_c = 1 / (2\pi R C)$. Para uma resistência de membrana de mil ohms e capacitância equivalente de dez microfarads, a constante de tempo $\tau = R C$ resultava em dez milissegundos — uma frequência de corte de aproximadamente 15,9 hertz.

"Agora veja a reatância capacitiva a um quilohertz," instruiu ela. O programador calculou e viu que $|H(1000\text{ Hz})|$ despencava para menos de 0,02, sofrendo uma perda superior a 35 decibéis. A capacitância da membrana agia como um curto-circuito para correntes de alta frequência, drenando-as antes que pudessem carregar a árvore dendrítica.

"A própria biologia da membrana é um filtro passa-baixa," concluiu o programador, finalmente entendendo. "Se você ignora o capacitor, você não está modelando tecido vivo; está modelando um resistor de carbono."
