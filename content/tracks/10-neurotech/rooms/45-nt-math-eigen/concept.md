# Conceito — Autovalores, Autovetores e Decomposição Espectral

A extração de padrões bioelétricos multicanais depende da diagonalização de matrizes de covariância. Seja no Principal Component Analysis (PCA) para redução de dimensionalidade ou no Common Spatial Patterns (CSP) para maximização de contraste motor, o coração do pipeline é a equação fundamental:
$$\Sigma v = \lambda v$$

## 1. O Fundamento Matemático do Lab

### Autovetor e Autovalor em Matrizes de Covariância
Para uma matriz de covariância simétrica $\Sigma \in \mathbb{R}^{C \times C}$:
- O **autovetor** $v \in \mathbb{R}^C$ representa um filtro espacial (uma direção de projeção no espaço de canais) que não sofre rotação quando transformado pela matriz de covariância; ele apenas é escalado.
- O **autovalor** $\lambda \in \mathbb{R}^+$ corresponde à variância (potência) do sinal projetado nessa direção:
  $$\lambda = \frac{v^T \Sigma v}{v^T v} = v^T \Sigma v \quad (\text{para } \|v\|_2 = 1)$$
  Essa expressão é conhecida como o **Quociente de Rayleigh**.

### O Método das Potências (Power Iteration)
Em sistemas embarcados de tempo real onde algoritmos iterativos completos de decomposição QR ou SVD são proibitivamente lentos, o autovetor associado ao maior autovalor ($\lambda_1$) pode ser extraído diretamente por power iteration:
1. Inicie com um vetor arbitrário não ortogonal $v^{(0)} = [1.0, 1.0]^T$.
2. Para cada iteração $k = 1, \dots, K$:
   $$w^{(k)} = \Sigma v^{(k-1)}$$
   $$v^{(k)} = \frac{w^{(k)}}{\|w^{(k)}\|_2}$$
3. Conforme $k \to \infty$, o vetor $v^{(k)}$ converge exponencialmente para o autovetor dominante $v_1$ com taxa determinada pela razão $|\lambda_2 / \lambda_1|$.

## 2. Unidades e Grandeza Física
- **Autovetor ($v$):** Vetor adimensional normalizado no círculo unitário ($\|v\|_2 = 1$).
- **Autovalor ($\lambda$):** Unidade de potência cortical: $\mu\text{V}^2$. Em uma montagem de 2 canais, $\lambda_1 + \lambda_2 = \text{tr}(\Sigma) = \text{Var}(C3) + \text{Var}(C4)$ (conservação da variância total).

## 3. Modos de Falha na Prática de Engenharia
1. **Espectro Degenerado ($\lambda_1 \approx \lambda_2$):** Se a matriz de covariância for aproximadamente isotrópica (ruído branco esférico onde $\Sigma \approx \sigma^2 I$), a power iteration não converge para uma direção única, oscilando dependendo da inicialização.
2. **Matrizes Singulares ou com Ruído de Linha:** Se um canal saturar em $60\text{ Hz}$, o autovalor dominante $\lambda_1$ capturará exclusivamente o ruído de rede elétrica em vez de atividade neural cortical, mascarando a banda mu/beta.

## 4. O que a Próxima Sala Assume
A sala seguinte ([`nt-math-probability`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/46-nt-math-probability/room.yaml)) assume que você compreende a distribuição de variâncias e está pronto para avaliar se as taxas de acerto derivadas dessas projeções superam estatisticamente o nível de chance pura.

## 5. Ponto de Destrave do Lab
Para sanar problemas na convergência da power iteration ou consultar a decomposição espectral analítica, consulte a documentação oficial [NumPy linalg eig](https://numpy.org/doc/stable/reference/generated/numpy.linalg.eig.html) e o paper seminal de Common Spatial Patterns de [Ramoser et al. (DOI 10.1109/86.895946)](https://doi.org/10.1109/86.895946).
