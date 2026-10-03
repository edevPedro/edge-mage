# Conceito — Interrupções de Baixa Latência, DMA e Double-Buffering (Ping-Pong)

## 1. O Custo Oculto de Interrupções por Amostra
Ao amostrar múltiplos canais em altas taxas (ex: $1\text{ kSPS}$ em 8 canais):
- Uma interrupção por amostra obriga a CPU a executar o empilhamento de registradores de hardware (*stack frame push* de R0-R3, R12, LR, PC, xPSR), desviar para a tabela vetorial de interrupções e desempilhar na saída.
- Em taxas elevadas, o tempo gasto em trocas de contexto (*overhead*) consome a maior parte do orçamento de processamento da CPU, introduzindo *jitter* estocástico na captura temporal e impedindo a execução de tarefas concorrentes (como transmissão sem fio).

## 2. Direct Memory Access (DMA) em Modo Circular
O controlador de DMA é um coprocessador dedicado exclusivamente à movimentação de dados entre periféricos (SPI, I2S, UART) e a memória RAM:
- Os dados transitam pelo barramento do sistema sem consumir um único ciclo de instrução do núcleo da CPU.
- Em modo circular, o DMA preenche um array de tamanho fixo $N$ (`full_size`) e, ao atingir o final, reinicia automaticamente no índice zero sem intervenção de software.

## 3. O Padrão Ping-Pong (Double Buffering)
Para permitir que o processador consuma dados continuamente enquanto o DMA grava novas amostras sem conflito de acesso concorrente:
1. Divide-se o buffer circular de tamanho $N$ em duas metades iguais:
   - **Buffer A (Ping):** Índices $[0, N/2 - 1]$
   - **Buffer B (Pong):** Índices $[N/2, N - 1]$
2. **Interrupção de Meia Transferência (Half Transfer - HT):**
   - Disparada quando o ponteiro de escrita do DMA cruza a marca de $N/2$ (`half_size`).
   - Sinaliza à aplicação que o Buffer Ping está completo e pode ser processado com segurança pela CPU enquanto o DMA continua preenchendo o Buffer Pong.
3. **Interrupção de Transferência Completa (Transfer Complete - TC):**
   - Disparada quando o ponteiro atinge o final $N$ e dá a volta para o início.
   - Sinaliza que o Buffer Pong está pronto para consumo enquanto o DMA volta a gravar no Buffer Ping.

## O Que a Próxima Sala Assume
A próxima sala (`nt-mcu-filter`) — **MCU pipeline stub (MA/FIR — não filter-bank MI)** — implementa filtragem digital em tempo real diretamente sobre buffers de amostras de microcontrolador.

## Artigos de Apoio e Leituras Recomendadas
- [ARM Cortex-M generic interrupt model (CMSIS docs hub)](https://www.keil.com/pack/doc/CMSIS/Core/html/index.html) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
