# Lição — BCI Competition IV case

## Objetivo

Usar Tangermann et al. (2012) como âncora para mapear **tasks / datasets / métricas** da Competition IV ao seu decode MVP — com CV e chance level honestos.

## Passos

1. Abra Tangermann et al. [10.1088/1741-2560/9/2/025009](https://doi.org/10.1088/1741-2560/9/2/025009) no protocolo de avaliação da BCI Competition IV (métrica e split, não o ranking): é esse resultado que o lab compara ao κ do MVP.
2. Liste ≥2 datasets/tarefas mencionados (nomes + paradigma em uma linha cada).
3. Para **uma** tarefa MI-like: escreva a métrica que *você* usaria no MVP (κ + `p_e`) e por quê.
4. Desenhe o fluxo: `dados → epochs → features → clf → métrica oficial vs sua métrica`.
5. Declare honesty: não é submissão à competição; é literacia de avaliação.

## Lab

**Entregável:**

- Tabela 4 colunas: Dataset/Task | Paradigma | Métrica (paper/challenge) | Analogia MVP
- 1 parágrafo: como um leak de trial destruiria a comparação justa numa competição
- 1 pergunta de journal club sobre generalização entre sujeitos

## Checklist

- [ ] DOI Tangermann citado
- [ ] Pelo menos 2 tasks nomeadas
- [ ] Métrica do MVP alinhada a κ/chance level
- [ ] Sem claim de “venci a Comp IV”
