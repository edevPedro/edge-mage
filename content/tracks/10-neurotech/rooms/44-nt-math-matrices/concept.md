# Conceito — Matrizes, Transformações Lineares e Covariância Amostral

Em processamento de sinais neurais, matrizes desempenham dois papéis fundamentais:
1. **Transformações espaciais instantâneas:** Uma matriz $A \in \mathbb{R}^{M \times C}$ mapeia $C$ canais de eletrodos em $M$ sinais derivados ($y = Ax$), como montagens bipolares ou Common Average Reference (CAR).
2. **Representação estatística da dinâmica cortical:** A matriz de covariância espacial $\Sigma \in \mathbb{R}^{C \times C}$ quantifica a dispersão conjunta e o acoplamento elétrico entre todos os pares de eletrodos ao longo de uma janela temporal de $T$ amostras.

## 1. O Fundamento Matemático do Lab

### Multiplicação Matriz-Vetor ($y = Ax$)
Se $x \in \mathbb{R}^C$ é o vetor de tensões em um instante $t$, a $i$-ésima saída transformada é o produto interno da $i$-ésima linha de $A$ por $x$:
$$y_i = \sum_{j=1}^C A_{ij} x_j$$

### Matriz de Covariância Multicanal Amostral
Dada uma matriz de dados centrada $\tilde{X} \in \mathbb{R}^{C \times T}$, onde cada linha corresponde a um canal com média temporal subtraída ($\mu_c = \frac{1}{T}\sum_{t=1}^T X_{c, t}$):
$$\tilde{X}_{c, t} = X_{c, t} - \mu_c$$

A estimativa não enviesada da covariância amostral entre o canal $i$ e o canal $j$ é:
$$\Sigma_{ij} = \frac{1}{T - 1} \sum_{t=1}^T \tilde{X}_{i, t} \tilde{X}_{j, t} = \left( \frac{1}{T - 1} \tilde{X} \tilde{X}^T \right)_{ij}$$

A diagonal principal $\Sigma_{ii}$ contém a variância temporal de cada eletrodo (energia da banda), enquanto os elementos fora da diagonal $\Sigma_{ij}$ refletem a correlação cruzada induzida pela condução de volume e sincronia neural.

## 2. Unidades e Estrutura Geométrica
- **Sinal temporal ($X_{c, t}$):** $\mu\text{V}$ (microvolts).
- **Variância e covariância ($\Sigma_{ij}$):** $\mu\text{V}^2$ (microvolts ao quadrado).
- **Propriedade fundamental:** $\Sigma$ é simétrica ($\Sigma = \Sigma^T$) e Semidefinida Positiva (SPD) se $T \ge C$ e os canais forem linearmente independentes.

## 3. Modos de Falha na Prática de Engenharia
1. **Esquecer de Centrar os Dados:** Se a média temporal $\mu_c$ (offset DC do eletrodo ou deriva de potencial) não for removida antes do produto externo, o termo $\frac{1}{T-1} X X^T$ não representará a variância, mas sim a potência média total contaminada por offset contínuo, gerando covariâncias falsamente infladas.
2. **Subamostragem Crítica ($T < C$):** Quando a janela temporal tem menos amostras do que o número de canais ($T < C$), a matriz empírica $\Sigma$ é estritamente singular (posto $< C$, determinante zero). Nenhuma rotina de inversão clássica funcionará sem regularização por shrinkage.

## 4. O que a Próxima Sala Assume
A sala seguinte ([`nt-math-eigen`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/45-nt-math-eigen/room.yaml)) assume que você tem uma matriz $\Sigma$ simétrica $2 \times 2$ válida para extrair autovalores e autovetores via power iteration.

## 5. Ponto de Destrave do Lab
Para sanar dúvidas de alinhamento dimensional em produtos matriciais ou na formulação da geometria Riemanniana sobre matrizes SPD, consulte [NumPy matmul](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html) e o paper pioneiro de [Barachant et al. (2011, DOI 10.1109/TBME.2011.2172210)](https://doi.org/10.1109/TBME.2011.2172210).
