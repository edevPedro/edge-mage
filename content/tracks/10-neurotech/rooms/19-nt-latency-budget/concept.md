# Conceito — Orçamento de Latência em Tempo Real (Sense → Decide → Act) e Prazos Fechados

## 1. Fundamento de Sistemas Embarcados em Malha Fechada (Closed-Loop BCI)
Para que uma interface cérebro-computador proporcione sensação de agência motora ou feedback neurofisiológico eficaz (neurofeedback), o circuito sensorial completo deve operar sob restrições estritas de tempo real (*hard real-time constraints*).

O atraso total fim-a-fim da malha é particionado em três estágios físicos e computacionais determinísticos:

$$\text{Latência Total} = T_{\text{sense}} + T_{\text{decide}} + T_{\text{act}}$$

Onde:
1. **$T_{\text{sense}}$ (Aquisição e Ingestão)**:
   O tempo físico necessário para coletar e encher o pacote de amostras do conversor analógico-digital:
   $$T_{\text{sense}} = \frac{N_{\text{packet}}}{f_s} \times 1000 \quad (\text{ms})$$
   Com $f_s = 250\text{ Hz}$ e pacotes de 1 amostra, o tempo de ingestão mínimo é $4.0\text{ ms}$.

2. **$T_{\text{decide}}$ (Processamento e Decisão)**:
   A soma do tempo de execução dos filtros causais IIR/biquads multicanal e do modelo de classificação linear:
   $$T_{\text{decide}} = T_{\text{filtros}} + T_{\text{classificador}} \quad (\text{ms})$$
   Com $C$ canais e $S$ seções de biquad, cada seção consumindo um custo de processamento determinístico, somado ao tempo de inferência do discriminante.

3. **$T_{\text{act}}$ (Atuação e Apresentação do Feedback)**:
   O tempo físico de transmissão serial/USB e o ciclo de varredura do atuador ou tela de exibição. Em um display gráfico padrão de $60\text{ Hz}$, o atraso intrínseco de atualização de quadro (*frame refresh*) é:
   $$T_{\text{display}} = \frac{1000}{60} \approx 16.67\text{ ms}$$

As diretrizes arquiteturais de sistemas closed-loop em BCI foram detalhadas por [Singh et al. (Sensors 2021, PMC8003721)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8003721/) e documentadas na pilha de hardware da [OpenBCI](https://docs.openbci.com/).

### O Teorema do Estouro de Buffer (Buffer Overrun)
Se o pipeline de decodificação processa dados a cada intervalo de passo (*hop interval*) de $N_{\text{hop}}$ amostras:
$$T_{\text{hop}} = \frac{N_{\text{hop}}}{f_s} \times 1000 \quad (\text{ms})$$

Para que a fila circular (*ring buffer*) de entrada não sofra estouro de capacidade (*buffer overrun*):
$$T_{\text{decide}} \le T_{\text{hop}}$$

Se o algoritmo consumir mais tempo calculando do que o intervalo de chegada dos novos blocos de dados ($T_{\text{decide}} > T_{\text{hop}}$), amostras de EEG serão inevitavelmente descartadas, corrompendo a continuidade temporal das fases dos filtros digitais e introduzindo instabilidade inaceitável.

## 2. Modos de Falha Operacionais
1. **O Modelo Pesado que Quebra o Deadline**: Embarcar uma rede neural profunda com tempo de inferência de $40\text{ ms}$ em um sistema com hop de $25\text{ ms}$ e prazo sensorial fatal (*deadline*) de $50\text{ ms}$. Com $T_{\text{sense}} = 4.0\text{ ms}$, $T_{\text{decide}} = 40.8\text{ ms}$ e $T_{\text{act}} = 16.6\text{ ms}$, a latência total atinge $61.4\text{ ms}$, quebrando o prazo e estourando o buffer de entrada.
2. **Esquecer a Latência do Monitor de Feedback**: O desenvolvedor calcula que seu código em C roda em $2\text{ ms}$ e declara que o sistema tem "latência de 2 ms", esquecendo que o sistema operacional e a taxa de varredura de $60\text{ Hz}$ do monitor impõem um atraso físico garantido de pelo menos $16.6\text{ ms}$ antes que os fótons atinjam a retina do sujeito.

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-online-stub`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/20-nt-online-stub/room.yaml)) assume que você tem um orçamento de latência validado e auditado, integrando todo o pipeline em um loop contínuo de streaming que ingere amostras, extrai características e emite comandos em tempo real.
