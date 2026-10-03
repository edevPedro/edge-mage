# História — A Frequência Fantasma de Duzentos Hertz

Em um teste de bancada de um headset de BCI experimental conectado a um conversor analógico-digital operando a 250 Hz (frequência de Nyquist de 125 Hz), o desenvolvedor do pipeline de DSP observa um pico espectral misterioso em 50 Hz durante a análise de densidade de potência espectral via periodograma de Welch.

O time suspeita imediatamente de interferência da rede elétrica européia ou de aterramento precário. No entanto, o equipamento está funcionando inteiramente a bateria, desconectado de qualquer tomada AC.

O engenheiro de hardware traz o analisador de espectro de bancada e descobre que o regulador chaveado (DC-DC buck converter) que alimenta a interface Bluetooth na mesma placa está operando com ripple de comutação em 200 Hz. Sem um filtro analógico passa-baixas na entrada do ADC, a frequência de 200 Hz estava sendo rebatida pelo espelho de Nyquist: $|200 - 250| = 50\text{ Hz}$. O chaveamento do regulador virou um fantasma digital indistinguível das oscilações gama lentas.

O desenvolvedor aprende que o filtro anti-aliasing analógico antes do ADC não é opcional: ele calcula a atenuação necessária em 125 Hz e projeta um corte em 40 Hz, silenciando o ripple de alta frequência antes da amostragem digital.
