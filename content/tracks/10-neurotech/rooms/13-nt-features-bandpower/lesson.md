# Lição — Potência de banda

1. Filter bank → um sinal por banda/canal (ou PSD → integrar banda).
2. Feature simples: média dos quadrados (potência média) na janela do trial.
3. Micro-exemplo: synth com `schedule_mu_burst` (probe de energia) deve subir bandpower µ — **não** chame isso de ERD fisiológico.
4. Unidades: synth em µV didáticos; potências ficam em µV² (didático).
5. Implemente `bandpower` na Sala; depois pense covariância multicanal.

## Fontes
- [Yger et al. HAL](https://inria.hal.science/hal-01394253/document)
