"""Widgets em blocos inspirados no Wave Terminal (§10/§11). Zero dependências.

Três widgets: WaveBlock (bloco com título), MetricStrip (streak/evidência/
dispersão) e SparklineBlock (curva da métrica no tempo). As funções puras
(`sparkline`, `bar_row`, `metric_text`) são testáveis sem TUI.
"""

from __future__ import annotations

from rich.text import Text
from textual.widgets import Static

_SPARK = "▁▂▃▄▅▆▇█"
_ACCENT = "#7aa2f7"
_OK = "#9ece6a"
_WARN = "#e0af68"
_DIM = "#6b7684"


def sparkline(values: list[float], *, width: int = 48) -> str:
    """Sparkline Unicode de uma série (últimos `width` pontos)."""
    vals = [float(v) for v in values][-width:]
    if not vals:
        return ""
    lo, hi = min(vals), max(vals)
    span = (hi - lo) or 1.0
    out = []
    for v in vals:
        idx = int((v - lo) / span * (len(_SPARK) - 1) + 0.5)
        out.append(_SPARK[max(0, min(len(_SPARK) - 1, idx))])
    return "".join(out)


def bar_row(fraction: float, *, width: int = 20, fill: str = "█", empty: str = "░") -> str:
    frac = max(0.0, min(1.0, fraction))
    n = int(round(frac * width))
    return fill * n + empty * (width - n)


def metric_text(metrics: list[tuple[str, str]]) -> Text:
    t = Text()
    for i, (k, v) in enumerate(metrics):
        if i:
            t.append("  ·  ", style=_DIM)
        t.append(f"{k} ", style=_DIM)
        t.append(str(v), style=f"bold {_OK}")
    return t


class WaveBlock(Static):
    """Bloco com título colorido e linhas de corpo."""

    DEFAULT_CSS = """
    WaveBlock {
        border: round #2a3642;
        padding: 0 1;
        height: auto;
        margin: 0 0 1 0;
    }
    """

    def __init__(self, title: str = "", lines: list[str] | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._title = title
        self._lines = list(lines or [])
        self._text = Text()
        self._apply()

    def _apply(self) -> None:
        t = Text()
        if self._title:
            t.append(self._title + "\n", style=f"bold {_ACCENT}")
        for i, ln in enumerate(self._lines):
            t.append(str(ln))
            if i < len(self._lines) - 1:
                t.append("\n")
        self._text = t
        self.update(t)

    @property
    def plain_text(self) -> str:
        return self._text.plain

    def set_block(self, title: str, lines: list[str]) -> None:
        self._title = title
        self._lines = list(lines)
        self._apply()


class MetricStrip(Static):
    """Linha de métricas: streak, evidências, dispersão."""

    DEFAULT_CSS = "MetricStrip { height: auto; padding: 0 1; }"

    @property
    def plain_text(self) -> str:
        return getattr(self, "_text", Text()).plain

    def set_metrics(self, metrics: list[tuple[str, str]]) -> None:
        self._text = metric_text(metrics)
        self.update(self._text)


class SparklineBlock(Static):
    """Curva de uma métrica no tempo (sparkline Unicode)."""

    DEFAULT_CSS = "SparklineBlock { height: auto; padding: 0 1; }"

    @property
    def plain_text(self) -> str:
        return getattr(self, "_text", Text()).plain

    def set_series(self, label: str, values: list[float], *, width: int = 48) -> None:
        t = Text()
        t.append(f"{label}: ", style=_DIM)
        if not values:
            t.append("(sem dados — rode `mage verify` mais vezes)", style=_DIM)
        else:
            t.append(sparkline(values, width=width), style=f"bold {_WARN}")
            t.append(f"  min={min(values):.4g} max={max(values):.4g} n={len(values)}", style=_DIM)
        self._text = t
        self.update(t)
