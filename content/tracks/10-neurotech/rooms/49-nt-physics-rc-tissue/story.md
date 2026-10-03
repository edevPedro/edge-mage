# História — A Membrana como Filtro Passa-Baixas

Em um laboratório de biofísica tecidual, um engenheiro eletrônico conecta um gerador de funções de precisão a um modelo simulado de tecido biológico e membrana celular. Ele aplica uma onda quadrada perfeita de 1 kHz para testar a resposta transitória da instrumentação.

Ao observar a saída no osciloscópio, o engenheiro surpreende-se: a onda quadrada de bordas verticais desaparece, transformando-se em uma curva suave e arredondada, com subidas e descidas exponenciais lentas.

O biofísico da equipe senta-se ao lado do osciloscópio e desenha a bicamada lipídica no quadro:
— O tecido biológico vivo não se comporta como um resistor puro no domínio da frequência — ensina o biofísico. — A membrana celular é formada por uma bicamada de fosfolipídios com espessura de apenas 5 nanômetros, separando dois condutores iônicos aquosos (o citoplasma e o meio extracelular). Isso forma um capacitor elétrico biológico com capacitância típica de aproximadamente 1 microfarad por centímetro quadrado ($1\ \mu\text{F}/\text{cm}^2$).

Ele apresenta o modelo elétrico equivalente RC:
— A resistência do citoplasma e dos canais iônicos combinada com a capacitância transmembrana forma um filtro passa-baixas intrínseco de primeira ordem. A constante de tempo biofísica $\tau = R C$ impõe uma frequência de corte natural:
$$f_c = \frac{1}{2\pi R C}$$

O biofísico calcula: para uma resistência intracelular e de meio na faixa de $10\text{ k}\Omega$ e capacitância de $1\ \mu\text{F}$, a frequência de corte situa-se na casa de $15.9\text{ Hz}$.

— É por essa razão biofísica que variações ultrarrápidas de biopotenciais são naturalmente integradas e atenuadas pelo próprio tecido cerebral antes mesmo de atingirem os eletrodos de escalpo — conclui o pesquisador.

O engenheiro implementa a rotina de corte RC (`rc_cutoff`). A compreensão da constante de tempo tecidual fundamenta o projeto dos amplificadores e explica por que os ritmos de EEG residem predominantemente abaixo de 40 Hz.
