# Conceito — Arquitetura AArch64, Instruções SIMD Neon e Stubs de Prototipagem

## 1. O Papel dos Stubs Didáticos vs. Silício de Produção
No desenvolvimento de produtos de neurotecnologia:
- **Ambiente de Prototipagem (Host):** Linguagens de alto nível (Python, C++) executadas em computadores de desenvolvimento permitem rápida iteração algorítmica, verificação estatística e criação de harnesses de teste. O `cortex_m_stub` ou módulos de simulação didática deste curso servem para fixar o modelo mental de registradores e fluxo de dados sem a complexidade de compilação cruzada ou configuração de emuladores ciclo-acurados (como QEMU).
- **Ambiente de Borda (Target Edge):** Microcontroladores ARM Cortex-M e microprocessadores ARM AArch64 (Cortex-A53, A72) exigem execução nativa de baixo nível para respeitar deadlines rigorosos de tempo real com eficiência energética milimétrica.

## 2. Acelerando Álgebra Linear com SIMD Neon (AArch64)
Em tarefas de decodificação neural (como projeção de Common Spatial Patterns ou filtros de média móvel espacial):
- Em processamento escalar convencional (SISD):
  $$y = \sum_{i=0}^{3} a_i \cdot b_i = a_0 b_0 + a_1 b_1 + a_2 b_2 + a_3 b_3$$
  O processador executa quatro instruções de multiplicação e três instruções de soma sequencialmente.
- Em arquitetura vetorial SIMD Neon (128 bits):
  - Um registrador Neon de 128 bits armazena um vetor de quatro floats de 32 bits (`float32x4_t`).
  - O hardware multiplica as 4 vias (*lanes*) em paralelo em um único ciclo de clock:
    $$[a_0, a_1, a_2, a_3] \odot [b_0, b_1, b_2, b_3] = [a_0 b_0, a_1 b_1, a_2 b_2, a_3 b_3]$$
  - Uma instrução de redução horizontal ou acumulação soma os quatro produtos, entregando o resultado final com aceleração de até $4\times$.

## 3. A Checklist da Ponte Embedded
Ao transitar um algoritmo validado em notebook para um dispositivo embarcado:
1. Validar se os tipos de dados float32 não sofrem perda de precisão frente a float64.
2. Garantir alinhamento de memória em múltiplos de 16 bytes (128 bits) para evitar falhas de barramento nas cargas vetoriais (`LDP`/`STP`).
3. Declarar explicitamente as limitações do modelo de simulação do host antes da integração em bancada física.

## O Que a Próxima Sala Assume
A próxima sala (`nt-fw-rt-constraints`) — **Firmware — Restrições realtime e buffers** — audita prazos rígidos de interrupções e calcula a margem de segurança temporal (headroom) do firmware.

## Artigos de Apoio e Leituras Recomendadas
- [edge-mage Edge AI track](https://github.com/edevPedro/edge-mage/blob/main/content/tracks/07-edge-ai/README.md) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
