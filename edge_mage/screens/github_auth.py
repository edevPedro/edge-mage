"""GitHub connect stub screen."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Static

from edge_mage.auth import github_connect_instructions
from edge_mage.paths import auth_path
from edge_mage.screens.base import MageScreen


class GitHubAuthScreen(MageScreen):
    context_label = "github"
    list_id = None

    def action_vim_back(self) -> None:
        self.app.pop_screen()

    def action_vim_open(self) -> None:
        self.app.pop_screen()

    def compose_body(self) -> ComposeResult:
        text = github_connect_instructions()
        with Vertical():
            yield Static("CONECTAR GITHUB", classes="panel-title")
            with VerticalScroll():
                yield Static(text, id="github-help")
            yield Static(
                f"Auth file: {auth_path()}  ·  h/Esc voltar",
                classes="muted",
            )
