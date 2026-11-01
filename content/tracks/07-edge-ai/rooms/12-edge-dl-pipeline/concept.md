# Conceito — Pipeline de DL até o device

## Estágios
`acquire → preproc → infer → post` dentro do deadline.

## Golden test
Saída do runtime embarcado == saída do modelo de referência (float/int8) — regressão real.

## Orçamento
`headroom = deadline − Σestágios`; `utilização = Σestágios / deadline`.