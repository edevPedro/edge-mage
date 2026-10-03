# Conceito — Estimação espectral para EEG

- **FFT curta** → resolução Δf ≈ 1/T pobre; vazamento se a janela não for periódica.
- **Welch:** médias de periodogramas com overlap → menor variância.
- **Trade-off:** janela longa = melhor Δf, pior resolução temporal (ruim para ERD rápido).
