# e-mage

Academia no terminal (TUI Textual): **uma jornada contínua** — engenharia de performance low-level → arch CPU → SIMD → HPC → GPU → otimização de inferência → co-design HW/SW.  
Rótulos legados (Systems / Performance / Edge / Neurotech) são **fases ou ramos**, não cursos rivais na home.  
Produto: **e-mage**. GitHub: [edevPedro/edge-mage](https://github.com/edevPedro/edge-mage).  
CLIs: `mage` · `emage` · `edge-mage` · id primário **`emage`**.

Arquitetura: [`docs/SPEC-emage-single-track.md`](docs/SPEC-emage-single-track.md) · diagnóstico: [`docs/DIAGNOSTIC-emage-pre-unification.md`](docs/DIAGNOSTIC-emage-pre-unification.md).

[English](README.md)

[![license](https://img.shields.io/badge/license-MIT-1c1c1c?style=flat-square)](LICENSE)
[![python](https://img.shields.io/badge/python-3.11%2B-1c1c1c?style=flat-square)](pyproject.toml)
[![tests](https://img.shields.io/github/actions/workflow/status/edevPedro/edge-mage/test.yml?branch=main&style=flat-square&label=tests)](https://github.com/edevPedro/edge-mage/actions)

## Objetivos — o que esperar

**e-mage não é um tutorial solto de sintaxe.** É um caminho até você conseguir **ler máquina + prova craft + ML no dispositivo**, com FLAG no lab e artefato real (GitHub / on-device) nos bosses.

### Nível de chegada (Mago Supremo)

Ao fechar o círculo (Fundamentos + Systems craft + Edge on-device), o nível técnico pretendido é o de alguém que consegue:

| Domínio | O que você consegue fazer |
|---------|---------------------------|
| **Compiladores / LLVM** | Ler IR, explicar pipeline clang→opt→llc, contribuir em issues/PRs pedagógicos de tooling de compilador, escrever ou adaptar um pass/lab simples |
| **Systems / low-level** | Raciocinar stack/heap/ABI, usar nm/objdump/lldb sem medo, ligar C → objeto → binário |
| **Segurança / RE** | Achar classes de falha (UB, race, trust boundary), fazer RE clássico leve e falar limites de lifting — base para bug hunting e cyber defensivo |
| **Embedded / bare-metal lite** | Ler asm AArch64 o suficiente para frames, MMIO, syscalls e boot conceitual — porta de entrada para firmware/robotics |
| **Machine learning (edge)** | Treinar/exportar modelo minúsculo, medir latência/RAM, rodar inferência on-device e defender o número com evidência |
| **Math → ML** | Tratar feature como vetor, um passo de gradiente de verdade, não só “usei a lib” |

Isso **não** te transforma automaticamente em sênior de compilador ou red team. Te deixa **acima de “só fiz curso de Python”**: pronto para contribuir em projetos low-level/ML edge, entrevistar para estágio hardcore, e continuar sozinho.

### Fases da jornada (um caminho)

| Fase | Rótulo interno | Ao concluir |
|------|----------------|-------------|
| **P0** Fundamentos | shared + clearance | *Mago base* |
| **P1** Systems | pack FLAG + craft | ABI/IR + evidência publicada |
| **P2–P5** Arch → SIMD → HPC → GPU | salas Performance | Medir → explicar → provar |
| **P6** Inferência | trilhas Edge ML + ponte | Ritual on-device (latência/RAM) |
| **P7** Co-design | RTL/HLS lite | Boss acelerador pedagógico |
| **Forge** | projeto cumulativo | Mesmo motivo evolui nas fases |
| **Ramo** Neurotech | opcional | BCI/EEG — rota Suprema alt.; não é a home |

### O que *não* prometer

- Emprego garantido ou certificação oficial
- Substituir faculdade / mestrado (complementa)
- Zerar só no emulador sem bosses = progresso de grimório, **não** o nível da tabela acima

Web espelho: [edevs.com.br/estudo](https://edevs.com.br/estudo) · detalhes: docs no edevs (`estudo-emage.md`).

## Assembly e arquiteturas

O curso **ensina a ler máquina**, não a memorizar três ISAs inteiras. Papel de cada família:

| ISA | Papel no curso | Onde |
|-----|----------------|------|
| **AArch64 (ARM 64-bit)** | ISA **profunda** — Edge ML / BCI, mobile, Apple Silicon | `intro-asm` → Edge `aarch64-abi` → CMSIS-NN · LLVM F2 |
| **x86_64** | Host/RE literacy — **sem trilha ISA completa** | Relance `isa-x86-aarch64` · Systems SysV / `sys-asm-read` |
| **ARM 32-bit (AArch32)** | Só contexto histórico | Docs Arm — **não** é trilha |
| **RISC-V** | Relance opcional — load/store + gosto de psABI | Shared `riscv-lite` — **não** substitui AArch64 |
| **Outras (MIPS, AVR…)** | Fora de escopo | — |

**Regra (Edge / BCI):** profundidade real = **AArch64**. x86_64 e RISC-V = literacia de relance (≤1 sala cada). Não diluir salas ARM.

**Por que AArch64 no centro?** Edge ML + BCI: energia/área/térmica, NEON/CMSIS-NN, LiteRT Micro.  
**Por que x86_64 ainda existe?** PC host + RE clássico — uma sala compare, não farm de opcode.  
**Por que RISC-V leve?** Silício aberto; alfabetização (`lw`/`sw`, `a0`); sem privileged ISA / Vector `V` / design de core.

Leitura pedida: conseguir abrir Godbolt / `objdump`, apontar registradores de arg/retorno e não entrar em pânico — depois o IR do LLVM amarra as pontas.

## Duração (± jornada única)

Caminho sustentável de **1–3 anos** a **4–8 h/semana**. Spine (P0–P7 + Forge) ≈ **400–650 h** guiadas.

| Fatia | Horas (±) | Notas |
|-------|-----------|--------|
| **P0** Fundamentos | 25–40 h | → Mago base |
| **P1** Systems | 50–90 h | FLAG + craft |
| **P2–P5 + P7** fases Performance | ~200–280 h scaffold | Arch→SIMD→HPC→GPU→co-design |
| **P6** Inferência / Edge | 50–90 h | Na spine **depois** da GPU |
| **Forge** | overlap com bosses | Evidência cumulativa |
| **Ramo Neurotech** | ver SPEC | Opcional |

Caveats M4: µarch ≠ Cortex-A; sem SVE; Metal ≠ CUDA.  
SPECs: [`SPEC-emage-single-track.md`](docs/SPEC-emage-single-track.md) · Performance · Neurotech.

> **O currículo evolui.** Números são snapshot, não diploma fixo. C++ pro ≠ pular arch/SIMD/GPU automaticamente.

## Jornada e browser de módulos

| id | Papel |
|----|--------|
| **`emage`** | **Jornada primária** (`mage` / `mage --course emage`) |
| `fundamentals` | Alias · P0 |
| `systems` | Alias · P1 FLAG |
| `performance` | Alias · salas P2–P7 |
| `edge` | Alias · P6 Edge ML |
| `neurotech` | **Ramo** opcional |

`mage` abre o launcher com **Continuar jornada** primeiro; ids legados ficam no módulo browser (soft gate / preview OK).

### Fase Systems no TUI

A jornada (ou alias **Systems**) carrega muitas salas FLAG offline (não é stub hello):

- Snapshot no pacote: `content/packs/systems.json` (exportado de edevs `systems.ts` / `llvm.ts` / `math.ts`)
- O install copia para `~/.mage/packs/systems.json` — primeira abertura já vem cheia
- Fases como trilhas: **systems** · **llvm** · **math** · **craft** (`boss-craft` + `shared-math-evidence` continuam YAML ricos)
- Núcleo compartilhado (`vectors`, `bits`, …) credita uma vez via `room_id`
- `mage sync` / `:sync` atualiza o pack de `GET /api/estudo/mage/catalog` (`systemsMagePack`) online; offline mantém o catálogo bundled

Edge ML Mage permanece o caminho ARM profundo on-device — Systems **não** substitui as trilhas Edge AI.

Salas compartilhadas em `content/shared/` (`vectors`, `bits`, `intro-asm`, `isa-x86-aarch64`, `riscv-lite`) com crédito por `room_id` único.

Índices de currículo + salas shared em JSON: repo irmão **[edevPedro/emage-content](https://github.com/edevPedro/emage-content)** (`SYNC.md`). Clone ao lado deste tree ou use `EMAGE_CONTENT_ROOT`.

## Instalar

Precisa de **Python 3.11+**.

### Uma linha (macOS / Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/edevPedro/edge-mage/main/install.sh | bash
```

### Clone

```bash
git clone https://github.com/edevPedro/edge-mage.git
cd edge-mage
./install.sh
# ou: make install
```

Symlinks em `~/.local/bin`: `mage` · `emage` · `edge-mage`.

```bash
export PATH="$HOME/.local/bin:$PATH"   # se precisar
mage --version && mage
```

Dev: `make install-dev` · `make test` · `USE_PIPX=1 ./install.sh`

### Plataformas

| Plataforma | Notas |
|----------|--------|
| **macOS** | Xcode CLT ou Homebrew `python@3.12`; depois `./install.sh` |
| **Debian / Ubuntu** | `sudo apt install python3 python3-venv python3-pip git` |
| **Fedora** | `sudo dnf install python3 python3-pip git` |
| **Arch** | `sudo pacman -S python python-pip git` |
| **Windows** | Use **WSL2** (Ubuntu) e siga o fluxo Debian |
| **Termux** | `pkg install python git`; rode `./install.sh` (coloque `~/.local/bin` no PATH) |

## Estudar offline (M4 / sem rede)

O TUI é a **fonte da verdade**. Lições em `content/` (`story` · `concept` · `lesson` · `room.yaml`). Links externos são opcionais — o Estuda ensina a fundação antes da Sala.

```bash
cd /Users/epedro/eCodes/edevs/edge-mage
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
mage --course emage
```

Sem rede: conteúdo + `content/packs/systems.json` + progresso em `~/.mage/`. `mage sync` / GitHub / web só quando online.

## Offline e sync

- Progresso: **`~/.mage/`** (cópia única de `~/.edge-mage/` se existir)
- Packs: `~/.mage/packs/` — Systems já vem com catálogo FLAG no install (`content/packs/systems.json` → `systems.json`)
- Auth stub: `~/.mage/auth.json`
- `mage sync` / `:sync` — puxa o pack Systems de `{MAGE_API_BASE}/api/estudo/mage/catalog` (`systemsMagePack`) + POST em `/api/estudo/mage/progress`. Offline mantém/semeia o pack bundled.

## Controles (curso Edge)

| Tecla | Ação |
|-----|--------|
| `j` `k` `h` `l` / Enter | navegar |
| `i` | INSERT (responder) |
| `:` | command line |
| `Ctrl+w` + `w`/`h`/`l` | painéis |
| `g` + `p`/`r`/`t`/`h` | perfil / grimório / trilhas / home |
| `:courses` | voltar ao launcher |
| `:sync` | packs + API + diário |
| `:publish <boss>` | gera `ARTIFACT/<boss>/` (não envia/pusha) |
| `q` | sair |

## Artefatos de boss (`mage publish`)

Cada boss gera um `ARTIFACT/<boss>/` pronto para o GitHub:

```bash
mage publish                 # lista bosses + status ritual/publicado
mage publish on-device       # valida o ritual e gera o artefato
```

Gera um `README.md` de uma página com as seções **O que medi / O que me
surpreendeu / O que faria depois** (+ instruções de reprodução), um
`evidence.json` e gráficos ASCII montados do evidence log
(`study-log/completions.jsonl`). **Não envia nada** sozinho — apenas imprime os
próximos passos de git.

Conteúdo limpo por princípio: sem código proprietário, protocolo interno ou dado
real de empregador/corretora. Salas de teoria são curtas e toda sala traz um
exercício verificável (não só MCQ); `scripts/lint_resources.py` garante isso.

## Ranks

O rank sobe **só com boss aprovado + artefato publicado** — o XP continua
acumulando, mas sozinho bate num teto (`mage publish <boss>` é o portão).

**Global:** nenhum → **Mago base** (Fundamentos) → intermediário (≥1 boss
publicado) → **Mago Supremo** (boss systems + on-device edge + shared math,
todos publicados; ou a rota MSc do Neurotech).

**Curso Edge (interno):** Noviço → … → Arquimago (teto de XP) → **Edge Mage**
(XP ≥ 2900 **e** ritual on-device **e** `mage publish on-device`).

## Qualidade e CI

- Testes do runner (`tests/test_runner_sandbox.py`): PASS, FAIL, timeout,
  compilação quebrada e ruído alto (stdout limitado a 20k chars).
- GitHub Actions roda `pytest`, `scripts/lint_resources.py` e um benchmark smoke
  do runner (`scripts/benchmark_smoke.py`) em Linux.

## Licença

MIT · Python 3.11+ · terminal com Unicode recomendado
