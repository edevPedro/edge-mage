# e-mage

Terminal academy (Textual TUI) for three courses: **Fundamentals** → **Systems Mage** → **Edge ML Mage**.  
Product name: **e-mage**. GitHub repo (for now): [edevPedro/edge-mage](https://github.com/edevPedro/edge-mage).  
CLI entrypoints: `mage` · `emage` · `edge-mage`.

[Português (pt-BR)](README.pt-BR.md)

[![license](https://img.shields.io/badge/license-MIT-1c1c1c?style=flat-square)](LICENSE)
[![python](https://img.shields.io/badge/python-3.11%2B-1c1c1c?style=flat-square)](pyproject.toml)
[![tests](https://img.shields.io/github/actions/workflow/status/edevPedro/edge-mage/test.yml?branch=main&style=flat-square&label=tests)](https://github.com/edevPedro/edge-mage/actions)

## Goals — what to expect

**e-mage is not a loose syntax tutorial.** It is a path to **read the machine + prove craft + run ML on-device**, with FLAGs in labs and real artifacts (GitHub / on-device) at bosses.

### Arrival level (Mago Supremo)

After closing the loop (Fundamentals + Systems craft + Edge on-device), the intended bar is someone who can:

| Domain | You should be able to |
|--------|------------------------|
| **Compilers / LLVM** | Read IR, explain clang→opt→llc, contribute to pedagogical compiler-tooling issues/PRs, write or adapt a simple pass/lab |
| **Systems / low-level** | Reason about stack/heap/ABI, use nm/objdump/lldb without fear, go C → object → binary |
| **Security / RE** | Spot failure classes (UB, races, trust boundaries), do light classic RE and state lifting limits — foundation for bug hunting / defensive cyber |
| **Embedded / bare-metal lite** | Read enough AArch64 asm for frames, MMIO, syscalls, and conceptual boot — on-ramp to firmware/robotics |
| **Machine learning (edge)** | Train/export a tiny model, measure latency/RAM, run on-device inference and defend the numbers with evidence |
| **Math → ML** | Treat features as vectors, take a real gradient step — not “I only called the library” |

This does **not** mint you a senior compiler engineer or red-teamer overnight. It puts you **ahead of “I only finished a Python course”**: ready to contribute to low-level / edge-ML projects, interview for hardcore internships, and keep going solo.

### Per course

| Course | Goal | Level when done |
|--------|------|-----------------|
| **Fundamentals** → *Mago base* | Stop fearing the PC/terminal; order, failure, useful math; first page/craft | Follow a lab, capture a FLAG, ship one simple artifact |
| **Systems Mage** | Bare metal → IR → AArch64 → DIY/RE | Join systems/LLVM discussions/PRs; hunt memory/ABI bugs |
| **Edge ML Mage** | Math → signal → model → **on-device** | Complete an edge ritual (real latency/RAM) and discuss device deploy trade-offs |

### What we do *not* promise

- A job offer or official certification
- A replacement for university / grad school (it complements them)
- Clearing emulator rooms only, without bosses = grimoire progress, **not** the table above

Web mirror: [edevs.com.br/estudo](https://edevs.com.br/estudo) · details in edevs `docs/estudo-emage.md`.

## Assembly & architectures

e-mage teaches you to **read the machine**, not memorize three full ISAs.

**Curriculum rule (Edge / BCI):** real depth = **AArch64**. x86_64 and RISC-V are **literacy at a glance** (≤1 room each). Do not dilute ARM rooms in Edge AI.

| ISA | Role | Where |
|-----|------|--------|
| **AArch64 (ARM 64-bit)** | **Deep** — phones, Apple Silicon, edge ML / BCI | `intro-asm` → Edge `aarch64-abi` → CMSIS-NN → on-device · LLVM F2 |
| **x86_64** | Host/RE literacy — **no full ISA track** | Glance room `isa-x86-aarch64` · Systems SysV / `sys-asm-read` |
| **AArch32** | Historical context only | Arm docs — **not** a track |
| **RISC-V** | Optional glance — load/store + psABI taste | Shared `riscv-lite` — **does not** replace AArch64 |
| **Other (MIPS, AVR…)** | Out of scope | — |

**Why AArch64 first?** Edge ML + BCI targets: power/area/thermal, NEON/CMSIS-NN, LiteRT Micro.  
**Why keep x86_64?** PC host dumps + classic RE — one compare room, not opcode farm.  
**Why light RISC-V?** Open silicon literacy (`lw`/`sw`, `a0`); skip privileged ISA / Vector `V` / core design.

## Duration (± current formation)

Rough hours for **today’s** catalog (~100+ web/TUI rooms + craft bosses), at **4–6 h/week**.

| Slice | Study hours (±) | Calendar (±) |
|-------|-----------------|--------------|
| **Fundamentals** → Mago base | 25–40 h | 5–10 weeks |
| **Systems Mage** (systems + LLVM + bosses) | 50–90 h | 3–5 months |
| **Edge ML Mage** | 30–50 h | 2–3 months |
| **Neurotech** (parallel circle, scaffold) | 35–55 h | 2–4 months |
| **Full path** → Mago Supremo | **~110–180 h** | **~6–10 months** |

Neurotech (`neurotech`) is a **parallel** course (BCI / EEG / physics / firmware). It does **not** replace Edge on-device or change **Mago Supremo** gates. SPEC: [`docs/SPEC-neurotech-course.md`](docs/SPEC-neurotech-course.md) · track: `content/tracks/10-neurotech/` (22 rooms F0→F6). Pedagogy: **Estuda → Sala**. TUI: `mage --course neurotech` · emulators: `mage emu all`.

Faster if you already code; slower on a first terminal/C contact.

> **The curriculum is meant to evolve.** Rooms, bosses, and electives (e.g. RISC-V) will be added or retired. Treat these numbers as a snapshot of the *current* formation, not a fixed diploma workload. The skill target (table above) stays; the path gets sharper over time.

## Courses

| id | Course | Role |
|----|--------|------|
| `fundamentals` | Fundamentals | Path to **Mago base** (shared core + clearance) |
| `systems` | Systems Mage | **Full FLAG catalog** in TUI: systems + llvm + math (same scope as web Systems Mage core) |
| `edge` | Edge ML Mage | Current math → on-device Edge AI tracks (full TUI UX) — **ARM-first** unchanged |
| `neurotech` | Neurotech | Parallel BCI/EEG — `mage --course neurotech` · `mage emu all` (not a Mago Supremo gate) |

`mage` opens a **course launcher** first (plus GitHub connect stub). Systems/Edge are soft-gated behind Mago base (preview allowed with a warning).

### Systems Mage on the TUI

Opening **Systems** loads many FLAG rooms offline (not a hello stub):

- Bundled snapshot: `content/packs/systems.json` (exported from edevs `systems.ts` / `llvm.ts` / `math.ts`)
- Install seeds `~/.mage/packs/systems.json` so first launch is full
- Phases as tracks: **systems** · **llvm** · **math** · **craft** (`boss-craft` + `shared-math-evidence` stay as Edge-rich YAML rituals)
- Shared cores (`vectors`, `bits`, …) still credit once via `room_id`
- `mage sync` / `:sync` refreshes the pack from `GET /api/estudo/mage/catalog` (`systemsMagePack`) when online; offline keeps the bundled catalog

Edge ML Mage stays the ARM-deep on-device path — Systems does **not** replace Edge AI tracks.

Shared core rooms live under `content/shared/` (`vectors`, `bits`, `intro-asm`, `isa-x86-aarch64`, `riscv-lite`) with stable `room_id` credit.

Portable curriculum indexes + shared room JSON: sibling repo **[edevPedro/emage-content](https://github.com/edevPedro/emage-content)** (`SYNC.md` there). Clone beside this tree or set `EMAGE_CONTENT_ROOT`.

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
- Packs cache: `~/.mage/packs/` — Systems ships with a full FLAG pack on install (`content/packs/systems.json` → `systems.json`)
- Auth stub: `~/.mage/auth.json`
- `mage sync` / `:sync` — pull Systems pack from `{MAGE_API_BASE}/api/estudo/mage/catalog` (writes `systemsMagePack`) + POST progress to `/api/estudo/mage/progress` (default API base `https://edevs.com`). If offline, keeps/seeds the bundled pack.

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
