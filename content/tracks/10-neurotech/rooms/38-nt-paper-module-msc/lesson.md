# Lição — Módulo de Artigo Científico Padrão Mestrado (Paper Module MSc)

## 1. O Padrão de Análise de Manuscrito Indexado
1. **Identificador Persistente**:
   O artigo selecionado deve obrigatoriamente possuir um identificador digital oficial (DOI) indexado e permanente.
2. **Reprodução Paramétrica**:
   A replicação de resultados deve comparar a métrica reportada com a métrica obtida pelo pipeline do aluno, declarando a variação:
   $$\Delta = \text{Métrica}_{\text{reproduzida}} - \text{Métrica}_{\text{reportada}}$$
   E verificando se $|\Delta| \le \text{tolerância}$ (tipicamente $\pm 0.05$).
3. **Crítica Metodológica e Limites**:
   Identificar suposições implícitas dos autores (estacionariedade do sinal, tempos de calibração, latência em microcontroladores).

## 2. A Função de Laboratório
- `verify_paper_reproduction(reported_metric, reproduced_metric, tolerance)`: Verifica se a reprodução empírica confirma os dados do artigo dentro da margem de tolerância declarada.

Para destravar o lab, abra [Barachant et al. DOI](https://doi.org/10.1109/TBME.2011.2172210) e leia o resultado geométrico de Barachant (distância em SPD versus euclidiana) para o módulo citar figura ou Methods sem dizer que o toy reproduz o paper.
