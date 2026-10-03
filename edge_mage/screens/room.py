"""Vista de sala: História | Conceito | Desafio + animação + tarefas (Ctrl+w)."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Markdown, OptionList, Static
from textual.widgets.option_list import Option

from edge_mage.animations.math import animation_for_room
from edge_mage.models import Room, Track
from edge_mage.screens.base import MageScreen
from edge_mage.widgets.animation_panel import AnimationPanel


class RoomScreen(MageScreen):
    list_id = "task-list"

    def __init__(self, track: Track, room: Room) -> None:
        super().__init__()
        self.track = track
        self.room = room
        self.context_label = f"{track.id}/{room.id}"
        self.anim_kind = animation_for_room(room.id, room.animation)
        panes = ["story", "concept", "desafio"]
        if self.anim_kind != "none":
            panes.append("anim")
        panes.append("tasks")
        self.pane_ids = panes
        self.focused_pane = "story"
        self._content_tab = "story"  # qual markdown está no painel esquerdo
        self._task_list_height = 7
        self._anim_width = 42


    def _md(self, kind: str) -> str:
        if kind == "story":
            return self.room.story_md.strip() or (
                f"_Sem história ainda._\n\n{self.room.summary}"
            )
        if kind == "concept":
            return self.room.concept_md.strip() or (
                "_Sem conceito ainda._\n\nUse a lição em Desafio."
            )
        return self.room.lesson_md.strip() or "_Sem lição._"

    def compose_body(self) -> ComposeResult:
        store = self.app.store  # type: ignore[attr-defined]
        done, total = store.room_progress(self.track.id, self.room)
        has_anim = self.anim_kind != "none"
        with Vertical():
            yield Static(self.room.title, classes="title")
            hint = "  ·  Ctrl+w painéis  ·  Space/:anim" if has_anim else "  ·  Ctrl+w painéis"
            yield Static(
                f"{self.room.summary}  ·  {done}/{total}{hint}",
                classes="muted",
            )
            yield Static(
                "[História]  Conceito  Desafio",
                id="tab-bar",
                classes="tab-bar",
            )
            with Horizontal(id="room-main"):
                with VerticalScroll(classes="panel -pane-focus", id="pane-story"):
                    yield Static("HISTÓRIA", classes="panel-title")
                    yield Markdown(self._md("story"), id="md-story")
                with VerticalScroll(classes="panel", id="pane-concept"):
                    yield Static("CONCEITO", classes="panel-title")
                    yield Markdown(self._md("concept"), id="md-concept")
                with VerticalScroll(classes="panel", id="pane-desafio"):
                    yield Static("DESAFIO / LIÇÃO", classes="panel-title")
                    yield Markdown(self._md("desafio"), id="md-desafio")
                if has_anim:
                    panel = AnimationPanel(self.anim_kind, id="anim-panel")
                    panel.add_class("-hidden")
                    yield panel
            yield Static(
                "TAREFAS — j/k · Enter/l  ·  Ctrl+w  ·  M mastery (sala limpa)",
                classes="panel-title",
            )
            yield OptionList(*self._task_options(), id="task-list", markup=False)

    def _task_options(self) -> list[Option]:
        store = self.app.store  # type: ignore[attr-defined]
        options: list[Option] = []
        missing = store.missing_skills_for_room(self.room)
        if missing:
            options.append(
                Option(f"🔒 Requer skills: {', '.join(missing)}", id="_locked")
            )
        for t in self.room.tasks:
            done = store.is_task_done(self.track.id, self.room.id, t.id)
            mark = "✓" if done else "○"
            kind = {
                "mcq": "MCQ",
                "numeric": "NUM",
                "fill": "FILL",
                "code": "CODE",
                "ritual": "RITUAL",
            }.get(t.type, t.type.upper())
            # Prompt inteiro: a lista quebra linha e rola. O corte em 70
            # partia o enunciado no meio da frase.
            one_line = " ".join(t.prompt.split())
            label = f"{mark}  [{kind}]  {one_line}  (+{t.xp} XP)"
            options.append(Option(label, id=t.id))
        if store.is_room_done(self.track.id, self.room.id):
            m = store.mastery_count(self.track.id, self.room.id)
            shine = "✦" if m >= 3 else "·"
            options.append(
                Option(
                    f"{shine}  Mastery {m}/3 — variantes (+XP menor)",
                    id="_mastery",
                )
            )
        return options

    def on_mount(self) -> None:
        super().on_mount()
        if hasattr(self.app, "set_nav_context"):
            self.app.set_nav_context(self.context_label)  # type: ignore[attr-defined]
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]
        try:
            self.query_one("#task-list").styles.height = self._task_list_height
        except Exception:
            pass
        self._apply_content_visibility()
        self.set_focused_pane("story")
        self.call_after_refresh(self._fit_anim_column)
        if self.anim_kind != "none":
            self.call_after_refresh(self._autoplay)

    def resize_pane(self, direction: str, delta: int = 2) -> None:
        """
        Redimensiona painéis estilo Neovim (Ctrl+w Shift+H/J/K/L ou +, -, <, >):
          K / + : Aumenta o conteúdo da sala (encolhe a lista de tarefas)
          J / - : Aumenta a lista de tarefas (encolhe o conteúdo da sala)
          H / < : Alarga o painel de texto / encolhe o painel de animação
          L / > : Alarga o painel de animação
        """
        try:
            task_list = self.query_one("#task-list")
        except Exception:
            return

        if direction in {"K", "+"}:
            self._task_list_height = max(3, self._task_list_height - delta)
            task_list.styles.height = self._task_list_height
            self.notify(
                f"Conteúdo ampliado  ·  Tarefas: {self._task_list_height} lin",
                severity="information",
            )
        elif direction in {"J", "-"}:
            self._task_list_height = min(22, self._task_list_height + delta)
            task_list.styles.height = self._task_list_height
            self.notify(
                f"Tarefas ampliadas: {self._task_list_height} lin",
                severity="information",
            )
        elif direction in {"H", "<"}:
            if self.anim_kind != "none":
                try:
                    anim = self.query_one("#anim-panel")
                    self._anim_width = max(24, self._anim_width - delta * 2)
                    anim.styles.width = self._anim_width
                    self.notify(
                        f"Texto mais largo  ·  Animação: {self._anim_width} cols",
                        severity="information",
                    )
                except Exception:
                    pass
        elif direction in {"L", ">"}:
            if self.anim_kind != "none":
                try:
                    anim = self.query_one("#anim-panel")
                    self._anim_width = min(68, self._anim_width + delta * 2)
                    anim.styles.width = self._anim_width
                    self.notify(
                        f"Animação: {self._anim_width} cols",
                        severity="information",
                    )
                except Exception:
                    pass
        self._fit_anim_column()

    def on_resize(self, event) -> None:  # type: ignore[no-untyped-def]
        self._fit_anim_column()

    def _fit_anim_column(self) -> None:
        """Não deixa a animação de 42 colunas esmagar história/conceito/desafio.

        Em terminal estreito o painel some enquanto se lê; no foco ANIM ele
        ocupa a faixa. Em terminal largo segue ao lado, na largura ajustável.
        """
        if self.anim_kind == "none":
            return
        try:
            anim = self.query_one("#anim-panel")
        except Exception:
            return
        width = self.size.width
        if width < 20:
            return
        side_ok = width >= 96
        if self.focused_pane == "anim" and not side_ok:
            anim.remove_class("-hidden")
            anim.styles.width = max(24, width - 4)
            for key in ("story", "concept", "desafio"):
                try:
                    self.query_one(f"#pane-{key}").add_class("-hidden-pane")
                except Exception:
                    pass
            return
        # leitura, ou ANIM ao lado quando cabe: restaura a aba de texto
        self._apply_content_visibility()
        if side_ok:
            anim.remove_class("-hidden")
            anim.styles.width = self._anim_width
        else:
            anim.add_class("-hidden")

    def _tab_label(self) -> str:
        marks = []
        for key, name in (
            ("story", "História"),
            ("concept", "Conceito"),
            ("desafio", "Desafio"),
        ):
            if self.focused_pane == key or (
                self.focused_pane not in {"story", "concept", "desafio"}
                and self._content_tab == key
            ):
                marks.append(f"[{name}]")
            else:
                marks.append(f" {name} ")
        return "  ".join(marks)

    def _apply_content_visibility(self) -> None:
        active = self.focused_pane if self.focused_pane in {
            "story",
            "concept",
            "desafio",
        } else self._content_tab
        self._content_tab = active
        for key in ("story", "concept", "desafio"):
            try:
                w = self.query_one(f"#pane-{key}")
                if key == active:
                    w.remove_class("-hidden-pane")
                else:
                    w.add_class("-hidden-pane")
            except Exception:
                pass
        try:
            self.query_one("#tab-bar", Static).update(self._tab_label())
        except Exception:
            pass

    def on_pane_changed(self, pane: str) -> None:
        if pane in {"story", "concept", "desafio"}:
            self._content_tab = pane
        self._apply_content_visibility()
        self._fit_anim_column()

    def _autoplay(self) -> None:
        try:
            panel = self.query_one("#anim-panel", AnimationPanel)
        except Exception:
            return
        panel.play(self.anim_kind)
        # play() mostra o painel; em tela estreita a leitura volta a largura cheia
        self._fit_anim_column()

    def toggle_animation(self, kind: str | None = None) -> None:
        if self.anim_kind == "none" and not kind:
            self.app.notify("esta sala não tem visual", severity="warning")
            return
        try:
            panel = self.query_one("#anim-panel", AnimationPanel)
        except Exception:
            self.app.notify("painel de animação indisponível", severity="warning")
            return
        use = kind or self.anim_kind
        if kind:
            self.anim_kind = kind  # type: ignore[assignment]
        panel.toggle(use)

    def action_start_mastery(self) -> None:
        import hashlib
        import random
        from datetime import date

        from edge_mage.daily import _variant_numeric
        from edge_mage.screens.task import TaskScreen

        store = self.app.store  # type: ignore[attr-defined]
        if not store.is_room_done(self.track.id, self.room.id):
            self.app.notify("complete a sala antes do mastery", severity="warning")
            return
        if store.mastery_count(self.track.id, self.room.id) >= 3:
            self.app.notify("mastery 3/3 — glyph no máximo", severity="information")
            return
        candidates = [t for t in self.room.tasks if t.type in {"numeric", "code", "mcq"}]
        if not candidates:
            self.app.notify("sem task para mastery", severity="warning")
            return
        seed = int(
            hashlib.sha256(
                f"{date.today().isoformat()}:{self.room.id}:{store.mastery_count(self.track.id, self.room.id)}".encode()
            ).hexdigest()[:8],
            16,
        )
        rng = random.Random(seed)
        base = rng.choice(candidates)
        quest = _variant_numeric(base, rng) if base.type == "numeric" else base
        self.app.push_screen(TaskScreen(self.track, self.room, quest, mastery=True))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        task_id = str(event.option.id)
        if task_id == "_mastery":
            self.action_start_mastery()
            return
        if task_id == "_locked":
            return
        missing = self.app.store.missing_skills_for_room(self.room)  # type: ignore[attr-defined]
        if missing:
            self.app.notify(
                f"skills necessárias: {', '.join(missing)}",
                severity="warning",
            )
            return
        task = next(t for t in self.room.tasks if t.id == task_id)
        from edge_mage.screens.task import TaskScreen

        self.app.push_screen(TaskScreen(self.track, self.room, task))

    def on_key(self, event) -> None:  # type: ignore[no-untyped-def]
        if event.character == "M":
            if getattr(self.app, "_in_insert", lambda: False)():
                return
            event.stop()
            self.action_start_mastery()

    def on_screen_resume(self) -> None:
        super().on_screen_resume()
        lst = self.query_one("#task-list", OptionList)
        lst.clear_options()
        lst.add_options(self._task_options())
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]
        self.focus_nav_target()
