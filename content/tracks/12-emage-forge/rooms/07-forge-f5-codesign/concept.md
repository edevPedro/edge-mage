# Conceito · Forge F5 — foundation before RTL/HLS

## Pré-requisitos

- Ponte de inferência (`pf-inference-bridge`) e preferência por evidência on-device
- Intro RTL/HLS lite na spine P7 (`pf-rtl-intro`, `pf-hls-lite`) — leia esses Estuda antes

## O que esta etapa ensina

Co-design não é “gerar Verilog mágico”. É perguntar: qual fatia do Forge ainda é memory-bound na CPU/GPU, e o que um acelerador pedagógico *poderia* fixar — com honestidade de que placa FPGA é opcional.

Se parar no portfólio sem silício, documente o “stop here” com critérios objetivos.
