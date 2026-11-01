# e-mage

Terminal academy (Textual TUI): **one continuous journey** from low-level performance engineering through CPU arch → SIMD → HPC → GPU → inference optimization → HW/SW co-design.  
Legacy labels (Systems / Performance / Edge / Neurotech) are **phases or branches**, not competing course picks.  
Product name: **e-mage**. GitHub: [edevPedro/edge-mage](https://github.com/edevPedro/edge-mage).  
CLI: `mage` · `emage` · `edge-mage` · primary id **`emage`**.

Architecture: [`docs/SPEC-emage-single-track.md`](docs/SPEC-emage-single-track.md) · pre-change diagnosis: [`docs/DIAGNOSTIC-emage-pre-unification.md`](docs/DIAGNOSTIC-emage-pre-unification.md).

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

### Journey phases (one path)

| Phase | Module label | Goal when done |
|-------|--------------|----------------|
| **P0** Foundations | shared core + clearance | *Mago base* — lab literacy + first craft |
| **P1** Systems | systems / llvm / math / craft | ABI/IR literacy + published craft evidence |
| **P2–P5** Arch → SIMD → HPC → GPU | Performance rooms | Measure → explain → prove (NEON / Roofline / Metal) |
| **P6** Inference | Edge ML tracks + bridge | On-device ritual with latency/RAM evidence |
| **P7** Co-design | RTL/HLS lite | Pedagogical accelerator boss (FPGA board optional) |
| **Forge** | cumulative project | Same motif evolves scalar→SIMD→Metal→inference |
| **Branch** Neurotech | optional | BCI/EEG circle — alternate Supremo route; not the home UX |

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

## Duration (± single journey)

Sustainable **1–3 year** path at **4–8 h/week**. Spine (P0–P7 + Forge) ≈ **400–650 h** guided; enrichment + Neurotech + denser labs push the upper end.

| Slice | Study hours (±) | Notes |
|-------|-----------------|--------|
| **P0** Foundations | 25–40 h | → Mago base |
| **P1** Systems | 50–90 h | FLAG pack + craft |
| **P2–P5 + P7** Perf phases | ~200–280 h scaffold (aspirational denser band higher) | Arch→SIMD→HPC→GPU→co-design |
| **P6** Inference / Edge | 50–90 h | On spine **after** GPU foundations |
| **Forge** | overlap with phase bosses | Cumulative evidence |
| **Neurotech branch** | see Neurotech SPEC | Optional; not required for Edge Supremo |

**M4 caveats:** Apple µarch ≠ Cortex-A; no SVE on M4; Metal ≠ CUDA.  
Detail SPECs: [`SPEC-emage-single-track.md`](docs/SPEC-emage-single-track.md) · [`SPEC-performance-mage.md`](docs/SPEC-performance-mage.md) · [`SPEC-neurotech-course.md`](docs/SPEC-neurotech-course.md).

Faster if you already code; slower on a first terminal/C contact. Pro C++ ≠ automatic skip of arch/SIMD/GPU — progressive assessment.

> **The curriculum evolves.** Rooms and electives will be added or retired. Numbers are a snapshot, not a diploma contract.

## Journey & module browser

| id | Role |
|----|------|
| **`emage`** | **Primary journey** — all phases sequenced (`mage` / `mage --course emage`) |
| `fundamentals` | Module alias · P0 |
| `systems` | Module alias · P1 FLAG catalog |
| `performance` | Module alias · P2–P7 rooms as one track |
| `edge` | Module alias · P6 Edge ML tracks |
| `neurotech` | **Branch** · optional BCI/EEG (`mage emu all`) |

`mage` opens the launcher: **Continue journey** first; legacy ids live under the module browser (soft-gated behind Mago base; preview OK).

### Systems phase on the TUI

Opening the journey (or **Systems** module alias) loads many FLAG rooms offline (not a hello stub):

- Bundled snapshot: `content/packs/systems.json` (exported from edevs `systems.ts` / `llvm.ts` / `math.ts`)
- Install seeds `~/.mage/packs/systems.json` so first launch is full
- Phases as tracks: **systems** · **llvm** · **math** · **craft** (`boss-craft` + `shared-math-evidence` stay as Edge-rich YAML rituals)
- Shared cores (`vectors`, `bits`, …) still credit once via `room_id`
- `mage sync` / `:sync` refreshes the pack from `GET /api/estudo/mage/catalog` (`systemsMagePack`) when online; offline keeps the bundled catalog

Inference (Edge ML) stays the ARM-deep on-device **phase** after GPU foundations — Systems does **not** replace it.

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

## Study offline (M4 / no network)

TUI is the **source of truth**. Lessons live under `content/` (`story.md` · `concept.md` · `lesson.md` · `room.yaml`). External links are optional further reading — Estuda must teach the foundation before Sala.

```bash
cd /Users/epedro/eCodes/edevs/edge-mage
python3 -m venv .venv && source .venv/bin/activate   # once
pip install -e ".[dev]"                              # or: make install-dev
mage --course emage                                  # primary journey
# equivalents:
python -m edge_mage --course emage
mage                    # launcher → Continuar jornada
```

| Offline | Online-only (optional) |
|---------|------------------------|
| All Estuda/Sala/Forge content in `content/` | `mage sync` catalog refresh |
| Bundled Systems pack `content/packs/systems.json` | GitHub device-auth stub |
| Progress `~/.mage/` | POST progress to edevs API |
| Labs/spells with local compiler/Python | Web Estudo mirror |

**M4 caveats stay in-portal:** µarch ≠ Cortex-A; no SVE; Metal ≠ CUDA.

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
| `:publish <boss>` | build `ARTIFACT/<boss>/` (does not send/push) |
| `q` | quit |

## Boss artifacts (`mage publish`)

Every boss produces a GitHub-ready `ARTIFACT/<boss>/`:

```bash
mage publish                 # list bosses + ritual/published status
mage publish on-device       # validate ritual, then generate the artifact
```

It writes a one-page `README.md` with the sections **O que medi / O que me
surpreendeu / O que faria depois** (+ reproduction steps), an `evidence.json`,
and ASCII charts built from the evidence log (`study-log/completions.jsonl`).
It **never** sends or pushes anything — it prints the next git steps.

Content stays clean by design: no proprietary code, internal protocols, or real
employer/broker data. Theory rooms are short and every room ships a verifiable
exercise (not MCQ-only); `scripts/lint_resources.py` enforces this.

## Ranks

Ranks climb only with an **approved boss + published artifact** — XP keeps
accruing, but alone it hits a ceiling (`mage publish <boss>` is the gate).

**Global:** none → **Mago base** (Fundamentals clear) → intermediate (≥1
published boss) → **Mago Supremo** (systems Boss craft + edge on-device + shared
math, all published; or the Neurotech MSc route).

**Edge course (internal):** Novice → … → Archmage (XP ceiling) → **Edge Mage**
(XP ≥ 2900 **and** on-device ritual **and** `mage publish on-device`).

## Quality & CI

- Runner tests (`tests/test_runner_sandbox.py`): PASS, FAIL, timeout, broken
  compilation, and high-noise output (capped at 20k chars).
- GitHub Actions runs `pytest`, `scripts/lint_resources.py`, and a Linux
  `scripts/benchmark_smoke.py` runner benchmark.


## License

MIT · Python 3.11+ · Unicode-capable terminal recommended
