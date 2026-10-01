# Edge Mage

Você abre o terminal. Não o Notion.

Academia TUI — teclado estilo **Neovim**, salão por salão — da trigonometria
até o low-level de **Edge AI**. XP existe. Título **Edge Mage** não: esse
só vem com ritual on-device de verdade.

```text
┌─ edge-mage ───────────────────────────────────────────── NORMAL · HISTÓRIA ─┐
│  Sala: trigonometria                                          ✧ 3/28       │
│                                                                              │
│  O portal gira. Sem seno/cosseno você não atravessa.                         │
│  j/k scroll · l abre · :daily · g r grimório                                 │
│                                                                              │
│      ·  braille unit circle  ·                                               │
│                                                                              │
│  -- NORMAL ----------------------------------------------------------------- │
│  :continue                                                                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

[![license](https://img.shields.io/badge/license-MIT-1c1c1c?style=flat-square)](LICENSE)
[![python](https://img.shields.io/badge/python-3.11%2B-1c1c1c?style=flat-square)](pyproject.toml)
[![tests](https://img.shields.io/github/actions/workflow/status/edevPedro/edge-mage/test.yml?branch=main&style=flat-square&label=tests)](https://github.com/edevPedro/edge-mage/actions)

*EN: terminal RPG-academy for math → on-device Edge AI. Vim keys. Earned rank.*

---

## O que é

Curso jogável no terminal (Textual). 28+ salas + bosses. Cada sala: **História → Conceito → Desafio → Anim → Tasks**. Progresso em `~/.edge-mage/`.

O loop:

1. **Quiz** — MCQ/num, feedback rápido, cerimônia `+XP`
2. **Feitiço** — código no sandbox (3s)
3. **Ritual** — boss / artefato em `study-log/artifacts/`

Mapa longo: [`content/CURRICULUM.md`](content/CURRICULUM.md) · spec do loop: [`SPEC-edge-mage-loop.md`](SPEC-edge-mage-loop.md)

---

## Instalar

Uma linha (macOS / Linux):

```bash
curl -fsSL https://raw.githubusercontent.com/edevPedro/edge-mage/main/install.sh | bash
```

Ou clone:

```bash
git clone https://github.com/edevPedro/edge-mage.git
cd edge-mage
./install.sh
# ou: make install
```

Isso pega Python **3.11+**, sobe um venv, e linka em `~/.local/bin`:

`mage` · `emage` · `edge-mage`

Se o shell reclamar de PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

Checagem de qualquer pasta:

```bash
cd /tmp && mage --version && mage
```

Dev / testes: `make install-dev` · `make test`  
Alternativa: `USE_PIPX=1 ./install.sh`

---

## Comandos (NORMAL)

| Tecla | Ação |
|-------|------|
| `j` `k` `h` `l` / Enter | navegar |
| `i` | INSERT (responder) |
| `:` | command line |
| `Ctrl+w` + `w`/`h`/`l` | painéis |
| `g` + `p`/`r`/`t`/`h` | perfil / grimório / trilhas / home |
| `Space` | anim on/off |
| `M` | mastery (sala limpa) |
| `q` | sair |

Úteis em `:` → `:continue` · `:daily` · `:grimorio` · `:sync` · `:help`

Run de hoje (`:daily`): review + task nova (~20 min). Streak ≥ 3 → mana XP ×1.25.

---

## Rank Edge Mage

| Rank | O que falta |
|------|-------------|
| Noviço → Arquimago | XP |
| **Edge Mage** | XP ≥ 2900 **e** ritual on-device (`study-log/artifacts/on-device.md`) |

Sem o checklist, você fica Arquimago mesmo com XP alto. De propósito.

---

## Diário no git (opcional)

Primeira conclusão de task → linha em `study-log/completions.jsonl` + commit/push (se tiver `origin`). Refazer não spamava. `:sync` pra pendência.

Desligar: `~/.edge-mage/config.json` → `"auto_git_push": false`.

---

## Contribuir

Sala nova: `content/tracks/<trilha>/rooms/<id>/` com `story.md` + `concept.md` + `lesson.md` + `room.yaml`, skill em `content/grimoire/skills.yaml`.

Código de desafio: subprocess + timeout + denylist. Não é sandbox militar — é pra math → edge inference.

```bash
make install-dev && make test
```

MIT · Python 3.11+ · terminal com Unicode (braille ajuda)
