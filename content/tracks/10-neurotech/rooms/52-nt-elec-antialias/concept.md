# Conceito — O Teorema de Nyquist-Shannon e Filtros Anti-Aliasing Analógicos

O aliasing (rebatimento espectral) é uma distorção irreversível que ocorre quando um sinal analógico contínuo é amostrado a uma taxa insuficiente.

## 1. O Critério de Nyquist-Shannon
Para que um sinal analógico contínuo com largura de banda limitada $f_{\max}$ possa ser perfeitamente reconstruído a partir de suas amostras discretas:
$$f_s > 2 f_{\max}$$
A frequência $f_{\text{Nyquist}} = f_s / 2$ atua como um espelho espectral rígido:
- Qualquer componente de frequência $f_{\text{sinal}} > f_{\text{Nyquist}}$ é refletido para a frequência aparente:
  $$f_{\text{alias}} = |k f_s - f_{\text{sinal}}|$$
  (Onde $k$ é o inteiro que traz o resultado para o intervalo $[0, f_s/2]$).

## 2. A Necessidade Estrita do Filtro Anti-Aliasing Analógico
- **Irreversibilidade Digital:** Se ruídos de alta frequência (como fontes chaveadas em $140\text{ Hz}$ ou harmônicos de rede) forem digitalizados abaixo de Nyquist, eles se misturam aos ritmos cerebrais de interesse (como ritmos alfa e beta). Nenhum algoritmo de inteligência artificial ou filtro digital consegue desfazer a soma de duas frequências idênticas no sinal digitalizado.
- **Posicionamento no Hardware:** O filtro anti-aliasing é um circuito analógico passa-baixas ativo ou passivo (como um filtro Butterworth de ordem 2 a 4) inserido fisicamente **antes da entrada analógica do ADC**.

## 3. Modos de Falha na Prática de Engenharia
1. **Conectar ADC sem Filtro Analógico:** Confiar em filtros digitais em Python/C, ignorando que o rebatimento já destruiu o sinal antes da execução da primeira linha de software.
2. **Subdimensionar a Atenuação na Banda de Rebatimento:** Escolher um filtro passa-baixas com transição suave que atenua apenas 6 dB em $f_s / 2$, permitindo que ruídos fortes ultrapassem o piso de ruído do conversor.

## 4. O que a Próxima Sala Assume
A próxima fase (`nt-physics-electrostatics`) consolida os fundamentos de física eletrostática, gradiente de potencial e campos elétricos biofísicos.

## 5. Ponto de Destrave do Lab
Consulte o tratamento formal de amostragem e aliasing em [Oppenheim & Schafer (Discrete-Time Signal Processing, Prentice Hall)](https://www.pearson.com/) e a nota de aplicação da [Analog Devices (MT-002: What the Nyquist Criterion Means to Your Sampled Data System Design)](https://www.analog.com/media/en/training-seminars/tutorials/MT-002.pdf).
