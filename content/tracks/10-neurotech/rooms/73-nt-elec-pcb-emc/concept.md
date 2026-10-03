# Conceito — Roteamento de PCB, Compatibilidade Eletromagnética (EMC) e Loops de Indução

O layout físico de circuitos impressos para biopotenciais de microvolts exige controle rigoroso de acoplamento capacitivo e indutivo.

## 1. A Lei de Faraday e a Área de Loop
Qualquer laço condutor de área $A$ (em $\text{m}^2$) exposto a um campo magnético alternado perpendicular $B(t) = B_0 \sin(2\pi f t)$ desenvolve uma tensão induzida de ruído:
$$V_{\text{ind}} = -\frac{d\Phi_B}{dt} = 2\pi f B_0 A \cos(2\pi f t)$$
Com amplitude de pico:
$$V_{\text{pico}} = 2\pi f B_0 A$$
- **Minimização de Área:** Reduzir a área de loop aproximando o traço de sinal do seu plano de retorno de terra imediato é a medida mais eficaz contra interferência magnética.

## 2. Stackup de PCB para Biopotenciais (4 Camadas Canônicas)
Um arranjo recomendado de camadas em neurotecnologia:
- **Layer 1 (Top - Componentes e Sinais Analógicos Sensíveis):** Trilhas curtas e diretas dos eletrodos.
- **Layer 2 (Inner 1 - Plano de Terra Sólido / Ground Plane):** Blindagem eletrostática e caminho de retorno de baixa indutância.
- **Layer 3 (Inner 2 - Plano de Alimentação / Power Plane):** Distribuição de energia desacoplada.
- **Layer 4 (Bottom - Sinais Digitais e SPI):** Roteamento de relógio e controle digital separado do topo analógico.

## 3. Modos de Falha na Prática de Engenharia
1. **Corte no Plano de Terra (Split Ground Plane):** Criar uma fenda no plano de terra sob trilhas rápidas, forçando as correntes de retorno a percorrerem um laço gigantesco ao redor da fenda.
2. **Roteamento Paralelo de Sinais Digitais e Analógicos:** Rotear o barramento SPI de alta velocidade paralelamente às trilhas de eletrodo por vários centímetros, injetando ruído de clock por acoplamento capacitivo mútuo.

## O Que a Próxima Sala Assume
A próxima sala (`nt-elec-shield-power`) — **Elétrica — Shielding, layout µV e power integrity** — aborda a blindagem eletrostática ativa (driven shield) e a rejeição de ruído de fonte de alimentação (PSRR).

## Artigos de Apoio e Leituras Recomendadas
- [TI ADS1299 datasheet](https://www.ti.com/lit/ds/symlink/ads1299.pdf) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
