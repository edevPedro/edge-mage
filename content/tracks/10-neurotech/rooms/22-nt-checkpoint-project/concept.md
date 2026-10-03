# Conceito — Consolidação de Projeto e Arquitetura de Software em BCI

A consolidação de projetos em neurotecnologia requer uma separação modular limpa entre aquisição de hardware, estruturas de bufferização, filtragem de sinais e interface de controle.

## 1. As Três Fatias Típicas de Projeto
1. **Fatia de Aquisição e Streaming:** Gerador determinístico de sinais, buffer circular lock-free e protocolo de empacotamento com CRC.
2. **Fatia de DSP e Banco de Filtros:** Implementação de seções de segunda ordem (Biquad), filtros FIR/IIR causais e cálculo de potências de banda espectral.
3. **Fatia de Firmware e Baixa Potência:** Pipeline em microcontrolador com aritmética de ponto fixo Q15 e orçamento estrito de ciclos de clock.

## 2. O Artefato de Checkpoint de Projeto
O ritual exige a criação do artefato em `study-log/artifacts/checkpoint-project.md`, documentando a execução do emulador correspondente (`synth`, `artifact`, `cortex` ou `all`), a latência observada e as asserções de teste automatizado satisfeitas.

## 3. Modos de Falha na Prática de Engenharia
1. **Acoplamento Monolítico:** Escrever o código de captura de porta serial diretamente misturado com o algoritmo de machine learning, inviabilizando testes unitários automatizados.
2. **Dependência de Hardware Físico sem Mocks:** Não fornecer geradores de dados sintéticos determinísticos (emuladores), impedindo a integração contínua (CI) e a depuração de regressões algorítmicas.

## O Que a Próxima Sala Assume
A próxima sala (`nt-neuro-mage`) — **Boss Neuro Mage** — submete o candidato ao julgamento do Boss intermediário, auditando o domínio unificado dos três pilares neurais (aquisição, decodificação e tempo real).

## Artigos de Apoio e Leituras Recomendadas
- [OpenBCI Cyton](https://docs.openbci.com/GettingStarted/Boards/CytonGS/) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [SPEC Neurotech checkpoints](https://github.com/edevPedro/edge-mage/blob/main/docs/SPEC-neurotech-course.md) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
