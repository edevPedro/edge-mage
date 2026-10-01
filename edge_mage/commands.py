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

NAVEGAÇÃO (NORMAL)
  j / k       descer / subir na lista
  h / Esc     voltar (Esc em INSERT → NORMAL)
  l / Enter   abrir item / confirmar
  g g         topo da lista
  G           fim da lista
  Space       toggle animação matemática (salas com visual)
  i           entrar em INSERT (tela de task)

LEADER (g + tecla)
  g p         perfil
  g t         trilhas
  g h         home

COMANDOS (:)
  :q / :sair          sair
  :tracks / :trilhas  lista de trilhas
  :profile / :perfil  perfil e ranks
  :home               tela inicial
  :room <id>          abrir sala pelo id
  :anim [kind]        toggle animação (unit_circle|sine_wave|vector|matrix)
  :xp                 mostrar XP / rank
  :sync               commit/push pendente do diário (study-log)
  :help / :ajuda      esta ajuda

OUTROS
  q                   sair (fora de INSERT)
  ?                   ajuda
  :                   abrir linha de comando

TASKS
  Começa em NORMAL. i ou «Editar» → INSERT.
  Esc sai de INSERT sem perder o texto.
  Enter no campo (não-code) verifica a resposta.
"""
