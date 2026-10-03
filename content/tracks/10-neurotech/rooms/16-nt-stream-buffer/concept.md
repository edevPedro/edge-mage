# Conceito — Stream e ring buffer

Online simulado: amostras chegam em chunks; você guarda só a janela recente em capacidade fixa.

Micro-exemplo: capacidade 64; ao empurrar a 65ª, a mais antiga cai — `latest(n)` devolve o fim do anel.
