# História — A Tempestade de Sessenta Hertz

Em um laboratório de testes eletrofisiológicos, um desenvolvedor conecta um sistema de aquisição a um voluntário saudável em uma sala sem gaiola de Faraday. No osciloscópio digital, o canal $C3$ não mostra ondas cerebrais, mas sim uma onda senoidal colossal de $60\text{ Hz}$ com mais de $180\ \mu\text{V}$ pico a pico.

O desenvolvedor corre para o código do backend e insere um filtro notch IIR de segunda ordem para ceifar os $60\text{ Hz}$. Mas quando o voluntário move os olhos ou aperta a mandíbula, o filtro gera ringing transitório severo que contamina todas as outras frequências.

O engenheiro de hardware desliga o software e mede as impedâncias dos eletrodos: o eletrodo ativo $C3$ está perfeitamente acoplado a $5\text{ k}\Omega$, mas o eletrodo de referência no mastoide descolou parcialmente, atingindo $25\text{ k}\Omega$. O desbalanço de $20\text{ k}\Omega$ atua sobre o campo elétrico de modo comum da rede ambiente de $1\text{ V}$, transformando o modo comum em ruído diferencial puro que o amplificador de instrumentação amplifica legitimamente.

O desenvolvedor compreende que o problema não é de software: sem balanceamento de impedâncias ($\Delta Z \approx 0$) e altíssima impedância de entrada ($R_{\text{in}} \ge 10\text{ G}\Omega$), o ruído de modo comum destrói o sinal bioelétrico antes de qualquer processamento digital.
