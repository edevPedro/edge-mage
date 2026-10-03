# Conceito — Online stub (janela → label → log)

## Loop

```text
window = buffer.latest(W)
feat = features(window)
label = clf(feat)          # ou policy
log(timestamp, label, latency_ms)
```

Deadline: se `latency > budget`, conta **miss** (liga `nt-latency-budget`).

## Emulator

`online_loop` / `mage emu online` — ensina a estrutura. Não é BCI clínico; não há sujeito.

## Runa

`rune-neuro-online` tipicamente desta sala (SPEC).

## Honesty

Offline κ alto ≠ online estável (jitter, underrun, concept drift).

## Contadores

- `n_windows`
- `n_deadline_miss`
- `p95_latency_ms`

Passe a Sala se o emulator reporta coerência com o budget da task numérica.

## Transição offline→online
Reutilize o *mesmo* vetor de features do MVP; mude só a origem das janelas (arquivo → ringbuf). Evita “dois pipelines”.

## Sense / decide / act (online)

Mesmo no stub educacional:
1. **Sense** — ler janela do ringbuf
2. **Decide** — features + clf (ou threshold de banda)
3. **Act** — log / comando simulado / feedback visual toy

Se decide>budget, act atrasa e o usuário (mesmo sintético) vê feedback velho — closed-loop sofre (`nt-closed-loop-control`).

## Contrato com offline
Salve `clf` treinado offline; online só infere. Retreinar online sem protocolo = outro projeto (pesquisa).

## Falhas a instrumentar
timeout; exception em feature NaN; clock rewind; buffer resize errado. Cada uma vira teste em `nt-cs-realtime-testing`.

## Síntese em 4 bullets
- Ensina o loop operacional janela → feature → label → log, com miss quando a latência passa do budget.
- O número a carregar é a latência em ms: 25 amostras a 250 Hz duram 100 ms; `sliding_windows` com janela 250 e hop 50 abre em (0, 250), (50, 300) e (100, 350).
- Honesty: κ offline alto não é online estável; o stub não tem sujeito e não cobre jitter, underrun nem concept drift.
- A sala seguinte no order é `nt-closed-loop-control`.

