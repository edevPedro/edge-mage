# Lição — Condução de Volume e Borrão Espacial

## 1. Condução de Volume no Modelo Esférico Concéntrico
A cabeça humana é modelada na eletrofisiologia como um condutor de volume multicamadas (tipicamente 3 ou 4 esferas concêntricas: cérebro, líquor, crânio e couro cabeludo).

1. **A Descontinuidade do Crânio**:
   O osso craniano possui condutividade elétrica $\sigma_{\text{crânio}} \approx 0.008\text{ S/m}$, enquanto o cérebro e o escalpo possuem condutividade cerca de 40 vezes maior ($\sigma \approx 0.33\text{ S/m}$). O líquor (LCR) atinge $\sigma \approx 1.79\text{ S/m}$.
   Essa barreira resistiva atua como um difusor lateral das correntes de retorno bioelétricas.

2. **Filtro Passa-Baixa Espacial**:
   Matematicamente, se expandirmos o potencial de superfície em harmônicos esféricos $Y_{lm}$, os modos de alta frequência espacial (altos valores de $l$, correspondentes a gradientes espaciais finos) decaem exponencialmente mais rápido do que os modos de baixa frequência espacial (baixo $l$).
   O resultado é uma Função de Espalhamento de Ponto (Point Spread Function - PSF) com largura a meia altura (FWHM) de $\approx 2.5\text{ cm}$.

3. **O Critério de Rayleigh e Resolução no Escalpo**:
   Duas fontes corticais separadas por uma distância $d$ só geram dois picos discerníveis no escalpo se $d \ge \text{FWHM}$. Fontes mais próximas do que $2.5\text{ cm}$ sofrem fusão unimodal completa no escalpo.

## 2. As Funções de Laboratório Desta Sala
- `spatial_blur_1d(channels, kernel)`: Simula a difusão espacial através de um filtro de convolução 1D suavizador.
- `audit_spatial_resolution(source_distance_cm, skull_blur_fwhm_cm)`: Aplica o critério de resolução espacial, calculando a razão entre distância física das fontes e o FWHM do crânio, determinando se há separabilidade direta no escalpo.

Para destravar o lab, abra [Michel & Brunet — EEG source imaging (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6700197/) e leia os passos de source imaging em Michel e Brunet (condução de volume, não pixel de escalpo) para fechar a conta de blur.
