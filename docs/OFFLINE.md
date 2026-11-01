# Offline study — e-mage on your machine

No network required for the core journey after install dependencies are present.

## One-time setup (can be done once while online)

```bash
cd /Users/epedro/eCodes/edevs/edge-mage
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
# optional: make install-dev  → pytest tooling
```

Or: `./install.sh` (links `mage` / `emage` / `edge-mage` into `~/.local/bin`).

## Daily offline

```bash
source /Users/epedro/eCodes/edevs/edge-mage/.venv/bin/activate
mage --course emage
# or: python -m edge_mage --course emage
# or: mage   → launcher → Continuar jornada
```

## What works offline

| Asset | Location |
|-------|----------|
| Journey content | `content/tracks/`, `content/courses/`, `content/shared/` |
| Systems FLAG pack | `content/packs/systems.json` (seeded to `~/.mage/packs/` on install) |
| Progress / ranks | `~/.mage/progress.json` |
| Forge cumulative project | `content/tracks/12-emage-forge/` |
| Pedagogy | Estuda (`concept.md`) → Sala (tasks) — foundations in-repo |

## Optional when online

- `mage sync` — refresh Systems pack + push progress
- Web Estudo mirror — CTA only; TUI remains source of truth
- GitHub device-auth stub

## Pedagogy reminder

Do not skip Estuda. NEON / Metal / inference / RTL rooms assume prior arch/memory/numerics foundations — enforced by `requires_rooms` and written into `concept.md`.
