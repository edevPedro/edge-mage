"""Painel de animação educativa (timer + braille/ASCII)."""

from __future__ import annotations

from textual.reactive import reactive
from textual.timer import Timer
from textual.widgets import Static

from edge_mage.animations.math import AnimKind, render_frame


class AnimationPanel(Static):
    """Área visual que anima com set_interval (~10–12 fps)."""

    DEFAULT_CSS = """
    AnimationPanel {
        height: 14;
        border: solid #2a3038;
        background: #0c1014;
        color: #9db8a5;
        padding: 0 1;
        margin: 0 1 1 1;
    }
    AnimationPanel.-hidden {
        display: none;
    }
    """

    playing: reactive[bool] = reactive(False)
    kind: reactive[str] = reactive("unit_circle")
    _t: float = 0.0
    _timer: Timer | None = None

    def __init__(self, kind: AnimKind | str = "unit_circle", **kwargs) -> None:
        super().__init__(render_frame(kind, 0.0), **kwargs)
        self.kind = kind if kind != "none" else "unit_circle"
        self.can_focus = False

    def on_mount(self) -> None:
        self._timer = self.set_interval(1 / 12, self._tick, pause=True)

    def _tick(self) -> None:
        if not self.playing:
            return
        self._t = (self._t + 1 / 12 / 6.0) % 1.0  # ~6s por ciclo
        self.update(render_frame(self.kind, self._t))

    def play(self, kind: AnimKind | str | None = None) -> None:
        if kind and kind != "none":
            self.kind = kind
        self.remove_class("-hidden")
        self.playing = True
        self._t = 0.0
        self.update(render_frame(self.kind, self._t))
        if self._timer is not None:
            self._timer.resume()

    def pause(self) -> None:
        self.playing = False
        if self._timer is not None:
            self._timer.pause()

    def toggle(self, kind: AnimKind | str | None = None) -> None:
        if self.playing:
            self.pause()
        else:
            self.play(kind)

    def stop_and_hide(self) -> None:
        self.pause()
        self.add_class("-hidden")
