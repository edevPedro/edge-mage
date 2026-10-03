# Conceito — Restrições de Tempo Real, Hierarquia de Prioridades e Margem Headroom

## 1. Hard Real-Time vs. Soft Real-Time em Neuroengenharia
- **Soft Real-Time:** Em aplicações de análise offline ou visualização gráfica para o usuário, atrasos ocasionais causam desconforto estético ou pequenas pausas perceptíveis, mas não comprometem a integridade física do experimento.
- **Hard Real-Time:** Em sistemas de malha fechada (*closed-loop neuromodulation*, estimulação em fase, controle de próteses ativas), a entrega de um comando fora do prazo estipulado é uma falha catastrófica equivalente à entrega de um comando incorreto.

## 2. A Hierarquia Canônica de Prioridades de Interrupção
Em um microcontrolador dedicado a BCI (ex: ARM Cortex-M NVIC):
1. **Prioridade Crítica (Mais Alta):** Interrupção de hardware do ADC / DMA (`DRDY_IRQ`). Amostras analógicas degradam se não forem transferidas no instante exato do relógio de amostragem.
2. **Prioridade Média-Alta:** Processamento de sinais determinístico (filtragem digital IIR, cálculo de potências de banda).
3. **Prioridade Média:** Pilha de comunicação e telemetria (BLE, Wi-Fi, barramento CAN).
4. **Prioridade Baixa (Background / Idle):** Registro de logs não essenciais, formatação de mensagens de texto para interface do usuário e atualização de displays gráficos.

A atribuição de prioridades incorreta gera inversão de prioridade: uma rotina lenta de impressão de logs (`printf`) pode bloquear a aquisição de amostras, provocando perda de dados irrecuperável.

## 3. O Critério Numérico de Headroom
Para absorver flutuações temporais provocadas por *jitter* de barramento, *cache misses* e variações na tensão de alimentação, define-se uma margem de segurança percentual ($headroom\_pct$):

$$t_{seguro} = t_{medido} \times \left(1 + \frac{headroom}{100}\right)$$

Critério de aprovação:
$$t_{seguro} \le t_{deadline}$$

Se $t_{seguro} > t_{deadline}$, o sistema é classificado como inseguro (*unsafe*), exigindo otimização de código, redução da taxa de amostragem ou adoção de hardware mais veloz.

## 4. O Que a Próxima Sala Assume
Esta sala encerra os fundamentos de firmware e conecta-se diretamente com os casos práticos e aplicações clínicas do percurso.
