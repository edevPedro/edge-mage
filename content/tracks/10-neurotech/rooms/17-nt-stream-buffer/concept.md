# Conceito — Streaming de Sinais Bioelétricos e Buffers Circulares (Ring Buffers)

O processamento online de sinais neurais opera sob um padrão assíncrono produtor-consumidor (Single-Producer Single-Consumer - SPSC): a aquisição de hardware gera amostras a uma taxa fixa, enquanto o pipeline de inferência processa janelas deslizantes em intervalos regulares.

## 1. A Estrutura do Buffer Circular
Um buffer circular é uma área de memória contígua de capacidade estática $N$ gerenciada por ponteiros de escrita (`head`) e leitura (`tail`):
- **Inserção (`push`):** Escreve a nova amostra em `buffer[head]` e avança `head = (head + 1) % N`. Se o buffer estiver cheio, sobrescreve a amostra mais antiga e avança `tail`.
- **Janelamento Deslizante:** Para decodificação contínua, o algoritmo extrai blocos de tamanho fixo $W$ (ex. 250 amostras) a cada salto de $S$ amostras (ex. 25 amostras = 100 ms).
- **Sem Alocação Dinâmica:** Como toda a memória é alocada na inicialização do sistema, elimina-se o risco de pausas por coleta de lixo e fragmentação de heap.

## 2. Unidades e Parâmetros Típicos
- **Taxa de amostragem ($f_s$):** $250\text{ Hz}$ (1 amostra a cada $4\text{ ms}$).
- **Comprimento da janela temporal ($W$):** $1.0\text{ s}$ ($250\text{ amostras}$).
- **Passo da janela deslizante (Hop/Step):** $100\text{ ms}$ ($25\text{ amostras}$).
- **Capacidade do ring buffer:** Tipicamente $2\times$ a $4\times$ o tamanho da janela para absorver variações temporais de processamento sem overrun.

## 3. Modos de Falha na Prática de Engenharia
1. **Buffer Overrun:** O algoritmo de inferência demora mais para processar do que o intervalo de novas amostras, forçando o ponteiro de escrita a atropelar o ponteiro de leitura e corrompendo a continuidade temporal do sinal.
2. **Buffer Underrun:** Tentar disparar a inferência antes que o buffer contenha o número mínimo de amostras para preencher a janela temporal, gerando predições com dados incompletos ou zeros residuais.

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-mcu-filter`) implementa a execução de filtros digitais sobre esses buffers dentro do ambiente restrito de um microcontrolador ARM Cortex-M.

## 5. Ponto de Destrave do Lab
Para o estudo de padrões de streaming de dados em tempo real e arquitetura SPSC lock-free em C/Python, consulte a documentação técnica do [Lab Streaming Layer (LSL)](https://labstreaminglayer.readthedocs.io/) e [OpenBCI Data Format](https://docs.openbci.com/).
