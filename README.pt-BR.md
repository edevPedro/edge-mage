# e-mage

Academia no terminal (TUI Textual) com três cursos: **Fundamentos** → **Systems Mage** → **Edge ML Mage**.  
Nome do produto: **e-mage**. Repositório GitHub (por enquanto): [edevPedro/edge-mage](https://github.com/edevPedro/edge-mage).  
CLIs: `mage` · `emage` · `edge-mage`.

[English](README.md)

[![license](https://img.shields.io/badge/license-MIT-1c1c1c?style=flat-square)](LICENSE)
[![python](https://img.shields.io/badge/python-3.11%2B-1c1c1c?style=flat-square)](pyproject.toml)
[![tests](https://img.shields.io/github/actions/workflow/status/edevPedro/edge-mage/test.yml?branch=main&style=flat-square&label=tests)](https://github.com/edevPedro/edge-mage/actions)

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
