# Conceito — Neurônio e Hodgkin–Huxley (fundação)

## Mensagem central

O potencial de ação (AP) emerge de correntes iônicas (Na⁺, K⁺, …) na membrana. O modelo HH (1952) formaliza condutâncias e threshold. **EEG de escalpo não é um AP isolado**: é sincronia de grandes populações filtrada pelo volume condutor.

## HH pedagógico

| Ideia | Intuição |
|-------|----------|
| Capacitância de membrana | integra corrente → V |
| Canais Na | sobem V (upstroke) |
| Canais K | repolarizam |
| Threshold | ponto em que regeneração explode |

## Escala → BCI

Single-unit / patch ≠ feature do MVP. Ponte: HH → sinapse/PSP → LFP (`nt-spike-lfp`) → ritmos populacionais → eletrodo.

## Honesty

Não simulamos HH completo nesta Sala; fixamos o modelo mental e o limite de interpretação do EEG.

## Fonte

Hodgkin & Huxley DOI clássico (resources).

## Do HH ao eletrodo (cadeia)

```text
canais iônicos → AP → PSP sináptico → população → LFP → volume → escalpo µV → AFE
```

Cada seta perde informação espacial/temporal. Por isso MI usa ritmos populacionais, não spikes HH.

## O que memorizar para a Sala
- AP regenerativo Na/K
- EEG ≠ single-unit
- DOI HH como âncora histórica

## Limites do modelo HH no curso
- Sem geometria 3D de neurônio completo
- Sem redes HH acopladas
- Sem farmacologia

## Por que ainda é pilar
Sem excitabilidade, “ritmo” vira epifenômeno mágico. HH ancora a biofísica; ritmos/maps fecham o BCI.

## Síntese em 4 bullets
- Ensina o passo de Euler do LIF, v ← v + (dt/τ)(−(v − v_rest) + R I), e o modelo mental HH (Na/K e limiar) como fundação, não como EEG.
- A unidade é mV por passo de 1 ms (τ = 20 ms, R = 10): em −70 mV com I = 0 não há spike; em −56 mV com I = 10 o passo cruza −55 mV e a Sala devolve o reset.
- Honesty: não há HH completo nem geometria 3D; EEG de escalpo não é um potencial de ação isolado.
- A sala seguinte no order é `nt-neuro-synapse`.

