"""Tela de cerimônia — victory juice (XP / skill / level / rank)."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from edge_mage.juice import (
    combo_line,
    level_up_banner,
    rank_up_banner,
    skill_drop_banner,
    xp_banner,
    xp_bar,
)
from edge_mage.screens.base import MageScreen


class CeremonyScreen(MageScreen):
    """Mostra banners de vitória e espera Enter/l para continuar."""

    context_label = "cerimônia"
    list_id = "ceremony-actions"

    def __init__(
        self,
        *,
        title: str = "VITÓRIA",
        gained: int = 0,
        total_xp: int = 0,
        into: int = 0,
        need: int | None = None,
        level: int = 1,
        leveled: bool = False,
        rank_title: str = "",
        ranked_up: bool = False,
        skill_glyph: str = "",
        skill_name: str = "",
        combo: int = 0,
        mult: float = 1.0,
        extra_lines: list[str] | None = None,
    ) -> None:
        super().__init__()
        self.title_text = title
        self.gained = gained
        self.total_xp = total_xp
        self.into = into
        self.need = need
        self.level = level
        self.leveled = leveled
        self.rank_title = rank_title
        self.ranked_up = ranked_up
        self.skill_glyph = skill_glyph
        self.skill_name = skill_name
        self.combo = combo
        self.mult = mult
        self.extra_lines = extra_lines or []

    def compose_body(self) -> ComposeResult:
        blocks: list[str] = [self.title_text, ""]
        if self.gained:
            blocks.append(xp_banner(self.gained))
            blocks.append("")
            blocks.append(xp_bar(self.into, self.need))
            if self.mult > 1.0:
                blocks.append(f"Mana de streak ×{self.mult:.2f}")
        if self.combo:
            cl = combo_line(self.combo)
            if cl:
                blocks.append(cl)
        if self.skill_name:
            blocks.append("")
            blocks.append(skill_drop_banner(self.skill_glyph or "✦", self.skill_name))
        if self.leveled:
            blocks.append("")
            blocks.append(level_up_banner(self.level))
        if self.ranked_up:
            blocks.append("")
            blocks.append(rank_up_banner(self.rank_title))
        for line in self.extra_lines:
            blocks.append(line)
        blocks.append("")
        blocks.append(f"Total {self.total_xp} XP · Nv {self.level} · {self.rank_title}")

        with Vertical():
            with VerticalScroll(classes="panel", can_focus=False):
                yield Static("\n".join(blocks), classes="ok")
            yield OptionList(
                Option("▶  Continuar", id="ok"),
                id="ceremony-actions",
            )

    def on_mount(self) -> None:
        super().on_mount()
        if hasattr(self.app, "set_nav_context"):
            self.app.set_nav_context("cerimônia")  # type: ignore[attr-defined]
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if str(event.option.id) == "ok":
            self.app.pop_screen()

    def open_default(self) -> None:
        self.app.pop_screen()
