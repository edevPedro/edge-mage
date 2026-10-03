# História — A Autópsia do Vazamento de Dados

Em uma conferência internacional de engenharia biomédica, um artigo submetido por uma equipe acadêmica causou alvoroço ao relatar 96% de acurácia em um decodificador de quatro classes motoras usando um dataset público complexo do PhysioNet. No entanto, quando outros pesquisadores tentaram reproduzir o pipeline com os scripts disponibilizados no GitHub, a acurácia despencou para 26% — praticamente o nível de acaso puro ($1/4 = 25\%$).

O comitê de reprodutibilidade convocou os autores para uma revisão do código-fonte.

O auditor técnico abriu o notebook de pré-processamento e localizou duas linhas fatais:
```python
# Normalização Z-score aplicada antes do split de validação cruzada
X_normalized = (X - X.mean(axis=0)) / X.std(axis=0)
X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, shuffle=True)
```

— Observem o que aconteceu aqui — explicou o auditor. — Em primeiro lugar, ao calcular a média e o desvio-padrão de todo o dataset antes da divisão entre treino e teste, a distribuição do conjunto de teste vazou para dentro do conjunto de treino (data leakage). Em segundo lugar, e ainda mais grave: ao utilizar `shuffle=True` sobre amostras de janelas deslizantes sobrepostas de 2 segundos com deslocamento de 100 milissegundos, janelas adjacentes com 95% de sobreposição temporal foram sorteadas simultaneamente no treino e no teste.

Ele desenhou no quadro o mecanismo da ilusão:
— O modelo de vocês não aprendeu a decodificar intenções motoras; ele aprendeu a memorizar fatias quase idênticas do mesmo epoch temporal que estavam presentes nos dois conjuntos. Quando testado em um ensaio verdadeiramente independente de uma sessão futura, o classificador falhou por completo.

O auditor destacou que em BCI de avaliação offline:
1. A validação cruzada deve ser estritamente aninhada e agrupada por blocos de ensaios completos (`GroupKFold` ou split por runs).
2. Qualquer normalização ou seleção de canais deve ser ajustada *exclusivamente* com os dados do fold de treino.
3. A métrica de avaliação não pode ser apenas a acurácia ingênua, mas o coeficiente Kappa de Cohen ($\kappa$) descontando o acaso, acompanhado da Taxa de Transferência de Informação de Wolpaw (ITR em bits por minuto).

Os autores recolheram o manuscrito para correção. A métrica autêntica do pipeline revelou-se $\kappa = 0.58$ com ITR de $14.2\text{ bits/min}$ — um resultado modesto, porém cientificamente real e reproduzível.
