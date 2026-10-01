"""Perfil, ranks e tabela de níveis."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from edge_mage.ranks import LEVEL_THRESHOLDS, RANKS, xp_for_next_level
from edge_mage.screens.base import MageScreen


class ProfileScreen(MageScreen):
    context_label = "profile"
    list_id = "profile-actions"

    def compose_body(self) -> ComposeResult:
        store = self.app.store  # type: ignore[attr-defined]
        p = store.profile_summary()
        rank = p["rank"]
        into, need = xp_for_next_level(p["xp"])

        rank_lines = []
        for r in RANKS:
            mark = "►" if r.id == rank.id else " "
            lock = "" if p["xp"] >= r.min_xp else " 🔒"
            rank_lines.append(
                f"{mark} {r.title:12s}  ≥{r.min_xp:4d} XP  · Nv{r.min_level}{lock}\n"
                f"    {r.blurb}"
            )

        level_rows = []
        for i, thr in enumerate(LEVEL_THRESHOLDS):
            lvl = i + 1
            star = "★" if lvl == p["level"] else " "
            level_rows.append(f"{star} Nv{lvl:2d}  {thr:5d} XP")

        with VerticalScroll(can_focus=False):
            yield Static("PERFIL DO MAGO", classes="title")
            with Vertical(classes="panel"):
                yield Static(
                    f"{rank.title}  ·  Nível {p['level']}  ·  {p['xp']} XP",
                    classes="rank",
                )
                if need:
                    yield Static(f"Próximo nível: {into}/{need} XP neste patamar")
                else:
                    yield Static("Nível máximo da tabela base.")
                nxt = p["next_rank"]
                if nxt:
                    yield Static(
                        f"Próximo rank: {nxt.title} (faltam {max(0, nxt.min_xp - p['xp'])} XP)",
                        classes="accent",
                    )
                yield Static(
                    f"Streak: {p['streak']} dias  ·  "
                    f"Tasks: {p['tasks_done']}  ·  Salas: {p['rooms_done']}",
                    classes="muted",
                )
                yield Static(f"Progresso em: {store.path}", classes="muted")

            yield Static("RANKS", classes="panel-title")
            yield Static("\n".join(rank_lines), classes="panel")

            yield Static("TABELA DE NÍVEIS (XP acumulado)", classes="panel-title")
            yield Static("\n".join(level_rows), classes="panel")

            yield OptionList(Option("←  Voltar", id="back"), id="profile-actions")

    def on_mount(self) -> None:
        super().on_mount()
        if hasattr(self.app, "set_nav_context"):
            self.app.set_nav_context("profile")  # type: ignore[attr-defined]
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if str(event.option.id) == "back":
            self.app.pop_screen()
