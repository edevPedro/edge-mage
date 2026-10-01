# e-mage

Terminal academy (Textual TUI) for three courses: **Fundamentals** → **Systems Mage** → **Edge ML Mage**.  
Product name: **e-mage**. GitHub repo (for now): [edevPedro/edge-mage](https://github.com/edevPedro/edge-mage).  
CLI entrypoints: `mage` · `emage` · `edge-mage`.

[Português (pt-BR)](README.pt-BR.md)

[![license](https://img.shields.io/badge/license-MIT-1c1c1c?style=flat-square)](LICENSE)
[![python](https://img.shields.io/badge/python-3.11%2B-1c1c1c?style=flat-square)](pyproject.toml)
[![tests](https://img.shields.io/github/actions/workflow/status/edevPedro/edge-mage/test.yml?branch=main&style=flat-square&label=tests)](https://github.com/edevPedro/edge-mage/actions)

## Courses

| id | Course | Role |
|----|--------|------|
| `fundamentals` | Fundamentals | Path to **Mago base** (shared core + clearance) |
| `systems` | Systems Mage | FLAG-lab / systems catalog (`~/.mage/packs/systems.json`) |
| `edge` | Edge ML Mage | Current math → on-device Edge AI tracks (full TUI UX) |

`mage` opens a **course launcher** first (plus GitHub connect stub). Systems/Edge are soft-gated behind Mago base (preview allowed with a warning).

Shared core rooms live under `content/shared/` (`vectors`, `bits`, `intro-asm`) with stable `room_id` credit.

Content packs may later live in a sibling `emage-content` repo; none was present beside this tree at Phase 0–1.

## Install

Requires **Python 3.11+**.

### One-liner (macOS / Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/edevPedro/edge-mage/main/install.sh | bash
```

### Clone

```bash
git clone https://github.com/edevPedro/edge-mage.git
cd edge-mage
./install.sh
# or: make install
```

Links into `~/.local/bin`: `mage` · `emage` · `edge-mage`.

```bash
export PATH="$HOME/.local/bin:$PATH"   # if needed
mage --version && mage
```

Dev: `make install-dev` · `make test` · `USE_PIPX=1 ./install.sh`

### Platform notes

| Platform | Notes |
|----------|--------|
| **macOS** | Xcode CLT or Homebrew `python@3.12`; then `./install.sh` |
| **Debian / Ubuntu** | `sudo apt install python3 python3-venv python3-pip git` |
| **Fedora** | `sudo dnf install python3 python3-pip git` |
| **Arch** | `sudo pacman -S python python-pip git` |
| **Windows** | Use **WSL2** (Ubuntu), then Debian steps |
| **Termux** | `pkg install python git`; run `./install.sh` (symlink `~/.local/bin` into PATH) |

## Offline progress & sync

- Progress home: **`~/.mage/`** (one-time copy from `~/.edge-mage/` if present)
- Packs cache: `~/.mage/packs/`
- Auth stub: `~/.mage/auth.json`
- `mage sync` / `:sync` — pull catalog stub + POST progress to `{MAGE_API_BASE}/api/estudo/mage/progress` (default API base `https://edevs.com`)

## Controls (Edge course TUI)

| Key | Action |
|-----|--------|
| `j` `k` `h` `l` / Enter | navigate |
| `i` | INSERT (answer) |
| `:` | command line |
| `Ctrl+w` + `w`/`h`/`l` | panes |
| `g` + `p`/`r`/`t`/`h` | profile / grimoire / tracks / home |
| `:courses` | back to launcher |
| `:sync` | packs + API + study journal |
| `q` | quit |

## Ranks

**Global:** none → **Mago base** (Fundamentals clear) → intermediate → **Mago Supremo** (systems boss craft + edge on-device + evidence).

**Edge course (internal):** Novice → … → Archmage → **Edge Mage** (XP ≥ 2900 **and** on-device ritual).

## License

MIT · Python 3.11+ · Unicode-capable terminal recommended
