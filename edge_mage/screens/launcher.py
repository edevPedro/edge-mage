"""Course launcher — primary journey first; module browser secondary."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from edge_mage.courses import COURSE_EMAGE, COURSES, primary_course
from edge_mage.screens.base import MageScreen

BANNER = r"""
╔══════════════════════════════════════════════════╗
║         e - m a g e   ·   JOURNEY                ║
║   One path · phases · optional Neurotech branch  ║
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
        primary = primary_course()

        with Vertical():
            yield Static(BANNER, id="banner")
            yield Static("JORNADA PRINCIPAL", classes="panel-title")
            yield Static(
                f"Rank global: [{g_title}]  ·  {mago}",
                classes="rank",
            )
            yield Static(
                "Uma progressão: Foundations → Systems → Arch → SIMD → HPC → "
                "GPU → Inference → Co-design. Módulos legados = browser.",
                classes="muted",
            )
            yield Static("j/k · Enter  ·  q sair", classes="muted")
            options: list[Option] = [
                Option(
                    f"▶  Continuar jornada  —  {primary.blurb}",
                    id=COURSE_EMAGE,
                ),
            ]
            options.append(Option("── Módulo browser (alias) ──", id="_sep", disabled=True))
            for c in COURSES:
                if c.primary:
                    continue
                lock = ""
                if c.requires_mago_base and not profile.get("mago_base"):
                    lock = "  [? preview]"
                prefix = "⌥  " if c.elective else "·  "
                options.append(
                    Option(f"{prefix}{c.title_pt}{lock}  —  {c.blurb}", id=c.id)
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
        if oid == "_sep":
            return
        if oid == "github":
            from edge_mage.auth import github_connect_instructions

            msg = github_connect_instructions()
            self.app.notify(msg.split("\n")[0], severity="information")
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

        known = {c.id for c in COURSES}
        if oid in known:
            preview = False
            info = next(c for c in COURSES if c.id == oid)
            if info.requires_mago_base and not mago:
                preview = True
                self.app.notify(
                    "Sem Mago base — entrando em preview. "
                    "Conclua Foundations (P0) na jornada para o caminho completo.",
                    severity="warning",
                )
            elif oid == COURSE_EMAGE and not mago:
                self.app.notify(
                    "Jornada única: comece em Foundations (P0). "
                    "Fases avançadas pedem Mago base (preview liberado).",
                    severity="information",
                )
            self._enter(oid, preview=preview)

    def open_default(self) -> None:
        lst = self._option_list()
        if lst is not None:
            lst.action_select()
