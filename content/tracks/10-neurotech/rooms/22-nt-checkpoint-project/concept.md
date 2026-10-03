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

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-neuro-mage`) é o grande marco integrador (Boss intermediário), exigindo a comprovação de evidências de código e métricas para a conquista do título de Neuro Mage.

## 5. Ponto de Destrave do Lab
Consulte os padrões de arquitetura de software para biossinais no repositório de código aberto do [OpenBCI GitHub](https://github.com/OpenBCI) e a documentação do [Brainflow Library](https://brainflow.org/).
