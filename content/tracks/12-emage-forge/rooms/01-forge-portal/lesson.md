# Forge · portal

Você manterá **um** motivo computacional (ex.: GEMM pequeno, filtro DSP, ou kernel de similaridade) e o evoluirá:

1. **F0** scalar + harness  
2. **F1** NEON/ASIMD  
3. **F2** Roofline / tiling  
4. **F3** Metal  
5. **F4** inference (quant / runtime)  
6. **F5** co-design lite (opcional)

Critério de passagem = o mesmo do Performance Boss: medir, explicar, provar correção. Não invente hardware que você não tem — documente o fallback.
