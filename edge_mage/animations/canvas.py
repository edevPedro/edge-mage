"""Canvas ASCII/braille leve para animações no terminal."""

from __future__ import annotations

import math
from dataclasses import dataclass


# Braille dots (2×4) → Unicode U+2800
_BRAILLE_MAP = (
    (0x01, 0x08),
    (0x02, 0x10),
    (0x04, 0x20),
    (0x40, 0x80),
)


@dataclass
class BrailleCanvas:
    """Buffer de pixels lógicos → células braille (2×4 por caractere)."""

    cols: int
    rows: int

    def __post_init__(self) -> None:
        self.px_w = self.cols * 2
        self.px_h = self.rows * 4
        self._buf = [0] * (self.cols * self.rows)

    def clear(self) -> None:
        for i in range(len(self._buf)):
            self._buf[i] = 0

    def set_pixel(self, x: int, y: int, on: bool = True) -> None:
        if x < 0 or y < 0 or x >= self.px_w or y >= self.px_h:
            return
        cx, dx = divmod(x, 2)
        cy, dy = divmod(y, 4)
        idx = cy * self.cols + cx
        bit = _BRAILLE_MAP[dy][dx]
        if on:
            self._buf[idx] |= bit
        else:
            self._buf[idx] &= ~bit

    def line(self, x0: float, y0: float, x1: float, y1: float) -> None:
        """Bresenham em coordenadas de pixel."""
        x0i, y0i = int(round(x0)), int(round(y0))
        x1i, y1i = int(round(x1)), int(round(y1))
        dx = abs(x1i - x0i)
        dy = -abs(y1i - y0i)
        sx = 1 if x0i < x1i else -1
        sy = 1 if y0i < y1i else -1
        err = dx + dy
        x, y = x0i, y0i
        while True:
            self.set_pixel(x, y)
            if x == x1i and y == y1i:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def circle(self, cx: float, cy: float, r: float, steps: int = 64) -> None:
        for i in range(steps):
            a0 = 2 * math.pi * i / steps
            a1 = 2 * math.pi * (i + 1) / steps
            self.line(
                cx + r * math.cos(a0),
                cy - r * math.sin(a0),
                cx + r * math.cos(a1),
                cy - r * math.sin(a1),
            )

    def render(self) -> str:
        lines: list[str] = []
        for row in range(self.rows):
            chars: list[str] = []
            base = row * self.cols
            for col in range(self.cols):
                chars.append(chr(0x2800 + self._buf[base + col]))
            lines.append("".join(chars))
        return "\n".join(lines)


def ascii_plot_grid(
    width: int,
    height: int,
    *,
    fill: str = " ",
) -> list[list[str]]:
    return [[fill for _ in range(width)] for _ in range(height)]


def flatten_grid(grid: list[list[str]]) -> str:
    return "\n".join("".join(row) for row in grid)
