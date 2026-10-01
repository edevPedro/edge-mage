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

## UX estilo Neovim

### Modos (statusline)

| Modo | Quando | Comportamento |
|------|--------|----------------|
| **NORMAL** | padrão / após Esc | `j/k/h/l`, leader, `:` — navega sem mouse |
| **INSERT** | `i` na task ou menu «Editar» | digitar resposta; Esc → NORMAL |
| **COMMAND** | após `:` | linha de comando |
| **G-** | após `g` | espera 2ª tecla (`gg`, `gp`, `gt`, `gh`) |

### Navegação (NORMAL)

| Tecla | Ação |
|-------|------|
| `j` / `k` | descer / subir na lista |
| `h` / `Esc` | voltar (Esc em INSERT → NORMAL) |
| `l` / `Enter` | abrir item |
| `gg` | topo da lista |
| `G` | fim da lista |
| `Space` | toggle animação matemática (salas com visual) |
| `i` | INSERT (tela de task) |
| `q` | sair (fora de INSERT) |
| `?` | ajuda |

### Leader (`g` + tecla)

| Sequência | Ação |
|-----------|------|
| `gp` | perfil |
| `gt` | trilhas |
| `gh` | home |

### Comandos `:`

| Comando | Efeito |
|---------|--------|
| `:q` / `:sair` | sair |
| `:tracks` / `:trilhas` | trilhas |
| `:profile` / `:perfil` | perfil |
| `:home` | tela inicial |
| `:room <id>` | abrir sala (ex.: `:room trigonometria`) |
| `:anim [kind]` | toggle animação (`unit_circle`, `sine_wave`, `vector`, `matrix`) |
| `:xp` | notificar XP / rank |
| `:help` / `:ajuda` | ajuda |

## Animações matemáticas

Salas de Fundamentos (e algumas de Física/Robótica) abrem um painel braille/ASCII (~12 fps):

| Animação | Salas |
|----------|--------|
| **unit_circle** | Trigonometria — raio varrendo θ, cos/sin |
| **sine_wave** | Ondas — seno/cosseno com fase |
| **vector** | Vetores — seta + componentes |
| **matrix** | Álgebra linear / Transforms 2D — R(θ)·diag |

Controles: `Space` ou `:anim` / `:anim sine_wave`.

## Progressão (ranks)

| Rank | XP mín. |
|------|---------|
| Noviço | 0 |
| Aprendiz | 80 |
| Adepto | 220 |
| Evocador | 450 |
| Mago | 800 |
| Arquimago | 1300 |
| **Edge Mage** | 2000 |

## Trilhas

1. **Fundamentos** — trig, vetores, álgebra linear (+ animações)
2. **Programação** — desafios Python
3. **Física & Sinais** — cinemática, ondas, amostragem
4. **Elétrica Edge** — Ohm, divisor, ADC
5. **Robótica** — transforms 2D, cinemática, sensores
6. **Otimização** — gradiente, loss, LR
7. **ML Math** — softmax, matmul, quantização
8. **Edge AI Low-Level** — layout, SIMD, on-device

## Adicionar uma sala

1. `content/tracks/<trilha>/rooms/<id>/`
2. `lesson.md` + `room.yaml` (opcional `animation: unit_circle|sine_wave|vector|matrix`)
3. Tasks: `mcq` | `numeric` | `fill` | `code`

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
