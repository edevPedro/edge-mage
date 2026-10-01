# e-mage

Academia no terminal (TUI Textual) com três cursos: **Fundamentos** → **Systems Mage** → **Edge ML Mage**.  
Nome do produto: **e-mage**. Repositório GitHub (por enquanto): [edevPedro/edge-mage](https://github.com/edevPedro/edge-mage).  
CLIs: `mage` · `emage` · `edge-mage`.

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

### Por curso

| Curso | Objetivo | Nível ao concluir |
|-------|----------|-------------------|
| **Fundamentos** → *Mago base* | Perder medo do PC/terminal; ordem, erro, math útil; primeira página/craft | Consegue seguir um lab, capturar FLAG, publicar 1 artefato simples |
| **Systems Mage** | Máquina nua → IR → AArch64 → DIY/RE | Consegue contribuir em discussões/PRs de systems/LLVM e caçar bugs de memória/ABI |
| **Edge ML Mage** | Math → sinal → modelo → **on-device** | Consegue um ritual edge (latência/RAM reais) e falar trade-offs de deploy no device |

### O que *não* prometer

- Emprego garantido ou certificação oficial
- Substituir faculdade / mestrado (complementa)
- Zerar só no emulador sem bosses = progresso de grimório, **não** o nível da tabela acima

Web espelho: [edevs.com.br/estudo](https://edevs.com.br/estudo) · detalhes: docs no edevs (`estudo-emage.md`).

## Cursos

| id | Curso | Papel |
|----|--------|------|
| `fundamentals` | Fundamentos | Caminho até **Mago base** (núcleo compartilhado + clearance) |
| `systems` | Systems Mage | FLAG-lab / catálogo systems (`~/.mage/packs/systems.json`) |
| `edge` | Edge ML Mage | Trilhas atuais math → Edge AI on-device (UX TUI completa) |

`mage` abre o **seletor de cursos** primeiro (e stub de GitHub). Systems/Edge têm soft gate atrás de Mago base (preview com aviso).

Salas compartilhadas em `content/shared/` (`vectors`, `bits`, `intro-asm`) com crédito por `room_id` único.

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

## Offline e sync

- Progresso: **`~/.mage/`** (cópia única de `~/.edge-mage/` se existir)
- Packs: `~/.mage/packs/`
- Auth stub: `~/.mage/auth.json`
- `mage sync` / `:sync` — puxa catálogo stub + POST em `{MAGE_API_BASE}/api/estudo/mage/progress`

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
| `q` | sair |

## Ranks

**Global:** nenhum → **Mago base** (Fundamentos) → intermediário → **Mago Supremo** (boss systems + on-device edge + evidência).

**Curso Edge (interno):** Noviço → … → Arquimago → **Edge Mage** (XP ≥ 2900 **e** ritual on-device).

## Licença

MIT · Python 3.11+ · terminal com Unicode recomendado
