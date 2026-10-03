# Conceito — Condução de Volume e Borrão Espacial

## 1. Fundamento Físico e Limite de Resolução
O cérebro humano é envolvido por camadas biológicas com descontinuidade extrema de condutividade elétrica $\sigma$ (em $\text{S/m}$):

| Camada | Espessura Típica | Condutividade $\sigma$ ($\text{S/m}$) | Razão vs Crânio |
|---|---|---|---|
| **Córtex / Substância Cinzenta** | $\sim 3\text{ mm}$ | $\approx 0.33\text{ S/m}$ | $\approx 40\times$ mais condutor |
| **Líquido Cefalorraquidiano (LCR)** | $\sim 2\text{ mm}$ | $\approx 1.79\text{ S/m}$ | $\approx 220\times$ mais condutor |
| **Osso Craniano (Crânio)** | $\sim 5\text{--}7\text{ mm}$ | $\approx 0.008\text{ S/m}$ | **Referência isolante** ($1\times$) |
| **Couro Cabeludo (Escalpo)** | $\sim 5\text{ mm}$ | $\approx 0.33\text{ S/m}$ | $\approx 40\times$ mais condutor |

A alta resistividade do crânio em relação ao córtex e ao couro cabeludo cria um fenômeno eletrostático crucial: as linhas de corrente bioelétricas que emanam de um dipolo cortical preferem espalhar-se lateralmente no LCR e no córtex antes de cruzar o osso de alta resistência. Ao emergirem no couro cabeludo, o potencial espalha-se por uma área considerável.

Esse efeito atua como um **filtro passa-baixa espacial** intrínseco. A função de espalhamento de ponto (Point Spread Function - PSF) de uma fonte focal no córtex atinge no escalpo uma largura a meia altura (Full Width at Half Maximum - FWHM) de aproximadamente $2.0\text{--}3.0\text{ cm}$, como detalhado em [Michel & Brunet (PMC6700197)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6700197/) e [Nunez (DOI 10.1017/S0140525X00003253)](https://doi.org/10.1017/S0140525X00003253).

### O Critério de Rayleigh Espacial
Pelo critério de resolução de Rayleigh adaptado a campos potenciais:
Duas fontes corticais separadas por uma distância $d$ só geram dois picos distintos no escalpo se:
$$d \ge \text{FWHM}_{\text{crânio}} \approx 2.5\text{ cm}$$

- Se duas fontes estão a $d = 1.0\text{ cm}$ (por exemplo, representações somatotópicas do polegar e do indicador no córtex motor primário M1):
  $$\text{Razão} = \frac{1.0}{2.5} = 0.4 < 1.0 \implies \text{Não resolvíveis diretamente no escalpo}$$
  Os potenciais fundem-se em um único pico largo e indistinto.
- Se as fontes estão a $d = 4.0\text{ cm}$ (representação da mão em C3 vs perna/pé em Cz):
  $$\text{Razão} = \frac{4.0}{2.5} = 1.6 \ge 1.0 \implies \text{Resolvíveis espacialmente no escalpo}$$

## 2. Modos de Falha Operacionais
1. **A Falácia do "Super-EEG de 256 Canais"**: Acreditar que adensar eletrodos a distâncias de $5\text{ mm}$ no escalpo confere resolução milimétrica aos sinais. Aumentar a densidade de eletrodos além de $\sim 64\text{--}128$ canais atinge o limite de difusão de Nyquist espacial do crânio. Sem modelos inversos regularizados com ressonância magnética estrutural, o ganho de informação útil satura.
2. **Ignorar Correlação Espacial no Machine Learning**: Como um único dipolo induz voltagem em múltiplos eletrodos adjacentes devido à condução de volume, canais vizinhos possuem covariância não-nula mesmo sem qualquer conectividade funcional real entre as áreas corticais subjacentes. Assumir independência entre canais de EEG em modelos bayesianos é um erro conceitual grave.

## 3. O que a Próxima Sala Assume
A próxima sala do percurso é `nt-physics-field-lite` (Physics — Campo e distância (lite)): Potencial vs distância; por que fontes profundas somem.
