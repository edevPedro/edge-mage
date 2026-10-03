# História — A Linha Vermelha do Dispositivo Médico

Em uma reunião com investidores de uma startup de neurotecnologia assistiva, o diretor de marketing exibiu um slide chamativo: *"Nosso decodificador de EEG é um dispositivo médico revolucionário capaz de ler os pensamentos de pacientes com esclerose lateral amiotrófica (ELA) e traduzir frases completas instantaneamente."*

O diretor de assuntos regulatórios e bioengenharia levantou-se imediatamente e interrompeu a apresentação:

— "Remova esse slide agora mesmo. Este curso, as boas práticas de engenharia e os órgãos regulatórios (como Anvisa e FDA) proíbem categoricamente alegações de dispositivo médico certificado para protótipos de pesquisa. EEG não lê pensamentos ou frases inteiras; EEG capta pequenas modulações estatísticas de biopotenciais no couro cabeludo."

Ele puxou o quadro branco e reescreveu os objetivos técnicos com rigor:

— "Em interfaces assistivas reais para pessoas com perda severa de controle motor (como o clássico trabalho de Wolpaw), o que nós medimos não é milagre: é latência de seleção, taxa de transferência de informação (Information Transfer Rate - ITR em bits por minuto) e carga cognitiva suportável pelo usuário. Ninguém quer um teclado virtual que cometa erros catastróficos a cada piscada."

O engenheiro de software da equipe perguntou:

— "Como evitamos seleções involuntárias provocadas por ruído momentâneo?"

— "Com integração temporal por acumulador de permanência (*dwell accumulator*)", explicou o regulador. "Em vez de disparar uma tecla na primeira amostra em que a probabilidade do classificador for alta, nós acumulamos as probabilidades ao longo do tempo. O comando só é confirmado quando a soma atinge um limiar seguro (*threshold*). Isso filtra picos espúrios de ruído e devolve ao usuário o controle da interface com segurança ética e usabilidade real."
