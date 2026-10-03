# Conceito — Benchmarking Padronizado, BCI Competition IV e Matriz de Confusão

## 1. O Legado da BCI Competition IV (Tangermann et al., 2012)
As quatro edições da BCI Competition (2000 a 2012) formaram a espinha dorsal de validação algorítmica da neuroengenharia moderna:
- **Padronização:** Forneceu conjuntos de dados abertos e amplamente documentados (como os datasets de Graz de 4 classes de imagética motora: mão esquerda, mão direita, pés e língua).
- **Separação Rígida:** Os dados de calibração continham rótulos para treinamento, enquanto os dados de teste tinham os rótulos retidos pelos organizadores para avaliação cega (*blind evaluation*).
- **Métrica Oficial:** Adoção de métricas ajustadas ao acaso, como o Coeficiente Kappa de Cohen ($\kappa$), para penalizar classificadores desbalanceados ou triviais.

## 2. A Estrutura da Matriz de Confusão Binária
Para avaliar formalmente as predições de um modelo supervisionado contra o gabarito verdadeiro (*ground truth*):
Sejam $y_{true} \in \{0, 1\}$ os rótulos reais e $y_{pred} \in \{0, 1\}$ as predições geradas:

| | Predito = 1 | Predito = 0 |
| :--- | :--- | :--- |
| **Real = 1** | **Verdadeiro Positivo (TP)** | **Falso Negativo (FN)** |
| **Real = 0** | **Falso Positivo (FP)** | **Verdadeiro Negativo (TN)** |

### Contagens Fundamentais:
- **Verdadeiro Positivo (TP):** $y_{true} == 1$ e $y_{pred} == 1$.
- **Falso Negativo (FN):** $y_{true} == 1$ e $y_{pred} == 0$ (o modelo errou por omissão).
- **Falso Positivo (FP):** $y_{true} == 0$ e $y_{pred} == 1$ (o modelo errou por falso alarme).
- **Verdadeiro Negativo (TN):** $y_{true} == 0$ e $y_{pred} == 0$.

## 3. Honestidade Intelectual em Benchmarks Públicos
- Reproduzir um pipeline sobre dados sintéticos ou dados públicos abertos é uma emulação didática (*reproduction lite*).
- É terminantemente vedado reivindicar colocações oficiais em leaderboards ou superar concorrentes históricos sem submeter-se ao protocolo original de avaliação cega em tempo real.

## O Que a Próxima Sala Assume
A próxima sala (`nt-irb-protocol`) — **IRB e protocolo ético (literacy)** — estrutura a submissão formal a comitês de ética em pesquisa e conformidade regulatória para ensaios clínicos.

## Artigos de Apoio e Leituras Recomendadas
- [Tangermann et al. 2012 BCI Competition IV review](https://doi.org/10.1088/1741-2560/9/2/025009) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
