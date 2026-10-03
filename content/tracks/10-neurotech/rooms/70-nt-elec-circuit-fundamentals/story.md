# História — O Divisor de Tensão que Esmagava o Sinal

Em um ensaio de bancada eletrônica, um desenvolvedor conecta um simulador de biopotenciais ajustado para emitir $50\ \mu\text{V}$ com impedância de saída de $50\text{ k}\Omega$ (simulando um eletrodo seco mal acoplado sobre a pele) à entrada de um amplificador analógico de testes.

Para sua frustração, o osciloscópio na saída registra apenas $25\ \mu\text{V}$ — metade exata da amplitude original do sinal.

O engenheiro sênior de hardware analisa as especificações da placa de testes e desenha o circuito equivalente no quadro:
— Você esqueceu de considerar a Lei de Ohm e a impedância de entrada do seu circuito ($R_{\text{in}}$) — ensina o sênior. — A interface entre o eletrodo e o amplificador forma um **divisor de tensão**:
$$V_{\text{medido}} = V_{\text{fonte}} \times \left( \frac{R_{\text{in}}}{R_{\text{fonte}} + R_{\text{in}}} \right)$$

Ele aponta para o esquemático da placa:
— A placa que você utilizou tem uma impedância de entrada de apenas $50\text{ k}\Omega$. Quando a impedância do eletrodo ($R_{\text{fonte}} = 50\text{ k}\Omega$) é igual à impedância do amplificador, a tensão medida é dividida exatamente por dois! Metade do sinal do cérebro é perdida no próprio contato da pele antes de qualquer processamento!

O engenheiro sênior explica o princípio de casamento de impedância de instrumentação:
— Para biopotenciais de microvolts, nunca buscamos casamento de potência conjugada ($R_{\text{in}} = R_S$); buscamos **transferência máxima de tensão**. Para que o erro do divisor seja inferior a $0.1\%$, a impedância de entrada do amplificador operacional deve ser pelo menos mil vezes maior do que a impedância de contato do eletrodo: $R_{\text{in}} > 1000 \times R_{\text{fonte}}$. Front-ends modernos utilizam transistores de efeito de campo CMOS/JFET com impedâncias de entrada na casa de gigaohms ($> 1\text{ G}\Omega$).

O desenvolvedor implementa a função `measured_voltage` para simular o efeito do divisor. Ao substituir a placa por um amplificador de alta impedância ($R_{\text{in}} = 1\text{ G}\Omega$), a tensão medida recupera $99.995\%$ de sua amplitude original.
