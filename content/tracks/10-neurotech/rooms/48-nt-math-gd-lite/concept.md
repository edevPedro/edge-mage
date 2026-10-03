# Conceito — Gradiente Descendente e Otimização Linear em BCI

Modelos de decodificação neural adaptativa (como filtros adaptativos LMS, regressão logística online e redes neurais como EEGNet) ajustam seus parâmetros minimizando uma função de perda empírica sobre os sinais cerebrais.

## 1. O Fundamento Matemático do Lab

### O Passo de Atualização por Gradiente
Dada uma função de perda convexa $L(w)$ parametrizada por pesos $w \in \mathbb{R}^d$, o gradiente $\nabla_w L$ aponta na direção de maior crescimento da perda. Para minimizar o erro, damos um passo na direção oposta com taxa de aprendizado $\eta > 0$ (learning rate):
$$w^{(k+1)} = w^{(k)} - \eta \, \nabla_w L(w^{(k)})$$

### Ajuste de Filtro Linear com Erro Quadrático Médio (MSE)
Considerando um conjunto de $N$ pares de treinamento $(x_i, y_i)$, onde $x_i \in \mathbb{R}^d$ é o vetor de features e $y_i \in \mathbb{R}$ é o alvo:
$$L(w) = \frac{1}{2N} \sum_{i=1}^N (w^T x_i - y_i)^2$$

O gradiente analítico em relação a $w$ é a média dos produtos do resíduo pelo vetor de entrada:
$$\nabla_w L = \frac{1}{N} \sum_{i=1}^N (w^T x_i - y_i) x_i$$

A convergência em direção aos pesos ótimos $w^*$ ocorre iterativamente ao longo de sucessivas épocas.

## 2. Unidades e Grandeza Física
- **Pesos ($w$):** Adimensionais ou inverso da grandeza da feature.
- **Gradiente ($\nabla L$):** Unidade da perda dividida pela unidade de $w$.
- **Taxa de aprendizado ($\eta$):** Fator de escala. Se os dados $x$ estão em microvolts ($\sim 10\ \mu\text{V}$), o gradiente pode assumir ordens de grandeza dependentes da escala; a normalização das features é crítica para que $\eta$ não precise ser infinitesimal.

## 3. Modos de Falha na Prática de Engenharia
1. **Divergência por Learning Rate Excessiva:** Se $\eta > \frac{2}{\lambda_{\max}(X^T X / N)}$, a power iteration implícita da Hessiana explode: os pesos $w$ alternam de sinal com magnitudes que crescem exponencialmente até `NaN` ou `inf`.
2. **Convergência Falsa por Platô:** Em classificadores sem regularização onde features são colineares (eletrodos adjacentes captando o mesmo dipolo elétrico), o gradiente se aproxima de zero mas o modelo oscila num vale plano de mínima curvatura.

## 4. O que as Próximas Fases Assumem
Com a conclusão da trilha de matemática (F1-math), o aluno possui o ferramental analítico completo (espaços vetoriais, covariância amostral, autovetores dominantes, níveis de significância estatística, correção de viés e otimização por gradiente) para ingressar na física e bioeletricidade dos tecidos (F2 e F3).

## 5. Ponto de Destrave do Lab
Para inspecionar convergência de classificadores lineares por descida de gradiente estocástica, consulte a documentação oficial do [scikit-learn SGDClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html).
