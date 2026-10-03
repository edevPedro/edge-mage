# Conceito — Stream buffer / ring buffer online

## Ideia

Offline lê o arquivo inteiro. Online consome um **fluxo**: amostras chegam, janelas saem, decisões têm deadline. A estrutura pedagoógica é o **ring buffer** (circular) de tamanho fixo.

## Operações

| Op | Semântica |
|----|-----------|
| `push(x)` | escreve no head; avança; pode sobrescrever oldest |
| `latest(n)` | lê as n amostras mais recentes (janela) |
| underrun | consumer pediu o que ainda não chegou |
| overrun | producer encheu e perdeu amostra (política) |

## Ligação ao emulador

`synth_eeg_stream` / modo online simulado processa **chunks com tempo** — não o dataset de uma vez. Pseudo-LSL: pense em “amostras/s”, não em “ficheiro”.

## Orçamento

Se `fs=250` e janela W=500 amostras (2 s) com hop H=50 (0,2 s), o consumer deve terminar o path feature→label em ≪ hop, senão acumula atraso (liga `nt-latency-budget`, `nt-cs-realtime-testing`).

## Honesty

Ringbuf no host ensina a API mental; no MCU real há ISR/DMA (`nt-fw-irq-dma`, `nt-fw-rt-constraints`). Stub ≠ QEMU.

## Diagrama mental

```text
ADC/synth ──push──▶ [ ring N ] ──latest(W)──▶ feature ▶ clf ▶ log
                         ▲ underrun se vazio
                         ▼ overrun se cheio (drop/block)
```

## Pseudo-LSL
Pense em stream com timestamps monotônicos. O TUI não exige LSL real; a metáfora basta para online stub.

## Exercício de sizing
N ≥ W + margem. Se hop=H amostras, consumer budget ≪ H/fs segundos. Documente N, W, H, fs no caderno.

## Políticas de overflow
1. **Drop oldest** — privilegiar frescor (comum em BCI online)
2. **Drop newest** — raro
3. **Block producer** — pode atrasar aquisição

Escolha e documente. No stub, drop oldest + contador de overrun.

## Teste unitário mínimo
push N+10 em buffer N; assert len==N; latest(W) shape correto; underrun flag se W>len.

