# Desafio — Campo de Dipolo e Atenuação com a Distância

## 1. Objetivo do Desafio
O potencial elétrico no escalpo é gerado por correntes pós-sinápticas em populações neuronais alinhadas. O modelo biofísico clássico de primeira aproximação é o dipolo elétrico de corrente.

## 2. Passo a Passo Matemático

### Potencial de Dipolo Eletrostático
$$V(r, \theta) = \frac{p \cos\theta}{4\pi \epsilon_0 r^2}$$

### Atenuação Geométrica Cortical vs. Escalpo
Dados $r_{\text{near}}$ e $r_{\text{scalp}}$ em metros, com o mesmo momento $p$ e ângulo $\theta$:
1. $V_{\text{near}} = \text{dipole\_potential}(p, \theta, r_{\text{near}})$.
2. $V_{\text{scalp}} = \text{dipole\_potential}(p, \theta, r_{\text{scalp}})$.
3. Razão teórica de atenuação:
   $$\text{ratio} = \frac{V_{\text{near}}}{V_{\text{scalp}}} = \left(\frac{r_{\text{scalp}}}{r_{\text{near}}}\right)^2$$
4. Retorne `(v_near, v_scalp, ratio)`.

Consulte [Michel & Brunet (2019)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6700197/) para os fundamentos da modelagem de fontes em eletroencefalografia.
