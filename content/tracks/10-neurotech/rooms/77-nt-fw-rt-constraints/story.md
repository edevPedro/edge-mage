# História — A folga que o microsegundo não tinha

Prioridade de amostragem fica acima de log de UI — o fill é “maior”. O stub de Cortex não é o chip. A conta é `rt_safe(measured_us, deadline_us, headroom_pct)`: cabe se `measured * (1 + headroom/100)` não passa do deadline.

Folga de 20%. Medido 700 µs, deadline 1000: `700 * 1,2 = 840 ≤ 1000` → verdadeiro. Medido 900: `900 * 1,2 = 1080 > 1000` → falso. Os 900 sozinhos caberiam; com headroom, não. Ignorar os 20% marca os dois como seguros e a Sala recusa.

840 e 1080 são microssegundos de orçamento, não tempo de uma ISR medida em silício. Headroom existe porque o caminho real ganha jitter que o notebook não mostra. FIR de 128 taps dentro da interrupção, a 500 Hz, é o jeito errado que esta sala corta: a conta da folga vem antes de comemorar que “no host passou”.

Fase F9, nt-fw-rt-constraints: 700 µs com 20% de folga passa; 900 µs não, porque 1080 > 1000. O fill da prioridade é maior para a amostragem. O stub não é o silício.
