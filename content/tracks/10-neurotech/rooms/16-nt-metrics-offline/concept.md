# Conceito — Métricas Offline: Cohen's Kappa ($\kappa$) e Taxa de Transferência de Informação de Wolpaw (ITR)

## 1. Fundamento Matemático: Além da Acurácia Ingênua
Na avaliação de interfaces cérebro-computador (BCI), a acurácia percentual simples ($P = \frac{\text{acertos}}{N}$) é uma métrica frágil e frequentemente enganosa quando há desbalanceamento de classes ou comparações entre paradigmas com números distintos de classes.

A literatura canônica estabelece duas métricas rigorosas: o coeficiente Kappa de Cohen ($\kappa$), estabelecido por [Schlögl et al. (JNE 2005, DOI 10.1088/1741-2560/2/4/L02)](https://doi.org/10.1088/1741-2560/2/4/L02), e a Taxa de Transferência de Informação (ITR) de [Wolpaw et al. (DOI 10.1016/j.clinph.2012.01.010)](https://doi.org/10.1016/j.clinph.2012.01.010).

### O Coeficiente Kappa de Cohen ($\kappa$)
O coeficiente $\kappa$ desconta a probabilidade de acerto esperado puramente por acaso ($p_e$):

$$\kappa = \frac{p_o - p_e}{1 - p_e}$$

Onde:
- $p_o$ é a acurácia observada (proporção de concordância entre predições e rótulos reais).
- $p_e$ é a concordância marginal esperada pelo acaso sob independência estatística:
  $$p_e = \sum_{k=1}^K P(\text{real} = k) \cdot P(\text{pred} = k)$$

Em um problema binário balanceado ($p_e = 0.50$):
- Se $p_o = 0.80$:
  $$\kappa = \frac{0.80 - 0.50}{1.0 - 0.50} = \frac{0.30}{0.50} = 0.60$$
- Se um classificador degenerado prever sempre a Classe 0 em uma base desbalanceada contendo $80\%$ de Classe 0 e $20\%$ de Classe 1:
  $$p_o = 0.80, \quad p_e = (0.80 \times 1.0) + (0.20 \times 0.0) = 0.80$$
  $$\kappa = \frac{0.80 - 0.80}{1.0 - 0.80} = 0.0$$
  O $\kappa$ colapsa exatamente para zero, expondo que o classificador não extraiu nenhuma informação neural útil!

### A Taxa de Transferência de Informação de Wolpaw (ITR)
Para comparar sistemas com diferentes números de classes $N$ e velocidades de emissão de comandos ($M$ ensaios por minuto), calcula-se a capacidade de canal em bits por ensaio ($B$):

$$B = \log_2(N) + P \log_2(P) + (1 - P) \log_2\left(\frac{1 - P}{N - 1}\right) \quad (\text{bits/ensaio})$$

E a taxa líquida em bits por minuto:
$$\text{ITR} = B \times M \quad (\text{bits/minuto})$$

Se $P = 1.0$ (acerto perfeito em $N = 4$ classes com $M = 10\text{ ensaios/min}$):
$$B = \log_2(4) = 2.0\text{ bits/ensaio} \implies \text{ITR} = 2.0 \times 10 = 20.0\text{ bits/min}$$

## 2. Modos de Falha Operacionais
1. **Publicar Acurácia sem Declarar a Distribuição Marginal das Classes**: Apresentar "acurácia de $75\%$" sem informar que o sujeito executou três vezes mais repetições de repouso do que de imagética ativa. Em classes desbalanceadas, a única métrica admissível em bancas de pós-graduação e revisões científicas é o Kappa de Cohen ou a matriz de confusão normalizada por classe.
2. **Comparar Acurácias entre Paradigmas Diferentes**: Comparar um sistema de P300 com matriz de 36 caracteres com um sistema de imagética motora binária (2 classes) usando acurácia bruta. Uma acurácia de $60\%$ em 36 classes (onde o acaso é de apenas $2.78\%$) representa uma ITR altíssima ($>40\text{ bits/min}$), enquanto $60\%$ em 2 classes (onde o acaso é de $50\%$) representa um $\kappa = 0.20$ medíocre.

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-latency-budget`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/19-nt-latency-budget/room.yaml)) assume que você tem um decodificador com métricas offline validadas ($\kappa > 0.60$), e introduz as restrições temporais determinísticas de malha fechada (*closed-loop*), onde o processamento matemático completo (aquisição, filtragem, extração de features, inferência e renderização) deve obedecer a um prazo fatal de latência (*deadline*).
