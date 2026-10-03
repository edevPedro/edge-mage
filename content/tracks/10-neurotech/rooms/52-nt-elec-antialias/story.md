# História — O Fantasma que Rebatia no Espelho

Na bancada de instrumentação de um novo protótipo de eletroencefalógrafo digital, um desenvolvedor conecta o sinal de saída de um pré-amplificador diretamente à entrada analógica de um conversor ADC amostrando a uma taxa fixa de 160 Hz. No monitor de espectro digital, o desenvolvedor identifica uma oscilação contínua e forte em exatamente 20 Hz.

— Temos um ritmo beta nítido em 20 Hz — comemora o novato.

O engenheiro sênior de hardware aproxima-se com um osciloscópio de bancada de alta frequência e conecta a ponta de prova diretamente no pino analógico de entrada do ADC:
— Olhe para o osciloscópio analógico — aponta o sênior. — Não existe nenhuma oscilação biológica em 20 Hz na entrada. O que existe é uma interferência eletromagnética espúria de 140 Hz induzida por uma fonte chaveada de computador próxima ao paciente.

O engenheiro sênior desenha o eixo de frequências de Nyquist no quadro:
— A sua taxa de amostragem é $f_s = 160\text{ Hz}$. Pelo Teorema de Nyquist-Shannon, a frequência máxima que o conversor pode representar sem ambiguidade é a frequência de Nyquist:
$$f_{\text{Nyquist}} = \frac{f_s}{2} = 80\text{ Hz}$$
Quando um sinal de frequência superior a Nyquist ($f_{\text{sinal}} = 140\text{ Hz}$) atinge o conversor analógico-digital sem filtragem analógica prévia, o processo de amostragem no tempo discretizado rebate essa frequência para dentro da banda base útil:
$$f_{\text{alias}} = |f_s - f_{\text{sinal}}| = |160 - 140| = 20\text{ Hz}$$

— O seu "ritmo beta de 20 Hz" é uma ilusão matemática destrutiva: é o fantasma rebatido do ruído de 140 Hz da fonte chaveada — alerta o sênior. — E o mais grave: uma vez que o sinal foi digitalizado com aliasing, é matematicamente impossível distinguir o sinal biológico autêntico do ruído rebatido por qualquer filtro digital subsequente! O filtro anti-aliasing deve ser posicionado **antes** do conversor, no domínio analógico.

A equipe instala um filtro analógico passa-baixas ativo de 4ª ordem antes do ADC (`check_aliasing`). O fantasma de 20 Hz desaparece, restabelecendo a fidelidade e a integridade da medição biológica.
