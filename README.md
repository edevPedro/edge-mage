# Edge Mage

Academia TUI (terminal) gamificada: da **trigonometria** até a matemática e o low-level de **Edge AI** — temática Mage Academy / hacker-arcane. Interface estilo **Neovim** (teclado, modos NORMAL/INSERT, `:` comandos, statusline).

## Clone & instalação

```bash
git clone https://github.com/edevPedro/edge-mage.git
cd edge-mage
./install.sh
```

Isso cria/atualiza o venv do projeto, faz `pip install -e .` e coloca wrappers em `~/.local/bin` para:

| Comando | Alias |
|---------|--------|
| `edge-mage` | principal |
| `emage` | curto |
| `mage` | curto |

Garanta que `~/.local/bin` esteja no PATH (zsh):

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

Verificar de **qualquer** diretório:

```bash
cd /tmp && which edge-mage && edge-mage --version
```

### Alternativas

```bash
make install
USE_PIPX=1 ./install.sh   # ou: pipx install -e .
```

### Dev local

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
edge-mage
```

Progresso local em `~/.edge-mage/progress.json` (não versionado).

## Diário no GitHub (auto-commit)

Na **primeira** vez que você conclui uma task (validação OK, XP ganho), o Edge Mage:

1. acrescenta uma linha em [`study-log/completions.jsonl`](study-log/completions.jsonl) (`timestamp`, `track_id`, `room_id`, `task_id`, `xp_awarded`);
2. faz `git commit` só desse arquivo (mensagem em PT, ex.: `study: concluiu fundamentos/trigonometria — Quantos radianos?`);
3. faz `git push origin HEAD` se existir remote `origin` (sem force push).

Refazer a mesma task **não** gera commit (evita spam). Se commit ou push falhar (rede, credencial, repo sujo), o app mostra aviso na TUI e continua; use `:sync` para commitar/push pendente do ledger.

### Config (`~/.edge-mage/config.json`)

```json
{
  "auto_git_commit": true,
  "auto_git_push": true
}
```

- `auto_git_commit`: padrão `true` quando o app detecta um repositório git (cwd, pacote instalado ou `EDGE_MAGE_REPO_ROOT`).
- `auto_git_push`: padrão `true` quando há `origin`; desligue para só commit local.

### Push / credenciais

- Rode o jogo **dentro do clone** ou exporte `EDGE_MAGE_REPO_ROOT=/caminho/para/edge-mage`.
- `git` precisa estar no `PATH`; push usa sua autenticação habitual (SSH ou `gh auth`).
- Commits vão para a **branch atual** (em geral `main`), só com mudanças em `study-log/`.

## Loop: quiz → feitiço → ritual

1. **Quiz** (MCQ/num) — ensina, XP baixo, feedback rápido (cerimônia `+XP`)
2. **Feitiço** (`code` + `code_tests`) — aplica no sandbox (3s)
3. **Ritual** (boss / `study-log/artifacts/`) — prova fora do quiz

**Edge Mage** ≠ só XP: precisa XP ≥ 2900 **e** checklist on-device (`study-log/artifacts/on-device.md`). Ver [`SPEC-edge-mage-loop.md`](SPEC-edge-mage-loop.md).

| Home / comando | Efeito |
|----------------|--------|
| Continuar / `:continue` | próxima porta pedagógica |
| Run de hoje / `:daily` | review + task nova (~20 min, seed por data) |
| `M` na sala limpa | mastery 0..3 |
| Streak ≥ 3 | mana XP ×1.25 |

## UX estilo Neovim

### Modos (statusline)

| Modo | Quando | Comportamento |
|------|--------|----------------|
| **NORMAL** | padrão / após Esc | `j/k/h/l`, leader, `:` — navega sem mouse |
| **INSERT** | `i` na task ou menu «Editar» | digitar resposta; Esc → NORMAL |
| **COMMAND** | após `:` | linha de comando |
| **G-** | após `g` | espera 2ª tecla (`gg`, `gp`, `gt`, `gh`, `gr`) |
| **C-W** | após `Ctrl+w` | modo janela — próxima tecla move painéis |

### Painéis (`Ctrl+w`) — salas e tasks

Na sala: **História → Conceito → Desafio → Anim → Tarefas**. Na task: **Prompt → Resposta → Ações**.

| Tecla | Ação |
|-------|------|
| `Ctrl+w` então `w` | ciclar painel focado |
| `Ctrl+w` então `h` / `l` | painel anterior / próximo |
| `Ctrl+w` então `j` / `k` | idem (layout linear) |
| `j` / `k` no painel de texto | scroll (sem mouse) |
| `j` / `k` em Tarefas | navegar opções |

A statusline mostra o painel (`· HISTÓRIA`, `· CONCEITO`, …) e o contador do grimório (`✧n/28`).

### Navegação (NORMAL)

| Tecla | Ação |
|-------|------|
| `j` / `k` | descer / subir (lista ou scroll) |
| `h` / `Esc` | voltar (Esc em INSERT/C-W → NORMAL) |
| `l` / `Enter` | abrir item |
| `gg` | topo |
| `G` | fim |
| `Space` | toggle animação |
| `i` | INSERT (tela de task) |
| `q` | sair (fora de INSERT) |
| `?` | ajuda |

### Leader (`g` + tecla)

| Sequência | Ação |
|-----------|------|
| `gp` | perfil |
| `gr` | grimório |
| `gt` | trilhas |
| `gh` | home |

### Comandos `:`

| Comando | Efeito |
|---------|--------|
| `:q` / `:sair` | sair |
| `:tracks` / `:trilhas` | trilhas |
| `:profile` / `:perfil` | perfil |
| `:grimorio` / `:grim` | grimório de habilidades |
| `:home` | tela inicial |
| `:room <id>` | abrir sala (ex.: `:room trigonometria`) |
| `:anim [kind]` | toggle animação |
| `:xp` | XP / rank / skills |
| `:sync` | commit/push pendente do diário (`study-log/`) |
| `:help` / `:ajuda` | ajuda |

## História · Conceito · Desafio

Cada sala carrega:

| Arquivo | Aba / painel |
|---------|----------------|
| `story.md` | **História** — cenário; resolver a task = resolver o conflito |
| `concept.md` | **Conceito** — editorial pedagógico (estilo LeetCode) |
| `lesson.md` | **Desafio** — lição operacional + tasks |

## Grimório

Skills definidas em [`content/grimoire/skills.yaml`](content/grimoire/skills.yaml). Completar uma sala desbloqueia 1+ habilidades (ex.: *Trigonometria Arcana*, *Gradiente Descendente*, *Quantização Int8*). Abrir com `:grimorio`, `gr`, ou o menu Home. Persistido em `progress.json` (`unlocked_skills`).

## Animações TUI

Painel braille/ASCII (~12 fps) em **todas** as salas (kind no `room.yaml`):

| Kind | Uso típico |
|------|------------|
| `unit_circle` / `sine_wave` / `vector` / `matrix` | Fundamentos / ondas / matmul |
| `circuit_pulse` / `adc_ladder` | Ohm, divisor, ADC |
| `gradient_descent` / `derivative_slope` | Otimização |
| `softmax_bars` / `probability_bars` / `quantize_steps` | ML Math |
| `robot_transform` / `sampling_dots` | Robótica / amostragem |
| `memory_grid` | Edge AI layout / roofline |

Controles: `Space` ou `:anim` / `:anim softmax_bars`.

## Progressão (ranks)

| Rank | XP mín. | Ideia |
|------|---------|--------|
| Noviço | 0 | Trig e primeiros passos |
| Aprendiz | 100 | Vetores, exp/log, Python |
| Adepto | 280 | Álgebra linear + sinais |
| Evocador | 550 | Elétrica + robótica |
| Mago | 1100 | Derivadas / gradiente / batch |
| Arquimago | 1750 | Softmax, FLOPs, quantização |
| **Edge Mage** | 2900 + ritual on-device | Checklist real — não cosmético |

Mapa pedagógico: [`content/CURRICULUM.md`](content/CURRICULUM.md). Spec do loop: [`SPEC-edge-mage-loop.md`](SPEC-edge-mage-loop.md). XP total ≈ **3144+** (bosses).

## Trilhas

1. **Fundamentos** (0) — trig, vetores, exp/log, álgebra linear (+ code spells)
2. **Programação** (100) — Python alinhado à math
3. **Física & Sinais** (250) — cinemática, ondas, amostragem
4. **Elétrica Edge** (500) — Ohm, divisor, ADC
5. **Robótica** (800) — transforms 2D, cinemática, sensores
6. **Otimização** (1100) — derivadas, gradiente, loss/LR, batch
7. **ML Math** (1650) — probabilidade, softmax/CE, matmul/FLOPs, quantização
8. **Edge AI Low-Level** (2300 + ritual Softmax Estável) — layout, banda, SIMD, on-device
9. **Rituais (Boss)** (400+) — Codex Matricial, Softmax Estável, Quant Lab

28+ salas + 3 bosses. Skills no grimório (~31).
## Adicionar uma sala

1. `content/tracks/<trilha>/rooms/<id>/`
2. `story.md` + `concept.md` + `lesson.md` + `room.yaml` (`animation: …`)
3. Entrada em `content/grimoire/skills.yaml`
4. Tasks: `mcq` | `numeric` | `fill` | `code`

## Testes

```bash
.venv/bin/pytest -q
# inclui navegação vim via Textual Pilot + frames de animação
```

## Requisitos

- Python **3.11+**
- Terminal com cores e Unicode (braille)

## Segurança

Desafios de código rodam em subprocesso com timeout e bloqueio de imports/I/O perigosos. Foco: math → edge inference.
