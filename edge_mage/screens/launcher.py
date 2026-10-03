"""Course launcher — first screen for `mage`."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from edge_mage.courses import (
    COURSE_EDGE,
    COURSE_FUNDAMENTALS,
    COURSE_NEUROTECH,
    COURSE_SYSTEMS,
    COURSES,
)
from edge_mage.screens.base import MageScreen

BANNER = r"""
╔══════════════════════════════════════════════════╗
║         e - m a g e   ·   LAUNCHER               ║
║   Fundamentals · Systems · Edge · Neurotech      ║
╚══════════════════════════════════════════════════╝
"""


class LauncherScreen(MageScreen):
    context_label = "launcher"
    list_id = "launcher-menu"

    def action_vim_back(self) -> None:
        return

    def compose_body(self) -> ComposeResult:
        store = self.app.store  # type: ignore[attr-defined]
        profile = store.profile_summary()
        g = profile.get("global_rank")
        mago = "✓ Mago base" if profile.get("mago_base") else "○ Mago base pendente"
        g_title = g.title if g else "Sem rank"

        with Vertical():
            yield Static(BANNER, id="banner")
            yield Static("CURSOS", classes="panel-title")
            yield Static(
                f"Rank global: [{g_title}]  ·  {mago}",
                classes="rank",
            )
            yield Static(
                "Systems/Edge/Neurotech: soft gate — preview OK sem Mago base.",
                classes="muted",
            )
            yield Static("j/k · Enter  ·  q sair", classes="muted")
            options: list[Option] = []
            for c in COURSES:
                lock = ""
                if c.requires_mago_base and not profile.get("mago_base"):
                    lock = "  [? preview]"
                options.append(
                    Option(f"{c.title_pt}{lock}  —  {c.blurb}", id=c.id)
                )
            options.append(Option("⌥  Conectar GitHub (device flow stub)", id="github"))
            options.append(Option("↻  Sync packs / progress", id="sync"))
            options.append(Option("✕  Sair", id="quit"))
            yield OptionList(*options, id="launcher-menu")

    def on_mount(self) -> None:
        super().on_mount()
        app = self.app
        if hasattr(app, "set_nav_context"):
            app.set_nav_context("launcher")  # type: ignore[attr-defined]
        if hasattr(app, "enter_normal"):
            app.enter_normal()  # type: ignore[attr-defined]

    def _enter(self, course_id: str, *, preview: bool) -> None:
        app = self.app
        enter = getattr(app, "enter_course", None)
        if callable(enter):
            enter(course_id, preview=preview)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        oid = str(event.option.id)
        store = self.app.store  # type: ignore[attr-defined]
        mago = bool(store.profile_summary().get("mago_base"))

        if oid == "quit":
            self.app.exit()
            return
        if oid == "github":
            from edge_mage.auth import github_connect_instructions

            msg = github_connect_instructions()
            self.app.notify(msg.split("\n")[0], severity="information")
            # full text on a simple overlay screen
            from edge_mage.screens.github_auth import GitHubAuthScreen

            self.app.push_screen(GitHubAuthScreen())
            return
        if oid == "sync":
            from edge_mage.sync import sync_all

            result = sync_all()
            sev = "information" if result.ok else "warning"
            self.app.notify(result.message, severity=sev)
            if result.warning:
                self.app.notify(result.warning[:120], severity="warning")
            return

        if oid in {COURSE_FUNDAMENTALS, COURSE_SYSTEMS, COURSE_EDGE, COURSE_NEUROTECH}:
            preview = False
            if oid != COURSE_FUNDAMENTALS and not mago:
                preview = True
                self.app.notify(
                    "Sem Mago base — entrando em preview. "
                    "Conclua Fundamentals para liberar o caminho completo.",
                    severity="warning",
                )
            self._enter(oid, preview=preview)

    def open_default(self) -> None:
        lst = self._option_list()
        if lst is not None:
            lst.action_select()
