# Desafio — Verificação de Aliasing e Cálculo de Frequência Rebatida

## 1. Objetivo do Desafio
Implementar a rotina analítica para verificar se um sinal contínuo de frequência $f_{\text{sinal}}$ sofrerá rebatimento sob taxa de amostragem $f_s$, calculando a frequência aparente resultante.

## 2. Especificação Técnica e Formulação
Dadas a frequência do sinal contínuo `f_signal` e a taxa de amostragem `fs` (ambas em Hertz):
- Implemente a função `check_aliasing(f_signal, fs)`:
  - Calcule o limite de Nyquist: $f_{\text{Nyq}} = f_s / 2$.
  - Se $f_{\text{signal}} \le f_{\text{Nyq}}$: não há aliasing; retorne `(False, f_signal)`.
  - Se $f_{\text{signal}} > f_{\text{Nyq}}$: há aliasing; calcule a frequência rebatida fundamental:
    $$f_{\text{alias}} = |f_{\text{signal}} - \text{round}(f_{\text{signal}} / f_s) \times f_s|$$
    Retorne a tupla `(True, f_alias)`.

## 3. Critérios de Validação e Armadilhas
- Para $f_{\text{signal}} = 140\text{ Hz}$ e $f_s = 160\text{ Hz}$, o retorno deve ser `(True, 20.0)`.
- Para $f_{\text{signal}} = 60\text{ Hz}$ e $f_s = 250\text{ Hz}$, o retorno deve ser `(False, 60.0)`.
