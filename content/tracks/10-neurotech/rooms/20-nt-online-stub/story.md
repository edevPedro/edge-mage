# História — O Primeiro Passo do Loop Contínuo

Na sala de validação de sistemas, a equipe de desenvolvimento prepara o primeiro teste de execução em malha aberta contínua de ponta a ponta. Não há sujeitos humanos plugados hoje: o gerador sintético de sinais (synth) emite blocos ininterruptos de 250 Hz simulando dados de 4 canais de escalpo com modulações alternadas de imagética motora.

O objetivo do sprint é validar a estabilidade do loop de processamento contínuo: receber pacotes sem perdas, manter o buffer circular preenchido, disparar a inferência a cada 100 milissegundos e registrar em log cada decisão com seu carimbo de tempo e latência associada.

O desenvolvedor júnior aperta o play no script do loop:
```python
# Loop online com coordenadas de janelamento deslizante
while streaming:
    packet = stream.read()
    ring_buffer.push(packet)
    if should_predict():
        coords = sliding_windows(total_samples, win_len, step_len)
        window = ring_buffer.get_window(coords[-1])
        prediction = model.predict(window)
        log.record(timestamp, prediction, latency)
```

No início, o sistema opera de forma fluida. Mas ao final de 30 minutos de teste de estresse ininterrupto, o arquivo de log revela o comportamento dos índices: a rotina de cálculo de coordenadas de janelas deslizantes (`sliding_windows`) precisa manter determinismo exato sobre o início e o fim de cada fatia para não perder amostras na fronteira nem processar janelas truncadas.

O engenheiro sênior examina o log de telemetria:
— O loop online é a prova definitiva de que seu pipeline de BCI está maduro. Na análise offline em notebooks, você tem todos os dados gravados no disco de uma vez e pode chamar funções globais. No loop online, você é escravo do relógio: a cada passo de janela (step), uma nova inferência deve ser entregue com precisão temporal milimétrica, sem vazamento do futuro e sem travar a ingestão de novas amostras.

As coordenadas das janelas deslizantes são verificadas: para um fluxo de tamanho `total_len`, com janelas de comprimento `win_len` e deslocamento `step_len`, as fatias cobrem o sinal sem descontinuidade. O ritual do loop online simulado é concluído com sucesso, marcando a transição oficial do estudante de analista offline de dados gravados para engenheiro de sistemas neurais de tempo real.
