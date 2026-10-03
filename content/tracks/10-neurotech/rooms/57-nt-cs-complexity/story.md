# História — O produto que cabe e o que não cabe

Deadline de janela não negocia com Big-O de quadro. `within_deadline(C, T, us_per_sample, deadline_us)` aceita se `C * T * us_per_sample` cabe no orçamento.

Primeiro: 8 canais, 200 amostras, 0,5 µs por par, deadline 1000 µs. `8 * 200 * 0,5 = 800 ≤ 1000` → verdadeiro. Segundo: 64 canais, 500 amostras, o mesmo custo unitário. `64 * 500 * 0,5 = 16000 > 1000` → falso. A diferença não é “otimizar depois”; é miss.

O fill lembra que covariância ingênua cresce com expoente em C — cortar canal corta essa conta. 800 e 16000 estão em microssegundos, não em κ. Estourar o deadline atrasa o decide. Nenhum dos dois casos é latência medida num córtex real; é o predicado que o harness da sala exige antes de prometer online.

Fase F5, nt-cs-complexity: 800 µs cabe em 1000; 16000 µs não. O predicado é booleano. Cov ingênua cresce com potência de C — o fill pede esse expoente, não um κ.
