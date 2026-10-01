# Conceito — Autograd

## Intuição (masters bar)
Frameworks (PyTorch) constroem um **grafo dinâmico** no forward quando tensores têm `requires_grad=True`. `loss.backward()` aplica a regra da cadeia e preenche `.grad`.

## Inferência
`torch.no_grad()` / `torch.inference_mode()` + `model.eval()`: sem tape → menos RAM e latência. Edge quase sempre roda assim.

## Não confundir
Autograd ≠ otimizador. Autograd calcula ∇; `optim.SGD` / Adam aplica o update.
