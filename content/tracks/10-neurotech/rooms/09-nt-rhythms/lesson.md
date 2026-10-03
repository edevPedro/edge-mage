# Lição — Ritmos e MI

## Objetivos

1. Escolher faixas alfa / mu / beta / gama o suficiente para dimensionar um filter-bank.
2. Associar MI a mudanças em ritmos **sensorimotores** (mu/beta), não a “ler pensamentos”.
3. Usar a convenção **ERD↓** deste curso sem confundir com “ativo = ↑ potência”.
4. Lembrar: EEG de escalpo mistura fontes (salas de física/volume).

## Passos

1. Desenhe a tabela de ritmos de memória; marque mu e beta como âncoras MI.
2. Dado `fs = 250 Hz`, qual a frequência de Nyquist? Qual banda mu ainda é legal?
3. Explique em 3 frases a diferença alfa occipital vs mu sensorimotor (mesma banda Hz ≠ mesma fonte).
4. Leia o abstract/figura de ERD em Pfurtscheller; anote o que o paper mede vs o que o synth gera.
5. Antes da Sala de filter-bank: escolha um banco toy `(8–12)` + `(16–24)` Hz e justifique.

Para destravar o lab, abra [Pfurtscheller & Lopes da Silva — Event-related EEG/MEG synchronization (review)](https://doi.org/10.1016/S1388-2457(99)00141-8) e leia a definição de ERD/ERS de Pfurtscheller e Lopes da Silva (queda de potência, não “ativo = sobe”) para o Lab B em C3.

## Labs

**Lab A (numeric).** `fs = 256`. Nyquist = ? Se alguém filtra 80–120 Hz “gama larga” sem antialias adequado, que risco aparece?

**Lab B (código mental).** Pseudo: `bandpower(x, fs, fmin, fmax)` → compare `fmin,fmax = (8,12)` vs `(13,30)` em C3 durante “left MI” synth. O sinal sintético pode inverter contrastes — documente honesty.

**Lab C.** Escreva uma frase de Methods: *“Features = log-bandpower mu/beta em C3/C4; ERD interpretado como redução relativa à baseline.”*

## Checklist

- [ ] ERD = ↓ potência (convenção curso) em MI mu/beta
- [ ] SMR ≠ mind-reading
- [ ] Synth ≠ fisiologia
- [ ] Pronto para escolher bandas no filter-bank
