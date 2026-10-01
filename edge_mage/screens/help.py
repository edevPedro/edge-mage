"""Tela de ajuda (:help)."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from edge_mage.commands import help_text
from edge_mage.screens.base import MageScreen


class HelpScreen(MageScreen):
    context_label = "help"
    list_id = "help-actions"

    def compose_body(self) -> ComposeResult:
        with VerticalScroll(can_focus=False):
            yield Static("AJUDA", classes="title")
            yield Static(help_text(), classes="panel", id="help-body")
            yield OptionList(Option("←  Voltar", id="back"), id="help-actions")

    def on_mount(self) -> None:
        super().on_mount()
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if str(event.option.id) == "back":
            self.app.pop_screen()
