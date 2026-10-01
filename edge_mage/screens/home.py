"""Tela inicial / dashboard — navegável por teclado (OptionList)."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from edge_mage.ranks import xp_for_next_level
from edge_mage.screens.base import MageScreen

BANNER = r"""
╔══════════════════════════════════════════════════╗
║      E D G E   M A G E   ·   ACADEMIA             ║
║   trig → vetores → ML math → inferência edge     ║
╚══════════════════════════════════════════════════╝
"""


class HomeScreen(MageScreen):
    context_label = "home"
    list_id = "home-menu"

    def action_vim_back(self) -> None:
        # Evita pop para a tela vazia inicial do App.
        if len(self.app.screen_stack) <= 2:
            return
        self.app.pop_screen()

    def compose_body(self) -> ComposeResult:
        store = self.app.store  # type: ignore[attr-defined]
        profile = store.profile_summary()
        rank = profile["rank"]
        into, need = xp_for_next_level(profile["xp"])
        if need:
            filled = int(20 * into / need) if need else 0
            bar = "█" * filled + "░" * (20 - filled)
            bar_line = f"Nível {profile['level']}  [{bar}]  {into}/{need} XP"
        else:
            bar_line = f"Nível {profile['level']}  [████████████████████]  CAP"

        with Vertical():
            yield Static(BANNER, id="banner")
            yield Static("STATUS DO MAGO", classes="panel-title")
            yield Static(
                f"Rank: [{rank.title}]  ·  XP: {profile['xp']}  ·  "
                f"Streak: {profile['streak']}d",
                classes="rank",
            )
            yield Static(bar_line, id="xp-bar")
            yield Static(rank.blurb, classes="muted")
            nxt = profile["next_rank"]
            if nxt:
                yield Static(
                    f"Próximo rank: {nxt.title} ({nxt.min_xp} XP)",
                    classes="accent",
                )
            yield Static(
                "j/k · Enter/l abrir  ·  :help  ·  gt trilhas  ·  gp perfil",
                classes="muted",
            )
            yield OptionList(
                Option("▶  Continuar / Trilhas", id="tracks"),
                Option("◆  Perfil / Ranks", id="profile"),
                Option("?  Ajuda", id="help"),
                Option("✕  Sair", id="quit"),
                id="home-menu",
            )

    def on_mount(self) -> None:
        super().on_mount()
        app = self.app
        if hasattr(app, "set_nav_context"):
            app.set_nav_context("home")  # type: ignore[attr-defined]
        if hasattr(app, "enter_normal"):
            app.enter_normal()  # type: ignore[attr-defined]

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        oid = str(event.option.id)
        if oid == "tracks":
            from edge_mage.screens.tracks import TracksScreen

            self.app.push_screen(TracksScreen())
        elif oid == "profile":
            from edge_mage.screens.profile import ProfileScreen

            self.app.push_screen(ProfileScreen())
        elif oid == "help":
            from edge_mage.screens.help import HelpScreen

            self.app.push_screen(HelpScreen())
        elif oid == "quit":
            self.app.exit()

    def open_default(self) -> None:
        lst = self._option_list()
        if lst is not None:
            lst.action_select()
