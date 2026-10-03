# História — O Gargalo do Produtor e do Consumidor

Na bancada de integração de um sistema de BCI portátil, um desenvolvedor conecta um conversor ADS1299 a um microcontrolador via barramento SPI. O conversor dispara interrupções de amostragem determinísticas a 250 Hz, enviando um novo pacote de biopotenciais a cada quatro milissegundos. No computador hospedeiro, uma rotina em Python consome os dados para extrair características de potência de banda em janelas de 1 segundo (250 amostras).

Nas primeiras horas de teste, o sistema trava subitamente ou apresenta atrasos bizarros de até dez segundos na resposta motora.

O engenheiro de software sênior abre o monitor de recursos e inspeciona o código de recepção:
```python
# Ingestão ingênua com alocação dinâmica em loop
buffer = []
while True:
    sample = read_sample()
    buffer.append(sample)
    if len(buffer) >= 250:
        predict(buffer[-250:])
```

— Observem a alocação dinâmica contínua — aponta o engenheiro sênior. — O array cresce indefinidamente na memória, forçando o coletor de lixo do Python a paralisar o processo periodicamente para desalocar blocos de memória antigos. Além disso, a rotina de predição leva 30 milissegundos para executar; enquanto ela processa uma janela, as interrupções de novas amostras são enfileiradas de forma caótica no driver serial, acumulando um atraso crescente (drift de latência).

Ele desenha a solução canônica de tempo real: o Buffer Circular (Ring Buffer) com ponteiros de leitura e escrita pré-alocados em memória contígua fixa:
— Em sistemas de streaming bioelétrico, nunca alocamos memória durante o ciclo de amostragem. O produtor (a interrupção de hardware) escreve amostras na posição do ponteiro `head`. O consumidor (o classificador de janelas deslizantes) lê blocos a partir de `tail`. Quando o índice atinge a capacidade máxima $C$, ele retorna a zero via aritmética modular ($i \pmod C$).

O desenvolvedor constrói a classe `RingBuffer` com capacidade fixa e métodos determinísticos `push`, `is_full` e extração de janelas deslizantes. O consumo de memória estabiliza-se em uma linha plana perfeita, o garbage collector cessa suas pausas, e a latência de ponta a ponta volta a respeitar o relógio em tempo real.
