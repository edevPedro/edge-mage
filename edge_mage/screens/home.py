"""Tela inicial / dashboard — navegável por teclado (OptionList)."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from edge_mage.curriculum import continue_label, next_open_room
from edge_mage.ranks import xp_for_next_level
from edge_mage.screens.base import MageScreen

BANNER = r"""
╔══════════════════════════════════════════════════╗
║      E D G E   M L   M A G E   ·   ACADEMIA      ║
║   quiz → feitiço → ritual   ·   Ctrl+w painéis   ║
╚══════════════════════════════════════════════════╝
"""


class HomeScreen(MageScreen):
    context_label = "home"
    list_id = "home-menu"

    def action_vim_back(self) -> None:
        stack = self.app.screen_stack
        if len(stack) <= 1:
            return
        # allow return to course launcher
        prev = stack[-2] if len(stack) >= 2 else None
        from edge_mage.screens.launcher import LauncherScreen

        if isinstance(prev, LauncherScreen):
            self.app.pop_screen()
            return
        if len(stack) <= 2:
            return
        self.app.pop_screen()

    def compose_body(self) -> ComposeResult:
        store = self.app.store  # type: ignore[attr-defined]
        tracks = self.app.tracks  # type: ignore[attr-defined]
        course = getattr(self.app, "course", None) or "edge"
        if course == "fundamentals":
            banner = (
                "╔══════════════════════════════════════════════════╗\n"
                "║      F U N D A M E N T A L S  ·  MAGO BASE       ║\n"
                "║   shared core → clear → unlock Systems / Edge    ║\n"
                "╚══════════════════════════════════════════════════╝"
            )
        elif course == "systems":
            banner = (
                "╔══════════════════════════════════════════════════╗\n"
                "║      S Y S T E M S   M A G E  ·  FLAG-lab         ║\n"
                "║   systems+llvm+math · craft · :sync              ║\n"
                "╚══════════════════════════════════════════════════╝"
            )
        else:
            banner = BANNER
        profile = store.profile_summary()
        rank = profile["rank"]
        into, need = xp_for_next_level(profile["xp"])
        if need:
            filled = int(20 * into / need) if need else 0
            bar = "█" * filled + "░" * (20 - filled)
            bar_line = f"Nível {profile['level']}  [{bar}]  {into}/{need} XP"
        else:
            bar_line = f"Nível {profile['level']}  [████████████████████]  CAP"

        mult = float(profile.get("mult") or 1.0)
        combo = int(profile.get("combo") or 0)
        mana = f"  ·  mana ×{mult:.2f}" if mult > 1 else ""
        combo_s = f"  ·  combo {combo}/4" if combo else ""
        od = "  ·  ritual on-device ✓" if profile.get("on_device") else ""

        with Vertical():
            yield Static(banner, id="banner")
            yield Static("STATUS DO MAGO", classes="panel-title")
            yield Static(
                f"Rank: [{rank.title}]  ·  XP: {profile['xp']}  ·  "
                f"Streak: {profile['streak']}d{mana}{combo_s}{od}",
                classes="rank",
            )
            yield Static(bar_line, id="xp-bar")
            yield Static(rank.blurb, classes="muted")
            nxt = profile["next_rank"]
            if nxt:
                extra = ""
                if nxt.id == "edge_mage" and not profile.get("on_device"):
                    extra = " + ritual on-device"
                yield Static(
                    f"Próximo: {nxt.title} (≥{nxt.min_xp} XP{extra})",
                    classes="accent",
                )
            yield Static(
                "j/k · Enter  ·  :continue  ·  :daily  ·  gr grimório",
                classes="muted",
            )
            yield OptionList(
                Option(continue_label(store, tracks), id="continue"),
                Option("☀  Run de hoje (~20 min)", id="daily"),
                Option("📚  Todas as trilhas", id="tracks"),
                Option("◆  Perfil / Ranks", id="profile"),
                Option("✧  Grimório", id="grimoire"),
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
        if oid == "continue":
            self.app.action_go_continue()  # type: ignore[attr-defined]
        elif oid == "daily":
            from edge_mage.screens.daily import DailyRunScreen

            self.app.push_screen(DailyRunScreen())
        elif oid == "tracks":
            from edge_mage.screens.tracks import TracksScreen

            self.app.push_screen(TracksScreen())
        elif oid == "profile":
            from edge_mage.screens.profile import ProfileScreen

            self.app.push_screen(ProfileScreen())
        elif oid == "grimoire":
            from edge_mage.screens.grimoire import GrimoireScreen

            self.app.push_screen(GrimoireScreen())
        elif oid == "help":
            from edge_mage.screens.help import HelpScreen

            self.app.push_screen(HelpScreen())
        elif oid == "quit":
            self.app.exit()

    def open_default(self) -> None:
        lst = self._option_list()
        if lst is not None:
            lst.action_select()
