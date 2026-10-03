# Lição — Portal Neurotech

## Antes de qualquer Sala deste círculo

1. Confirme a ordem **Estuda → Sala**.
2. Distinga **offline** (replay) de **online** (latência importa).
3. Trate fontes humanas com **consentimento** e sem overclaim (próxima sala aprofunda Belmont).
4. Prefira dados **sintéticos** ou datasets abertos no MVP; hardware (ex. OpenBCI) é eletivo documentado.
5. Aceite a escala: este não é um “weekend course” — fundações→avançado + espinha + research pedem banda MSc-prep (**~180–300 h** guiadas).

## Checklist da 1ª sessão (30–45 min)

- [ ] `mage --course neurotech` abre sem erro.
- [ ] Li o SPEC §4 (phases/hours) e §6 (runas / ranks).
- [ ] Sei dizer em uma frase o que *não* é clínico neste círculo.
- [ ] Rodei `mage emu all` (ou li o que cada emulator ensina).
- [ ] Anotei: Estuda completo **antes** da primeira FLAG de decode.

## Mapa mental — o que vem depois do portal

1. **Ética** (`nt-ethics-consent`) — Belmont, consentimento, dual-use.
2. **Math×6** — do produto interno à intuição de CSP.
3. **Physics×5 + EE×5** — do dipolo ao LSB.
4. **Neuro×5** — HH → ritmos (âncora MI).
5. **CS×4** — complexidade, ringbuf, numerics, harness.
6. **Espinha** — filter-bank → MI → bandpower → decode → CV/stats.
7. **Online/FW** — stream, stub MCU, latency, closed-loop.
8. **Mage / apps / cases / research / Supremo**.

Para destravar o lab, abra [Singh et al. — MI-BCI review (Sensors 2021, PMC8003721)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8003721/) e leia o panorama do pipeline de MI e o que o review não autoriza como claim clínico, para fechar o parágrafo do lab sobre falhas concretas ao pular ética e fundação.

## Lab portal (leve)

Escreva um parágrafo (5–8 linhas) respondendo: *Se eu só fizer as salas de decode e pular math/EE/ética, que falhas concretas aparecem no meu relatório MSc?* (Ex.: overclaim; leak; SNR mal interpretado; κ sem chance level.)
