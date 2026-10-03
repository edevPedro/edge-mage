# Conceito — Semicondutores em Neurotecnologia: Diodos de Proteção ESD e Transistores de Entrada

Os semicondutores formam a base dos front-ends de biopotenciais modernos, operando como chaves de proteção e amplificadores de altíssima impedância.

## 1. Diodos de Grampeamento contra ESD (Clamping Diodes)
Descargas eletrostáticas (ESD) são surtos ultrarrápidos de tensão ($> 2\text{--}15\text{ kV}$) com tempos de subida de sub-nanossegundos.
O circuito de proteção canônico posiciona dois diodos em cada linha de sinal:
- **Diodo Superior:** Conecta o pino de sinal ao trilho positivo de alimentação $V_{\text{pos}}$. Se $V_{\text{in}} > V_{\text{pos}} + V_D$, o diodo entra em condução direta e grampeia a tensão em $V_{\text{pos}} + V_D$.
- **Diodo Inferior:** Conecta o pino de sinal ao trilho negativo de alimentação $V_{\text{neg}}$. Se $V_{\text{in}} < V_{\text{neg}} - V_D$, o diodo conduz e grampeia em $V_{\text{neg}} - V_D$.
- Onde $V_D \approx 0.3\text{ V}$ para diodos Schottky ou $0.7\text{ V}$ para diodos de silício de junção PN.

## 2. A Corrente de Fuga (Leakage Current)
O maior desafio ao escolher diodos de proteção para EEG é a **corrente de fuga reversa** ($I_{\text{leak}}$). Como os biopotenciais geram correntes ínfimas, se os diodos apresentarem fuga superior a alguns nanoamperes, essa corrente escorre através do eletrodo gerando offsets de tensão contínua gigantescos que saturam os amplificadores. Diodos de grau biomédico exigem $I_{\text{leak}} < 1\text{ pA}$.

## 3. Modos de Falha na Prática de Engenharia
1. **Omissão de Resistores de Limitação de Corrente em Série:** Colocar diodos de proteção sem um resistor em série ($R_{\text{series}} \approx 1\text{--}10\text{ k}\Omega$), permitindo que a corrente da descarga de ESD queime os próprios diodos de proteção por sobrecorrente térmica.
2. **Capacitância Parasita Excessiva:** Diodos com capacitância de junção alta ($C_j > 10\text{ pF}$) criam filtros passa-baixas indesejados e degradam o CMRR do sistema em alta frequência.

## O Que a Próxima Sala Assume
A próxima sala (`nt-electrode-snr`) — **Eletrodo, impedância, SNR** — analisa a interface eletroquímica eletrodo-gel-pele e o efeito de atenuação do divisor resistivo formado pela impedância de contato.

## Artigos de Apoio e Leituras Recomendadas
- [TI ADS1299 datasheet](https://www.ti.com/lit/ds/symlink/ads1299.pdf) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
