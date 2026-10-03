# História — A Margem dos Vinte Por Cento

A sala limpa do laboratório de engenharia clínica recebia os testes finais de integração de um estimulador neural responsivo de malha fechada. O dispositivo operava com amostragem a 1000 Hz, o que impunha um deadline rígido inegociável de exatamente 1000 microssegundos para todo o ciclo: ler o ADC, filtrar o sinal, calcular a potência espectral e decidir se o pulso de estimulação terapêutica deveria ser disparado.

O desenvolvedor responsável pelo firmware apresentou com orgulho os dados de telemetria:

— "O tempo médio de execução do nosso pipeline é de 850 microssegundos. Ele cabe dentro dos 1000 microssegundos do deadline. Estamos prontos para fechar a versão final do firmware."

O engenheiro-chefe de sistemas de segurança crítica olhou para o gráfico e balançou a cabeça negativamente:

— "850 microssegundos para um prazo de 1000? Sua margem de segurança é de apenas 15%. Basta uma única variação térmica no cristal oscilador, uma rajada de interrupções de telemetria sem fio ou uma linha de cache não alinhada para seu tempo de processamento subir para 1020 microssegundos. Se isso acontecer, você perde a janela de amostragem, o buffer de entrada estoura e o pulso de estimulação é entregue na fase errada da oscilação cerebral."

Ele abriu a norma de engenharia de software de dispositivos médicos:

— "Em sistemas de tempo real rígido (*hard real-time*), nós exigimos uma margem de segurança (*headroom*) mínima estipulada em projeto — tipicamente pelo menos 20%. Isso significa que o pior tempo medido, inflacionado pela margem de 20%, ainda deve ser estritamente menor ou igual ao deadline estipulado:

$$t_{medido} \times \left(1 + \frac{\text{headroom}}{100}\right) \le t_{deadline}$$

Com 850 microssegundos e 20% de margem, o tempo projetado vai para 1020 microssegundos, o que viola o deadline de 1000. O firmware é inseguro. Se um processo leva 700 microssegundos, com 20% ele vai para 840, cabendo confortavelmente. Implemente essa verificação estrita antes de certificar qualquer pipeline para operação em malha fechada."
