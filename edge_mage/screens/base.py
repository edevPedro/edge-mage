"""Tela base com statusline e navegação estilo nvim."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Input, OptionList, TextArea

from edge_mage.nav import NavMode
from edge_mage.widgets.statusline import StatusLine


class MageScreen(Screen[None]):
    """Base: statusline + vim nav (teclas tratadas no App em NORMAL)."""

    # Só Esc com priority: sai de INSERT sem depender do Input engolir Esc.
    BINDINGS = [
        Binding("escape", "vim_escape", "Esc", show=False, priority=True),
    ]

    context_label: str = ""
    #: id do OptionList principal desta tela (se houver)
    list_id: str | None = None

    def compose_body(self) -> ComposeResult:
        yield from ()

    def compose(self) -> ComposeResult:
        yield from self.compose_body()
        yield StatusLine()

    def on_screen_resume(self) -> None:
        self.refresh_statusline()
        self.call_after_refresh(self.focus_nav_target)

    def on_mount(self) -> None:
        self.refresh_statusline()
        self.call_after_refresh(self.focus_nav_target)

    def refresh_statusline(self) -> None:
        app = self.app
        try:
            sl = self.query_one(StatusLine)
        except Exception:
            return
        store = getattr(app, "store", None)
        mode = getattr(app, "nav_mode", NavMode.NORMAL)
        if hasattr(mode, "value"):
            mode = mode.value
        ctx = self.context_label or getattr(app, "nav_context", "")
        xp = 0
        rank = ""
        if store is not None:
            p = store.profile_summary()
            xp = p["xp"]
            rank = p["rank"].title
        sl.set_status(mode=str(mode), context=ctx, xp=xp, rank=rank)

    def is_typing(self) -> bool:
        focused = self.focused
        return isinstance(focused, (Input, TextArea))

    def _option_list(self) -> OptionList | None:
        if self.list_id:
            try:
                return self.query_one(f"#{self.list_id}", OptionList)
            except Exception:
                pass
        try:
            return self.query_one(OptionList)
        except Exception:
            return None

    def focus_nav_target(self) -> None:
        """Foca o OptionList em NORMAL; não rouba foco se já estamos em INSERT."""
        app = self.app
        mode = getattr(app, "nav_mode", NavMode.NORMAL)
        if mode == NavMode.INSERT or mode == NavMode.COMMAND:
            return
        lst = self._option_list()
        if lst is not None:
            lst.focus()
            if lst.option_count and lst.highlighted is None:
                lst.highlighted = 0
            return
        try:
            self.set_focus(None)
        except Exception:
            pass

    def action_vim_escape(self) -> None:
        app = self.app
        if self.is_typing() or getattr(app, "nav_mode", None) == NavMode.INSERT:
            self.set_focus(None)
            if hasattr(app, "enter_normal"):
                app.enter_normal()  # type: ignore[attr-defined]
            self.focus_nav_target()
            self.refresh_statusline()
            return
        self.action_vim_back()

    def action_vim_back(self) -> None:
        if self.is_typing():
            return
        if len(self.app.screen_stack) > 1:
            self.app.pop_screen()

    def action_vim_down(self) -> None:
        if self.is_typing():
            return
        lst = self._option_list()
        if lst is not None:
            if not lst.has_focus:
                lst.focus()
            lst.action_cursor_down()

    def action_vim_up(self) -> None:
        if self.is_typing():
            return
        lst = self._option_list()
        if lst is not None:
            if not lst.has_focus:
                lst.focus()
            lst.action_cursor_up()

    def action_vim_open(self) -> None:
        if self.is_typing():
            return
        lst = self._option_list()
        if lst is not None:
            if not lst.has_focus:
                lst.focus()
            lst.action_select()
            return
        self.open_default()

    def open_default(self) -> None:
        """Ação Enter/l sem OptionList."""

    def action_vim_top(self) -> None:
        if self.is_typing():
            return
        lst = self._option_list()
        if lst is not None and lst.option_count:
            if not lst.has_focus:
                lst.focus()
            lst.highlighted = 0

    def action_vim_bottom(self) -> None:
        if self.is_typing():
            return
        lst = self._option_list()
        if lst is not None and lst.option_count:
            if not lst.has_focus:
                lst.focus()
            lst.highlighted = lst.option_count - 1

    def action_vim_anim(self) -> None:
        if self.is_typing():
            return
        toggle = getattr(self, "toggle_animation", None)
        if callable(toggle):
            toggle()

    def action_vim_insert(self) -> None:
        enter = getattr(self, "enter_insert", None)
        if callable(enter):
            enter()
