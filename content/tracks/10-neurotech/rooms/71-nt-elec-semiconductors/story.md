# História — A Fuga Invisível dos Diodos

Durante a fase de testes de certificação de imunidade eletrostática de um novo amplificador de EEG vestível, o protótipo anterior havia falhado miseravelmente: uma descarga de quatro mil volts aplicada ao cabo do eletrodo fritou os canais analógicos do processador.

Para a segunda revisão da placa, o desenvolvedor de hardware tomou uma medida radical: soldou pares de diodos de proteção rápida nos pinos de todos os oito canais, interligando-os aos trilhos de três volts e terra.

"Agora o hardware aguenta até raio," comemorou ele na reunião de alinhamento. "Coloquei diodos Schottky ultra-rápidos em cada pino para grampear qualquer pico acima de zero vírgula três volts."

No dia seguinte, porém, o desenvolvedor de firmware não conseguia registrar nenhum sinal cerebral. Nos oito canais, os conversores analógico-digitais de vinte e quatro bits retornavam leituras estáticas coladas no valor máximo da escala de saturação.

A arquiteta de instrumentação biomédica do laboratório pegou o multímetro e mediu a tensão DC diretamente nos eletrodos colocados na cabeça de um voluntário. O voltímetro acusava mais de um milivolt de tensão contínua fixa.

"Você olhou a corrente de fuga reversa desses diodos Schottky no datasheet?" perguntou ela, abrindo o gráfico de temperatura do semicondutor. "Esses diodos foram projetados para fontes de alimentação chaveadas. A fuga reversa deles é de vinte nanoamperes. Quando essa corrente flui pelos cinquenta quilo-ohms da resistência de contato da pele do sujeito, a lei de Ohm gera uma queda de tensão DC de exatamente um milivolt — mil microvolts."

O projetista arregalou os olhos. Um sinal de EEG tinha apenas dez microvolts.

"Com um ganho analógico de vinte e quatro vezes, um milivolt de offset vira vinte e quatro milivolts," continuou a engenheira. "Se o seu ganho for de cem vezes, vira cem milivolts. Seus amplificadores estão saturados pela própria proteção que você colocou. Em biopotenciais de microvolts, você não pode usar diodos comuns de potência; você precisa de diodos de silício de fuga ultra-baixa com corrente na casa de picoamperes."
