# Desafio — Validação de Margem de Segurança em Tempo Real (RT-Safe)

## 1. Objetivo do Desafio
Implementar a rotina de certificação temporal para sistemas de tempo real estrito, verificando se o tempo de execução medido de uma tarefa neural embarcada atende ao prazo máximo estipulado mesmo após a inclusão de uma margem de segurança de engenharia (*headroom*).

## 2. Especificação Técnica
Implemente a função `rt_safe(measured_us, max_deadline_us, headroom_pct=20.0)`:
- Calcule o tempo projetado com a margem de headroom:
  $$t_{proj} = measured\_us \times \left(1 + \frac{headroom\_pct}{100.0}\right)$$
- Retorne um booleano indicando se a execução é segura:
  - `True`: se $t_{proj} \le max\_deadline\_us$.
  - `False`: se $t_{proj} > max\_deadline\_us$.

## 3. Casos de Teste de Referência
```python
# 700 us + 20% = 840 us <= 1000 us -> True
assert rt_safe(700.0, 1000.0, 20.0) is True

# 900 us + 20% = 1080 us > 1000 us -> False
assert rt_safe(900.0, 1000.0, 20.0) is False
```

## 4. Critérios de Validação e Armadilhas
- Certifique-se de que a comparação utilize a relação menor ou igual ($\le$).
- O parâmetro `headroom_pct` deve ser interpretado como porcentagem (ex: 20.0 significa 20%, ou fator multiplicativo de 0.20).
