# História — O Divisor que Comeu o Ritmo Mu

Em uma bancada de eletrônica analógica, um programador de sistemas tenta integrar um amplificador operacional genérico de bancada a um par de eletrodos de escalpo $\text{Ag/AgCl}$ aplicados sobre a região sensoriomotora ($C3$). O amplificador de teste possui uma especificação de impedância de entrada nominal de $1\text{ M}\Omega$, perfeitamente adequada para sensores industriais ou circuitos de áudio.

Após preparar a pele com pasta abrasiva e gel eletrolítico, a medição de impedância de contato registra $50\text{ k}\Omega$ no eletrodo ativo. Ao inicializar a aquisição, o programador nota que os ritmos mu de $10\text{ Hz}$, que deveriam apresentar picos claros de $15\ \mu\text{V}$, aparecem atenuados e afogados em ruído térmico.

O engenheiro de hardware aponta o diagrama esquemático: a impedância de contato de $50\text{ k}\Omega$ e a entrada do amplificador de $1\text{ M}\Omega$ formam um divisor de tensão passivo. Uma fração de quase $5\%$ da tensão bioelétrica é perdida de imediato na interface. Mais crítico ainda: qualquer leve oscilação na pressão do eletrodo altera a impedância de contato em $\pm 10\text{ k}\Omega$, modulando o sinal em quase $1\%$, criando um ruído dinâmico que destrói a calibração do decodificador.

O desenvolvedor é instruído a auditar a folha de dados do AFE dedicado (ADS1299): com entradas CMOS de $1\text{ G}\Omega$, a perda pelo divisor colapsa para menos de $0.005\%$, garantindo a integridade dos microvolts cerebrais.
