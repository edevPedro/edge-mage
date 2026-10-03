# Conceito — FIR vs IIR no BCI

- **FIR linear-phase:** atraso constante ≈ (N−1)/(2 fs) — previsível no budget.
- **IIR:** eficiente, mas fase não-linear / atraso de grupo variável; cuidado em online.
- **Causalidade:** filtros forward-backward (filtfilt) são offline; online precisa causal.
