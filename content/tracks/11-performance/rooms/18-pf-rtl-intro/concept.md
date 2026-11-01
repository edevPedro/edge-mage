# Conceito — Digital logic e RTL lite

Co-design começa quando o requisito deixa de ser só “função C rápida” e vira **ciclos, largura de barramento e enables**.

## Comb vs seq

- **Combinacional**: saída é função imediata das entradas (cuidado com hazards/glitches conceituais).
- **Sequencial**: estado em registradores atualizado em borda de clock.

RTL (*Register Transfer Level*) descreve transfers entre registradores a cada ciclo — o nível em que você especifica um MAC, um FIFO ou um mini pipeline sem ainda falar de layout físico.

## Verilog lite (alfabetização)

Você precisa ler/escrever o suficiente para:

- Declarar `wire` vs armazenamento de estado.
- Um bloco sensível a clock com reset.
- Um testbench mental: estímulos → observar saídas → comparar com golden SW.

## Escopo honesto

Isto **não** é curso de ASIC/FPGA industrial completo. O boss Accelerator aceita RTL pedagógico, modelo de ciclos, ou HLS lite documentado — desde que haja baseline SW, evidência e testes funcionais. Tapeout e board bring-up ficam como gaps futuros (ver SPEC).
