# História — A Ilusão do Filtro Perfeito

No laboratório de decodificação neural, uma desenvolvedora comemorava um marco no pipeline de processamento de sinais de EEG: sua rotina de filtragem offline para isolar o ritmo mu de dez hertz entregava curvas suaves, sem qualquer distorção de fase. Os classificadores treinados nos dados filtrados alcançavam noventa por cento de acurácia.

"O código está pronto para ser transferido para o firmware do estimulador em tempo real," disse ela ao líder técnico da bancada.

O líder olhou para o script Python e apontou para uma única linha de código: `scipy.signal.filtfilt(b, a, raw_eeg)`.

"O que essa função faz exatamente sob o capô?" perguntou ele.

"Ela passa o filtro IIR no sentido direto e depois passa novamente de trás para a frente para zerar o deslocamento de fase," explicou a desenvolvedora.

"Exatamente," respondeu o líder técnico. "Para filtrar de trás para a frente, ela precisa saber como o sinal vai se comportar daqui a dez segundos no futuro. Quando o sinal vem do conversor analógico-digital em tempo real amostra por amostra, você não tem as amostras futuras. Se você tentar aplicar isso em uma fila de streaming, você precisa acumular buffers enormes, gerando um atraso inaceitável."

A desenvolvedora tentou então substituir por um filtro FIR simétrico de alta ordem, com cento e vinte e nove coeficientes para manter a fase linear. O líder pediu para ela calcular o atraso de grupo: $(129 - 1) / (2 \times 250) = 256$ milissegundos.

"Duzentos e cinquenta e seis milissegundos apenas de atraso no filtro," observou ele. "O córtex humano perde a sensação de agência motora se o feedback visual demorar mais de cem milissegundos no total. Seu filtro consome mais do que o dobro do orçamento total do sistema."

A solução era implementar uma seção biquad IIR causal de segunda ordem via Transformada Bilinear com pré-deformação de frequência, auditando rigorosamente os polos da equação característica para garantir que permanecessem dentro do círculo unitário. O atraso caiu para doze milissegundos, salvando a malha fechada.
