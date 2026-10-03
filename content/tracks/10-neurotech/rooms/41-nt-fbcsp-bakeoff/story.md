# História — O Duelo de Titãs: FBCSP contra Riemann

Em um seminário de benchmark em neurotecnologia, duas equipes de pesquisadores debatem qual arquitetura é superior para BCI de quatro classes motoras: a primeira defende o algoritmo Filter Bank Common Spatial Pattern (FBCSP), consagrado como vencedor de múltiplas BCI Competitions; a segunda defende os classificadores baseados em Geometria Riemanniana no espaço tangente (TS+ElasticNet).

O moderador do laboratório coloca um terminal no centro da mesa e estabelece as regras de um confronto rigoroso (Bake-Off):
— Nenhuma comparação entre algoritmos tem valor científico se os modelos forem avaliados em splits diferentes, com sementes diferentes ou com janelas temporais desiguais — determina o moderador. — Um bake-off honesto exige que ambas as abordagens recebam exatamente os mesmos dados brutos, passem pela mesma filtragem causal e sejam avaliadas pelos mesmos folds estritos de validação cruzada por blocos.

As duas equipes executam seus pipelines sobre o benchmark público:
- O **FBCSP** decompõe o sinal em sub-bandas de 4 Hz, extrai 4 filtros espaciais CSP por banda e classifica os vetores de log-variância concatenados.
- O **Classificador Riemanniano** calcula a matriz de covariância espacial regularizada, projeta os dados no espaço tangente euclidiano através do logaritmo matricial e classifica com regressão linear regularizada.

Os resultados finais são projetados lado a lado:
- FBCSP: Acurácia média de $77.8\%$, Kappa $\kappa = 0.704$, tempo de treino de $14.2\text{ s}$.
- Riemann: Acurácia média de $78.2\%$, Kappa $\kappa = 0.709$, tempo de treino de $1.8\text{ s}$.

— A beleza do bake-off transparente é desmistificar dogmas — conclui o moderador. — Ambos os métodos atingem desempenho de topo estatisticamente equivalente, mas a abordagem Riemanniana demonstra extrema elegância computacional e menor tempo de calibração, enquanto o FBCSP permite uma inspeção neurofisiológica mais direta das bandas ativadas.
