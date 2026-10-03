# História — A Ilusão da Causalidade em Tempo Real

Em uma demonstração ao vivo de controle de cursor por imagética motora, um engenheiro de software conecta seu novo filtro digital baseado na biblioteca SciPy. Durante a fase de calibração em dados gravados, os resultados eram impecáveis: ruído de 60 Hz e oscilações lentas foram completamente suprimidos sem qualquer distorção temporal aparente.

Porém, assim que o pipeline entra em operação contínua em tempo real, o sistema trava ou exibe atrasos intoleráveis:
```python
# Erro fatal de tempo real: filtragem não-causal em streaming
y = scipy.signal.filtfilt(b, a, chunk)
```

O especialista em processamento digital de sinais do laboratório aproxima-se e desconecta a rotina:
— A função `filtfilt` aplica o filtro no sentido direto e, em seguida, inverte o sinal no tempo e o filtra de trás para frente — explica o especialista. — Isso cancela a distorção de fase e produz fase estritamente zero, mas viola o princípio da causalidade física: para filtrar para trás, você precisa conhecer o futuro do sinal! No mundo real de streaming contínuo, você só tem acesso às amostras do presente e do passado.

Ele desenha a estrutura canônica de uma seção de segunda ordem (Biquad IIR) no quadro:
— Em tempo real, você é obrigado a trabalhar com filtros causais. Filtros IIR (como Butterworth) oferecem transições de corte muito mais íngremes com pouca ordem matemática, mas introduzem atraso de grupo não-linear (distorção de fase). Filtros FIR oferecem fase perfeitamente linear, mas injetam um atraso de grupo fixo de $(N - 1)/(2 f_s)$ amostras. Para um filtro FIR com 65 coeficientes a 250 Hz, isso representa um atraso inegociável de 128 milissegundos!

O engenheiro compreende o trade-off: ele substitui o filtro não-causal por uma cascata de seções biquad IIR causais calculadas ponto a ponto (`biquad_step`), monitorando o atraso de grupo e garantindo estabilidade numérica estrita.
