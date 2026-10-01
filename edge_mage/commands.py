"""Parser de comandos estilo Vim (`:q`, `:tracks`, …)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedCommand:
    """Comando colon normalizado."""

    name: str
    args: tuple[str, ...] = ()
    error: str | None = None
    raw: str = ""


# nome canônico → aliases aceitos
_ALIASES: dict[str, str] = {
    "q": "quit",
    "quit": "quit",
    "sair": "quit",
    "qa": "quit",
    "tracks": "tracks",
    "trilhas": "tracks",
    "t": "tracks",
    "profile": "profile",
    "perfil": "profile",
    "p": "profile",
    "home": "home",
    "h": "home",
    "room": "room",
    "sala": "room",
    "help": "help",
    "ajuda": "help",
    "?": "help",
    "xp": "xp",
    "anim": "anim",
    "animation": "anim",
    "sync": "sync",
    "grimoire": "grimoire",
    "grimorio": "grimoire",
    "grimório": "grimoire",
    "grim": "grimoire",
    "daily": "daily",
    "hoje": "daily",
    "run": "daily",
    "continue": "continue",
    "continuar": "continue",
    "c": "continue",
    "courses": "courses",
    "cursos": "courses",
    "launcher": "launcher",
}


KNOWN_COMMANDS = sorted(set(_ALIASES.values()))


def parse_command(line: str) -> ParsedCommand:
    """
    Interpreta uma linha de comando (com ou sem `:` inicial).

    Exemplos:
      :q  → quit
      :room trigonometria  → room ["trigonometria"]
      :  → erro
    """
    raw = line if line is not None else ""
    text = raw.strip()
    if text.startswith(":"):
        text = text[1:].strip()
    if not text:
        return ParsedCommand(name="", error="comando vazio", raw=raw)

    parts = text.split()
    head = parts[0].lower()
    args = tuple(parts[1:])
    canonical = _ALIASES.get(head)
    if canonical is None:
        return ParsedCommand(
            name=head,
            args=args,
            error=f"comando desconhecido: {head}",
            raw=raw,
        )
    if canonical == "room" and not args:
        return ParsedCommand(
            name=canonical,
            args=args,
            error="uso: :room <id>",
            raw=raw,
        )
    return ParsedCommand(name=canonical, args=args, raw=raw)


def help_text() -> str:
    """Texto de :help (PT-BR)."""
    return """\
EDGE MAGE — atalhos (estilo nvim)

MODOS (statusline)
  NORMAL      navegar listas / telas (padrão)
  INSERT      digitar resposta na task (i ou menu)
  COMMAND     linha : (após :)
  G-          leader aguardando 2ª tecla (após g)
  C-W         modo janela (após Ctrl+w)

PAINÉIS (Ctrl+w) — salas e tasks
  Ctrl+w w    ciclar painel (História→Conceito→Desafio→Anim→Tarefas)
  Ctrl+w h/l  painel anterior / próximo
  Ctrl+w j/k  idem (layout linear)
  j / k       scroll no painel de texto · navegar opções em Tarefas
  Statusline  mostra o painel focado (HISTÓRIA, CONCEITO, …)

NAVEGAÇÃO (NORMAL)
  j / k       descer / subir (lista ou scroll)
  h / Esc     voltar (Esc em INSERT/C-W → NORMAL)
  l / Enter   abrir item / confirmar
  g g         topo
  G           fim
  Space       toggle animação
  i           INSERT (tela de task)

LEADER (g + tecla)
  g p         perfil
  g r         grimório
  g t         trilhas
  g h         home

COMANDOS (:)
  :q / :sair          sair
  :tracks / :trilhas  lista de trilhas
  :continue / :c      próxima porta pedagógica
  :daily / :hoje      run de hoje (~20 min)
  :profile / :perfil  perfil e ranks
  :grimorio / :grim   grimório de habilidades
  :home               tela inicial
  :room <id>          abrir sala pelo id
  :anim [kind]        toggle animação
  :xp                 XP / rank / skills / mana
  :sync               packs + progress API + diário git
  :courses / :cursos  launcher de cursos
  :help / :ajuda      esta ajuda

LOOP
  quiz (MCQ/num) → feitiço (code+tests) → ritual (artifact/boss)
  Edge course: Edge Mage = XP≥2900 + checklist on-device
  Global: Mago base (Fundamentals) → Mago Supremo (evidence)
  Mastery: M numa sala limpa (3/3)
  Streak≥3 → mana ×1.25
"""
