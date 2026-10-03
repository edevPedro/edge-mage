# Lição — Ring buffer para EEG online

## Objetivos

Implementar mentalmente push/latest; detectar underrun; ligar ao online stub.

## Passos

1. Desenhe buffer N=1024, head/tail.
2. `fs=250`: quantas samples em 100 ms?
3. Defina política: drop oldest vs block on full.
4. Escreva pseudo `latest(W)` thread-safe (lock ou single-writer).
5. Rode `mage emu` / online path e anote se há underrun simulado.

Para destravar o lab, abra [LSL — Lab Streaming Layer docs](https://labstreaminglayer.readthedocs.io/) e leia o modelo de stream contínuo do LSL (chunk versus amostra) para implementar latest(n) no ring sem inventar amostra que não está no anel.

## Labs

**Numeric.** Hop=40 ms, feature+clf=25 ms médio, 55 ms p95 — quantos % de deadlines falham se deadline=40 ms? (qualitativo: p95 estoura).

**Code mental.**

```text
on_sample(x):
  buf.push(x)
  if due_for_window():
    X = buf.latest(W)
    y = decide(X)   # budget!
    log(y, t)
```

## Checklist

- [ ] push / latest
- [ ] underrun definido
- [ ] Pronto para latency + online stub

## Caderno (domínio)

Escreva 1 página: (1) diagrama desta sala, (2) 3 números com unidade, (3) honesty note, (4) ligação à sala anterior e seguinte do PEDAGOGICAL path. Isto conta como Estuda completo antes da Sala.
