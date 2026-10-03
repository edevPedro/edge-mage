# Conceito — Semicondutores, Proteção ESD e Corrente de Fuga no AFE

## 1. O Papel dos Semicondutores no Front-End Analógico
Em sistemas de biopotenciais (EEG/EMG/ECG), os dispositivos semicondutores operam em funções críticas de proteção e condicionamento de sinal:

| Componente | Mecanismo Físico | Função no Bioamplificador |
|---|---|---|
| **Diodo de Junção PN** | Barreira de potencial e condução unidirecional | Clamping de sobretensão e proteção contra descargas eletrostáticas (ESD) |
| **MOSFET de Canal N/P** | Modulação de condutância de canal por campo elétrico no gate | Chaves analógicas de multiplexação de canais e buffers de entrada CMOS |
| **Ponto de Polarização (Bias DC)** | Fixação do ponto de repouso na região linear | Garantir que o sinal de microvolts oscile longe da saturação dos trilhos |

### O Dilema Entre Proteção ESD e Corrente de Fuga
O corpo humano acumulando eletricidade estática ao caminhar sobre carpete pode descarregar potenciais de até $\pm 8000\text{ V}$. Os gates de óxido de silício dos transistores CMOS na entrada de circuitos integrados como o [TI ADS1299](https://www.ti.com/lit/ds/symlink/ads1299.pdf) rompem com tensões acima de $\pm 10\text{--}15\text{ V}$.

Para evitar a destruição do chip, redes de diodos de clamp conectam cada pino de entrada aos trilhos de alimentação $V_{DD}$ e $V_{SS}$:
- Se $V_{\text{in}} > V_{DD} + V_{\text{diodo}}$: o diodo superior conduz, desviando a corrente da descarga para a fonte.
- Se $V_{\text{in}} < V_{SS} - V_{\text{diodo}}$: o diodo inferior conduz, desviando a corrente para o terra.

Contudo, diodos semicondutores sob polarização reversa apresentam uma **corrente de fuga reversa** ($I_{\text{leak}}$). Essa corrente é forçada a circular pela impedância de contato da pele $R_{\text{pele}}$ do eletrodo para fechar o circuito:

$$V_{\text{offset}} = I_{\text{leak}} \times R_{\text{pele}}$$

- **Entrada Integrada de Baixa Fuga (TI ADS1299)**:
  Com arquitetura CMOS customizada para eletrofisiologia, a corrente de fuga é de apenas $I_{\text{leak}} \approx 0.2\text{ nA} = 200\text{ pA}$.
  Com eletrodo úmido ($R_{\text{pele}} = 10\text{ k}\Omega$):
  $$V_{\text{offset}} = (0.2 \times 10^{-9}\ \text{A}) \times (10 \times 10^3\ \Omega) = 2.0\ \mu\text{V}$$
  O offset DC introduzido é de apenas $2\ \mu\text{V}$, perfeitamente tolerável pela faixa dinâmica de entrada.
- **Proteção Discreta Mal Dimensionada (Diodos Schottky Comuns)**:
  Diodos comerciais discretos frequentemente possuem correntes de fuga reversa de $I_{\text{leak}} \approx 20\text{ nA}$ a temperatura ambiente.
  Com um eletrodo seco ($R_{\text{pele}} = 50\text{ k}\Omega$):
  $$V_{\text{offset}} = (20 \times 10^{-9}\ \text{A}) \times (50 \times 10^3\ \Omega) = 1.0\text{ mV} = 1000\ \mu\text{V}$$
  Um offset de $1000\ \mu\text{V}$ é cem vezes maior do que o próprio sinal de EEG ($10\ \mu\text{V}$), causando saturação imediata dos amplificadores operacionais seguintes ou esgotamento da faixa de conversão analógico-digital.

## 2. Modos de Falha Operacionais
1. **Adicionar Diodos TVS Genéricos sem Ler a Corrente de Fuga**: Tentar proteger entradas de eletrodos soldando diodos TVS de barramento digital de alta velocidade (onde fugas de microamperes são aceitáveis). No EEG, uma fuga de $1\ \mu\text{A}$ em $10\text{ k}\Omega$ gera $10\text{ mV}$ de offset DC, destruindo a leitura bioelétrica.
2. **Deixar Entradas de Alta Impedância Flutuantes (Floating Inputs)**: Operar um canal de EEG sem qualquer referência de bias DC. Sem um caminho de retorno para as correntes de polarização de gate dos transistores MOSFET, a carga eletrostática acumula-se no capacitor de entrada e a voltagem do pino sobe até colidir com o trilho de alimentação.

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-electrode-snr`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/06-nt-electrode-snr/room.yaml)) assume que você entende como a resistência de contato e o offset DC gerado por semicondutores interagem com a tensão de meia-célula eletroquímica da interface prata/cloreto de prata.
