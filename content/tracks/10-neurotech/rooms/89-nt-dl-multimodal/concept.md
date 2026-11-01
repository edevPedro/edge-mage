# Conceito — Multimodal: uma paleta, várias modalidades

Esta é a sala-eletiva de fechamento do módulo F15. Ela mostra que a paleta
aprendida (tokens → atenção → quantização → batching) serve para texto, áudio,
imagem e sinal — e que a infraestrutura de inferência muda de forma, não de
lógica.

## 1. Embeddings e um espaço comum
- Modelos multimodais (CLIP, Whisper-style encoders) mapeiam cada modalidade
  para **embeddings** num espaço onde *similaridade de cosseno* = proximidade
  semântica: imagem de gato fica perto de "gato".
- Retri on retrieval: buscar imagem por texto = achar o vizinho mais próximo.

## 2. Modelos gerativos por modalidade
- **Texto**: LLM autoregressivo (já visto — decode e cache).
- **Imagem**: difusão — começa em ruído puro e *denoisa em passos iterativos*
  (o "decode" da imagem custa N passos de rede → latência e steps são o SLA).
- **Áudio/sinal**: encoders contínuos (Whisper para fala; EEG/BCI usa janelas +
  convoluções — a mesma noção de janela).

## 3. O que muda na inferência
- **Pipeline heterogêneo**: encoder (modalidade) → unificador → decoder
  (geração). Cada estágio tem seu próprio formato de tensão e SLA.
- **Batching contínuo ainda vale**: cada estágio tem fila própria (as imagens
  pedem GPU, o texto pede CPU/GPU, o encoder é leve) — mas a API de fila e as
  métricas (TTFT/throughput/percentis) são as mesmas.
- **Quantização e cache**: igualmente aplicáveis (denoising loop re-lê
  intermediários; cache de prompts-vizinhos é gold).

## 4. Fechamento do módulo
Do `nt-dl-portal` ao multimodal você percorreu o mapa do roadmap.sh:
- decide quando DL faz sentido (N≫D vs inductive bias);
- forward de MLP/CNN, treino honesto;
- tokens, atenção, LLM;
- cache, quantização, formatos, serving;
- métricas para fechar o loop com medição.

## Leituras recomendadas
- [CLIP (Radford et al.)](https://arxiv.org/abs/2103.00020)
- [Hugging Face Diffusers](https://huggingface.co/docs/diffusers/en/index)
- [Whisper (Radford et al.)](https://arxiv.org/abs/2212.04356)