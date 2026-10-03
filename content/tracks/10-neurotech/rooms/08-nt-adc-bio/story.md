# História — Os Dez Microvolts Engolidos pelo Conversor

Em um projeto de BCI experimental de baixo custo, um desenvolvedor decide conectar a saída de uma montagem de eletrodos diretamente aos pinos de entrada analógica de um microcontrolador comum de 32 bits, sem utilizar um chip de front-end analógico especializado. Ele configura o conversor analógico-digital para operar com 12 bits de resolução e referência interna de $3.3\text{ V}$.

O código em C lê o registrador periférico via interrupção a 250 Hz e transmite os inteiros para um dashboard web. No entanto, o gráfico de onda exibe uma linha perfeitamente reta com pequenos saltos aleatórios que não respondem a nenhuma tentativa de modulação sensorial ou fechamento de olhos.

O engenheiro de hardware realiza o cálculo na lousa: para 12 bits bipolares em $3.3\text{ V}$, o menor bit significativo (LSB) corresponde a impressionantes $1611\ \mu\text{V}$ ($1.61\text{ mV}$). Um biopotencial de escalpo humano, oscilando entre $10\ \mu\text{V}$ e $20\ \mu\text{V}$, precisaria crescer cento e sessenta vezes para alterar um único bit do conversor! O sinal biológico estava afogado na cegueira do degrau de quantização.

O time substitui a arquitetura por um ADC delta-sigma de 24 bits com PGA interno de $24\times$: o LSB cai imediatamente para $0.012\ \mu\text{V}$, revelando a dinâmica microvoltica das ondas cerebrais com mais de oitocentos níveis de quantização por oscilação.
