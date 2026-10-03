# Lição — FIR vs IIR, Atraso de Grupo e Projeto de Biquads

## 1. O Trade-Off Fundamental de Filtragem em BCI
1. **FIR de Fase Linear**:
   - Vantagens: Estabilidade intrínseca incondicional (sem polos fora da origem), fase linear com atraso de grupo puramente constante em todas as frequências.
   - Desvantagens: Exige alta ordem ($N \ge 65\text{--}129$ taps) para transições espectrais abruptas. Atraso puro de grupo $\tau = \frac{N-1}{2 f_s}$ consome dezenas a centenas de milissegundos do orçamento em tempo real.

2. **IIR Causal de 2ª Ordem (Biquads)**:
   - Vantagens: Atinge transições espectrais acentuadas com apenas 5 multiplicações por amostra ($b_0, b_1, b_2, a_1, a_2$) e atraso de grupo muito baixo ($<15\text{ ms}$).
   - Desvantagens: Não possui fase estritamente linear; suscetível a instabilidade numérica se os polos saírem do círculo unitário ($|z| \ge 1.0$).

3. **A Ilusão do `filtfilt`**:
   O algoritmo `filtfilt` realiza filtragem bidirecional acausal, sendo estritamente reservado para análises retrospectivas em lote (*offline*). Em loops causais fechados, apenas filtros unilaterais com histórico de estado são admissíveis.

## 2. As Funções de Laboratório Desta Sala
- `biquad_step(x, b, a, state)`: Executa um passo causal de equação em diferenças IIR com persistência de estado.
- `design_butterworth_lowpass_biquad(fs, fc)`: Projeta os coeficientes digitalmente via Transformada Bilinear com pre-warping espectral.
- `audit_filter_stability(a)`: Avalia os polos característicos da equação $z^2 + a_1 z + a_2 = 0$, verificando se residem no interior do círculo unitário ($|z| < 1.0$).

Para destravar o lab, abra [scipy.signal.firwin](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.firwin.html) e leia o comprimento do FIR e a janela em scipy.signal.firwin, para o atraso de grupo (N−1)/(2 fs) não ficar só no datasheet.
