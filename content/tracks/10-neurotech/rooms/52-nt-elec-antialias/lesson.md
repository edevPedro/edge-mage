# Lição — Teorema de Nyquist e Filtro Anti-Aliasing

## 1. Contexto Operacional
O Teorema de Amostragem de Nyquist-Shannon impõe que qualquer componente espectral acima de $f_s / 2$ sofrerá dobramento (aliasing) irreversível sobre a banda de interesse bioelétrico. O filtro anti-alias analógico deve atuar antes do conversor.

## 2. Passo a Passo Matemático

### Detecção de Rebatimento Espectral
Dado um sinal analógico em $f_{\text{sinal}}$ e taxa $f_s$:
1. $f_N = f_s / 2$.
2. Se $f_{\text{sinal}} \le f_N$:
   não há aliasing, $f_{\text{aparente}} = f_{\text{sinal}}$.
3. Se $f_{\text{sinal}} > f_N$:
   $f_{\text{aparente}} = |f_{\text{sinal}} - \text{round}(f_{\text{sinal}} / f_s) \times f_s|$.

### Auditoria da Spec de Filtro Anti-Alias Butterworth
Dados $f_c$ (frequência de corte em Hz), $f_s$, ordem do filtro $n$ e atenuação mínima requerida em decibéis:
1. $f_N = f_s / 2.0$.
2. Se $f_c \ge f_N$:
   retorne `(False, 0.0, f"Frequência de corte {fc_hz}Hz >= Nyquist ({nyquist_hz}Hz): filtro inútil")`.
3. Calcule a atenuação na frequência de Nyquist:
   $$\text{att\_db} = 10.0 \times \log_{10}\left(1.0 + \left(\frac{f_N}{f_c}\right)^{2n}\right)$$
4. Se $\text{att\_db} < \text{min\_attenuation\_at\_nyquist\_db}$:
   retorne `(False, att_db, f"Atenuação insuficiente em Nyquist ({att_db:.1f} dB < {min_attenuation_at_nyquist_db} dB)")`.
5. Caso contrário:
   retorne `(True, att_db, f"Filtro anti-alias válido com atenuação de {att_db:.1f} dB em Nyquist")`.

Consulte [SciPy signal decimate](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.decimate.html) para exemplos práticos de filtragem passa-baixas pré-amostragem.
