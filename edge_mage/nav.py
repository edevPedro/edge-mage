"""Modos de navegação estilo Neovim e helpers de teclado."""

from __future__ import annotations

from enum import Enum


class NavMode(str, Enum):
    NORMAL = "NORMAL"
    INSERT = "INSERT"
    COMMAND = "COMMAND"
    LEADER = "G-"
    WINDOW = "C-W"  # após Ctrl+w: w cicla, h/j/k/l move painéis


# Nomes curtos dos painéis (statusline)
PANE_LABELS = {
    "story": "HISTÓRIA",
    "concept": "CONCEITO",
    "desafio": "DESAFIO",
    "anim": "ANIM",
    "tasks": "TAREFAS",
    "prompt": "PROMPT",
    "answer": "RESPOSTA",
    "actions": "AÇÕES",
}


def mode_label(mode: NavMode | str) -> str:
    if isinstance(mode, NavMode):
        return mode.value
    return str(mode)


def is_insert_like(mode: NavMode | str) -> bool:
    label = mode_label(mode).upper()
    return label in {"INSERT", "COMMAND"}


# Teclas de navegação que o App trata em NORMAL (não em INSERT/COMMAND).
VIM_NAV_KEYS = frozenset(
    {
        "j",
        "k",
        "h",
        "l",
        "g",
        "G",
        "enter",
        "escape",
        "space",
        "i",
    }
)
