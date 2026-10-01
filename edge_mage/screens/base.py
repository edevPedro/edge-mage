"""Tela base com statusline, painéis (Ctrl+w) e navegação estilo nvim."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Input, OptionList, TextArea

from edge_mage.nav import PANE_LABELS, NavMode
from edge_mage.widgets.statusline import StatusLine


class MageScreen(Screen[None]):
    """Base: statusline + vim nav (teclas tratadas no App em NORMAL)."""

    BINDINGS = [
        Binding("escape", "vim_escape", "Esc", show=False, priority=True),
    ]

    context_label: str = ""
    #: id do OptionList principal desta tela (se houver)
    list_id: str | None = None
    #: painéis cicláveis via Ctrl+w (override nas telas)
    pane_ids: list[str] = []
    focused_pane: str | None = None

    def compose_body(self) -> ComposeResult:
        yield from ()

    def compose(self) -> ComposeResult:
        yield from self.compose_body()
        yield StatusLine()

    def on_screen_resume(self) -> None:
        self.refresh_statusline()
        self.call_after_refresh(self.focus_nav_target)

    def on_mount(self) -> None:
        if self.pane_ids and self.focused_pane is None:
            self.focused_pane = self.pane_ids[0]
        self.refresh_statusline()
        self.call_after_refresh(self.focus_nav_target)

    def pane_context_suffix(self) -> str:
        if not self.focused_pane:
            return ""
        label = PANE_LABELS.get(self.focused_pane, self.focused_pane.upper())
        return f" · {label}"

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
        ctx = (self.context_label or getattr(app, "nav_context", "")) + self.pane_context_suffix()
        xp = 0
        rank = ""
        skills = ""
        if store is not None:
            p = store.profile_summary()
            xp = p["xp"]
            rank = p["rank"].title
            skills_n = p.get("skills_done", 0)
            skills_total = getattr(app, "skills_total", 0)
            if skills_total:
                skills = f"✧{skills_n}/{skills_total}"
            elif skills_n:
                skills = f"✧{skills_n}"
        sl.set_status(mode=str(mode), context=ctx, xp=xp, rank=rank, skills=skills)

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

    def _scroll_for_pane(self, pane: str | None) -> VerticalScroll | None:
        if not pane:
            return None
        mapping = {
            "story": "#pane-story",
            "concept": "#pane-concept",
            "desafio": "#pane-desafio",
            "prompt": "#pane-prompt",
        }
        wid = mapping.get(pane)
        if not wid:
            return None
        try:
            return self.query_one(wid, VerticalScroll)
        except Exception:
            return None

    def focus_nav_target(self) -> None:
        """Foca o painel ativo (OptionList / scroll / input); não rouba INSERT."""
        app = self.app
        mode = getattr(app, "nav_mode", NavMode.NORMAL)
        if mode == NavMode.INSERT or mode == NavMode.COMMAND:
            return
        pane = self.focused_pane
        if pane == "tasks" or pane == "actions" or (pane is None and self.list_id):
            lst = self._option_list()
            if lst is not None:
                lst.focus()
                if lst.option_count and lst.highlighted is None:
                    lst.highlighted = 0
                return
        if pane == "answer":
            # Em NORMAL não foca o input — só destaca o pane no statusline
            try:
                self.set_focus(None)
            except Exception:
                pass
            return
        if pane == "anim":
            try:
                self.set_focus(None)
            except Exception:
                pass
            return
        scroll = self._scroll_for_pane(pane)
        if scroll is not None:
            scroll.can_focus = True
            scroll.focus()
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

    def cycle_pane(self, delta: int = 1) -> None:
        if not self.pane_ids:
            return
        cur = self.focused_pane or self.pane_ids[0]
        try:
            idx = self.pane_ids.index(cur)
        except ValueError:
            idx = 0
        idx = (idx + delta) % len(self.pane_ids)
        self.set_focused_pane(self.pane_ids[idx])

    def set_focused_pane(self, pane: str) -> None:
        if pane not in self.pane_ids and self.pane_ids:
            return
        self.focused_pane = pane
        # highlight CSS
        for pid in self.pane_ids:
            try:
                w = self.query_one(f"#pane-{pid}")
                w.set_class(pid == pane, "-pane-focus")
            except Exception:
                pass
        # also task-list / anim-panel ids
        try:
            if pane == "tasks":
                self.query_one("#task-list").set_class(True, "-pane-focus")
            else:
                self.query_one("#task-list").set_class(False, "-pane-focus")
        except Exception:
            pass
        try:
            if pane == "actions":
                self.query_one("#task-actions").set_class(True, "-pane-focus")
            else:
                self.query_one("#task-actions").set_class(False, "-pane-focus")
        except Exception:
            pass
        try:
            anim = self.query_one("#anim-panel")
            anim.set_class(pane == "anim", "-pane-focus")
        except Exception:
            pass
        on_change = getattr(self, "on_pane_changed", None)
        if callable(on_change):
            on_change(pane)
        self.focus_nav_target()
        self.refresh_statusline()

    def move_pane(self, direction: str) -> None:
        """h/l ciclam; j/k também ciclam (layout linear)."""
        if direction in {"l", "j", "w"}:
            self.cycle_pane(1)
        elif direction in {"h", "k"}:
            self.cycle_pane(-1)

    def action_vim_escape(self) -> None:
        app = self.app
        if getattr(app, "nav_mode", None) == NavMode.WINDOW:
            if hasattr(app, "enter_normal"):
                app.enter_normal()  # type: ignore[attr-defined]
            self.refresh_statusline()
            return
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
        pane = self.focused_pane
        if pane in {"story", "concept", "desafio", "prompt"}:
            scroll = self._scroll_for_pane(pane)
            if scroll is not None:
                scroll.scroll_down(animate=False)
                return
        if pane == "anim":
            return
        if pane == "answer":
            return
        lst = self._option_list()
        if lst is not None:
            if not lst.has_focus:
                lst.focus()
            lst.action_cursor_down()

    def action_vim_up(self) -> None:
        if self.is_typing():
            return
        pane = self.focused_pane
        if pane in {"story", "concept", "desafio", "prompt"}:
            scroll = self._scroll_for_pane(pane)
            if scroll is not None:
                scroll.scroll_up(animate=False)
                return
        if pane == "anim":
            return
        if pane == "answer":
            return
        lst = self._option_list()
        if lst is not None:
            if not lst.has_focus:
                lst.focus()
            lst.action_cursor_up()

    def action_vim_open(self) -> None:
        if self.is_typing():
            return
        pane = self.focused_pane
        if pane == "answer":
            enter = getattr(self, "enter_insert", None)
            if callable(enter):
                enter()
            return
        if pane in {"story", "concept", "desafio", "anim", "prompt"}:
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
        pane = self.focused_pane
        if pane in {"story", "concept", "desafio", "prompt"}:
            scroll = self._scroll_for_pane(pane)
            if scroll is not None:
                scroll.scroll_home(animate=False)
                return
        lst = self._option_list()
        if lst is not None and lst.option_count:
            if not lst.has_focus:
                lst.focus()
            lst.highlighted = 0

    def action_vim_bottom(self) -> None:
        if self.is_typing():
            return
        pane = self.focused_pane
        if pane in {"story", "concept", "desafio", "prompt"}:
            scroll = self._scroll_for_pane(pane)
            if scroll is not None:
                scroll.scroll_end(animate=False)
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
