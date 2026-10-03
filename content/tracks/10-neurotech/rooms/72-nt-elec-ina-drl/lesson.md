# Lição — Amplificador de Instrumentação e Saturação por Trilho

## 1. Contexto Operacional
O amplificador de instrumentação (INA) é o primeiro guardião analógico da cadeia de sinal bioelétrico. O projetista deve equilibrar ganho suficiente para elevar o biopotencial acima do ruído térmico sem saturar os trilhos de alimentação devido a offsets DC de eletrodo.

## 2. Passo a Passo Matemático

### Ganho do Amplificador de Instrumentação
$$G = 1 + \frac{2 R_1}{R_G}$$

### Auditoria de Saturação por Trilho
Dados o ganho $G$, o sinal diferencial AC $V_{\text{diff\_uv}}$ (microvolts), o offset DC $V_{\text{offset\_dc\_mv}}$ (milivolts), a tensão de alimentação $V_{\text{supply\_v}}$ e a folga de trilho $V_{\text{headroom\_v}}$ (ex: $0.2\text{ V}$):
1. Calcule a tensão de entrada total em Volts:
   $$V_{\text{in}} = (V_{\text{diff\_uv}} \times 10^{-6}) + (V_{\text{offset\_dc\_mv}} \times 10^{-3})$$
2. Tensão de saída teórica:
   $$V_{\text{out}} = G \times V_{\text{in}}$$
3. Limite de excursão linear:
   $$V_{\max} = V_{\text{supply\_v}} - V_{\text{headroom\_v}}$$
4. Se $|V_{\text{out}}| \ge V_{\max}$:
   retorne `(False, v_out, f"Saturação do INA: V_out = {v_out:.3f}V excede limite linear ({v_max:.2f}V)")`.
5. Caso contrário:
   retorne `(True, v_out, f"Operação linear: V_out = {v_out:.3f}V na faixa segura")`.

Consulte o datasheet do [TI ADS1299](https://www.ti.com/lit/ds/symlink/ads1299.pdf) para entender os limites de modo comum e dinâmica de entrada em bioamplificadores integrados.
