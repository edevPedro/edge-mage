"""Statusline estilo Neovim (modo · contexto · XP · rank)."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Static


class StatusLine(Widget):
    """Barra inferior: modo | contexto | XP | rank."""

    DEFAULT_CSS = """
    StatusLine {
        dock: bottom;
        height: 1;
        background: #12181e;
        color: #a8b2bc;
    }
    StatusLine Horizontal {
        height: 1;
        width: 1fr;
    }
    StatusLine #sl-mode {
        width: auto;
        min-width: 10;
        background: #1a222a;
        color: #d8dee4;
        text-style: bold;
        padding: 0 1;
    }
    StatusLine #sl-mode.-command {
        background: #2a2418;
        color: #e6c07b;
    }
    StatusLine #sl-mode.-leader {
        background: #1a2420;
        color: #9ece6a;
    }
    StatusLine #sl-mode.-insert {
        background: #1a2030;
        color: #7aa2f7;
    }
    StatusLine #sl-ctx {
        width: 1fr;
        color: #8b949e;
        padding: 0 1;
    }
    StatusLine #sl-xp {
        width: auto;
        color: #9ece6a;
        padding: 0 1;
    }
    StatusLine #sl-rank {
        width: auto;
        color: #c9a227;
        text-style: bold;
        padding: 0 1;
    }
    StatusLine #sl-skills {
        width: auto;
        color: #9db8a5;
        padding: 0 1;
    }
    """

    can_focus = False

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Static(" NORMAL ", id="sl-mode")
            yield Static("", id="sl-ctx")
            yield Static("", id="sl-skills")
            yield Static("", id="sl-xp")
            yield Static("", id="sl-rank")

    def set_status(
        self,
        *,
        mode: str = "NORMAL",
        context: str = "",
        xp: int = 0,
        rank: str = "",
        skills: str = "",
    ) -> None:
        mode_w = self.query_one("#sl-mode", Static)
        upper = mode.upper()
        label = f" {upper} "
        mode_w.update(label)
        mode_w.set_class(upper.startswith("COMMAND"), "-command")
        mode_w.set_class(upper.startswith("G-") or upper == "LEADER", "-leader")
        mode_w.set_class(upper == "INSERT", "-insert")
        mode_w.set_class(upper.startswith("C-W") or upper == "WINDOW", "-leader")
        self.query_one("#sl-ctx", Static).update(context)
        self.query_one("#sl-skills", Static).update(skills)
        self.query_one("#sl-xp", Static).update(f"XP:{xp}")
        self.query_one("#sl-rank", Static).update(rank)
