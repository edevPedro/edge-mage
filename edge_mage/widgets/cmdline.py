"""Linha de comando `:` (estilo Vim)."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.screen import ModalScreen
from textual.widgets import Input, Static


class CmdlineScreen(ModalScreen[str | None]):
    """Modal discreto no rodapé para digitar comandos colon."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancelar", show=False),
    ]

    CSS = """
    CmdlineScreen {
        align: left bottom;
        background: transparent;
    }
    #cmdline-bar {
        dock: bottom;
        height: 1;
        width: 100%;
        background: #0c1014;
        layout: horizontal;
    }
    #cmdline-prompt {
        width: auto;
        color: #e6c07b;
        text-style: bold;
        padding: 0 0 0 1;
    }
    #cmdline-input {
        width: 1fr;
        border: none;
        background: #0c1014;
        padding: 0;
    }
    #cmdline-input:focus {
        border: none;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal(id="cmdline-bar"):
            yield Static(":", id="cmdline-prompt")
            yield Input(placeholder="q  tracks  profile  room <id>  help  xp", id="cmdline-input")

    def on_mount(self) -> None:
        self.query_one("#cmdline-input", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if not text:
            self.dismiss(None)
            return
        if not text.startswith(":"):
            text = ":" + text
        self.dismiss(text)

    def action_cancel(self) -> None:
        self.dismiss(None)
