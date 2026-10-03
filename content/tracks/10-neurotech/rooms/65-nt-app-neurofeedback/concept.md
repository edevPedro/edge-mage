# Conceito — Paradigma de Neurofeedback em Malha Fechada e Recompensa Retificada

## 1. O Laço de Neurofeedback (Closed-Loop BCI)
O neurofeedback consiste em um circuito cibernético de retroalimentação operante contínua:
1. **Aquisição:** O sinal de EEG é captado em tempo real sobre áreas corticais específicas (ex: $O1/O2$ para ritmo alfa occipital, ou $C3/C4$ para ritmo sensoriomotor).
2. **Extração de Característica:** A potência espectral da banda alvo ($P_{atual}$) é estimada em janelas deslizantes contínuas.
3. **Mapeamento de Feedback:** O desvio da potência em relação a uma linha de base calibrada ($P_{base}$) é convertido em reforço sensorial (tamanho de um círculo na tela, volume de uma música suave, pontuação de um jogo).
4. **Modulação Cognitiva:** O usuário utiliza estratégias mentais (relaxamento atencional, foco visual) para manter a potência acima do patamar alvo.

## 2. A Literatura Crítica de John Gruzelier
Conforme documentado nas revisões de Gruzelier (2014):
- O neurofeedback exige controles metodológicos estritos: grupos controle com feedback falso (*sham feedback*), protocolos duplo-cegos e validação estatística de transferência comportamental.
- Prescrever terapias clínicas sem respaldo médico homologado viola as diretrizes de ética biomédica. O escopo da engenharia é fornecer instrumentação e algoritmos de alta fidelidade e latência determinística.

## 3. Função de Recompensa Linear Retificada
Para treinar a autorregulação sem gerar confusão cognitiva, a função de recompensa deve ser monotônica crescente para valores acima da baseline e nula para valores inferiores (retificação de meia-onda):

$$\text{recompensa} = \max\left(0.0, (P_{atual} - P_{base}) \times \text{escala}\right)$$

- Se $P_{atual} > P_{base}$: O usuário recebe uma recompensa proporcional ao ganho acima da referência.
- Se $P_{atual} \le P_{base}$: O feedback é fixado em zero, evitando penalizações com valores negativos que violariam a dinâmica de condicionamento operante.

## 4. O Que a Próxima Sala Assume
A próxima sala (`nt-app-hybrid-p300`) analisa o paradigma do P300 Speller e potenciais evocados relacionados a eventos.
