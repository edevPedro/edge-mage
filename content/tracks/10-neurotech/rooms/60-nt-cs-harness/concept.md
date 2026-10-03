# Conceito — Harness de Testes, Reprodutibilidade e Integridade de Transporte

## 1. O Papel do Test Harness em Sistemas Neurais
Um *test harness* é um ambiente de execução controlado que submete pipelines de processamento a dados sintéticos conhecidos ou gravações canônicas com respostas de referência (*ground truth*) pré-estabelecidas.

Pilares de confiabilidade em software de neuroengenharia:
1. **Controle Estrito de Sementes (`seed`):** Todos os processos estocásticos (geração de ruído, inicialização de pesos, divisão de folds de validação cruzada) devem utilizar geradores pseudoaleatórios com sementes fixadas para permitir reprodução determinística bit-a-bit.
2. **Asserções Automatizadas (`assert`):** Verificações lógicas contínuas sobre invariantes de domínio (ex: amplitudes de EEG dentro de $\pm 500\ \mu\text{V}$, matrizes estritamente positivas definidas, latência de inferência abaixo do deadline).
3. **Detecção Imediata de Regressão:** Qualquer alteração no código que reduza a acurácia de referência ou estoure limites temporais deve falhar a suíte de testes de integração contínua (CI).

## 2. Integridade de Transporte e Numeração de Sequência
Em dispositivos físicos de aquisição eletrofisiológica (como OpenBCI, placas ADS1299 ou encoders BLE):
- Cada pacote de dados transmitido por UART, SPI ou Bluetooth contém um cabeçalho com um número de sequência inteiro de tamanho fixo (frequentemente 8 bits: $0\text{ a }255$).
- O contador é incrementado monotonicamente a cada amostra e reinicia em zero após atingir o valor máximo ($255 \to 0$).

## 3. Algoritmo de Detecção de Pacotes Perdidos (*Drop Detector*)
Dada uma sequência de contadores $[s_0, s_1, s_2, \dots, s_{k-1}]$ com módulo $M = max\_seq$:
Para cada par consecutivo $(s_i, s_{i+1})$, a diferença modular de passos decorridos é:

$$\Delta = (s_{i+1} - s_i) \pmod M$$

- Se $\Delta == 1$: Nenhum pacote foi perdido; a transmissão foi perfeita.
- Se $\Delta > 1$: Ocorreu a perda de $(\Delta - 1)$ pacotes.
- Se $\Delta == 0$: Pacote duplicado.

O total de pacotes perdidos em uma transmissão é o somatório de $(\Delta - 1)$ para todas as transições com $\Delta > 1$.

## 4. O Que a Próxima Sala Assume
A próxima sala (`nt-cs-realtime-testing`) estende a validação automatizada para a medição empírica de jitter e prazos rígidos de streaming.
