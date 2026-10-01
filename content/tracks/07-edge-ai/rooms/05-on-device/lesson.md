# On-Device Checklist

Antes de chamar a si mesmo Edge Mage, o binário precisa sobreviver ao mundo real.

## Orçamento

RAM, flash, potência (mW), latência (ms), térmica. Sem orçamento, não há deploy — só demo.

## Ops e fallback

Aceleradores (NPU/DSP) cobrem um subset de ops. O que não cabe cai em **fallback CPU** lento — profile o grafo.

## Golden tests

Compare saídas com referência conhecida (float vs quantizado) em inputs fixos. Regressão silenciosa é o boss final.

## Pipeline

Sensor → pré-processamento → inferência → pós-processamento → ato (UI/motor/alerta).
O modelo é só o miolo.
