"""Animações educativas de matemática (frames em texto)."""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import Literal

from edge_mage.animations.canvas import BrailleCanvas, ascii_plot_grid, flatten_grid

AnimKind = Literal["unit_circle", "sine_wave", "vector", "matrix", "none"]


def frame_unit_circle(t: float, *, cols: int = 36, rows: int = 12) -> str:
    """Círculo unitário com raio varrendo o ângulo θ = t."""
    canvas = BrailleCanvas(cols, rows)
    cx, cy = canvas.px_w / 2, canvas.px_h / 2
    r = min(cx, cy) - 2
    canvas.circle(cx, cy, r, steps=80)
    # eixos
    canvas.line(2, cy, canvas.px_w - 3, cy)
    canvas.line(cx, 1, cx, canvas.px_h - 2)
    theta = (t % 1.0) * 2 * math.pi
    px = cx + r * math.cos(theta)
    py = cy - r * math.sin(theta)
    canvas.line(cx, cy, px, py)
    # projeção cos (eixo x) e sin (eixo y)
    canvas.line(cx, cy, px, cy)
    canvas.line(px, cy, px, py)
    canvas.set_pixel(int(px), int(py))
    deg = theta * 180 / math.pi
    header = (
        f"θ={deg:6.1f}°  cos={math.cos(theta):+0.3f}  sin={math.sin(theta):+0.3f}"
    )
    return f"{header}\n{canvas.render()}"


def frame_sine_wave(t: float, *, cols: int = 48, rows: int = 10) -> str:
    """Desenha seno (e cos pontilhado) com fase avançando."""
    canvas = BrailleCanvas(cols, rows)
    mid = canvas.px_h // 2
    canvas.line(0, mid, canvas.px_w - 1, mid)
    phase = (t % 1.0) * 2 * math.pi
    amp = (canvas.px_h / 2) - 2
    # desenha até a fase atual
    progress = 0.15 + 0.85 * ((t * 0.7) % 1.0)
    last_sx = last_sy = last_cx = last_cy = None
    steps = canvas.px_w
    for i in range(int(steps * progress)):
        x = i
        ang = (i / max(1, steps - 1)) * 4 * math.pi + phase
        sy = mid - amp * math.sin(ang)
        cy = mid - amp * math.cos(ang)
        if last_sx is not None:
            canvas.line(last_sx, last_sy, x, sy)
            # cos mais espaçado
            if i % 2 == 0 and last_cx is not None:
                canvas.line(last_cx, last_cy, x, cy)
        last_sx, last_sy = x, sy
        last_cx, last_cy = x, cy
    header = f"sin(x) sólido · cos(x) pontilhado · fase={phase * 180 / math.pi:5.1f}°"
    return f"{header}\n{canvas.render()}"


def frame_vector(t: float, *, cols: int = 36, rows: int = 12) -> str:
    """Seta de vetor rotacionando + componentes."""
    canvas = BrailleCanvas(cols, rows)
    ox, oy = 4, canvas.px_h - 3
    # eixos
    canvas.line(ox, 1, ox, canvas.px_h - 2)
    canvas.line(2, oy, canvas.px_w - 2, oy)
    ang = (t % 1.0) * 2 * math.pi
    length = min(canvas.px_w, canvas.px_h) * 0.55
    vx = length * math.cos(ang)
    vy = -length * math.sin(ang)
    ex, ey = ox + vx, oy + vy
    canvas.line(ox, oy, ex, ey)
    # ponta da seta
    tip_ang = math.atan2(vy, vx)
    for da in (2.5, -2.5):
        ax = ex - 5 * math.cos(tip_ang + da * 0.35)
        ay = ey - 5 * math.sin(tip_ang + da * 0.35)
        canvas.line(ex, ey, ax, ay)
    # componentes
    canvas.line(ox, oy, ex, oy)
    canvas.line(ex, oy, ex, ey)
    mag = math.hypot(vx, vy)
    # normaliza para “unidade didática”
    ux, uy = math.cos(ang), math.sin(ang)
    header = f"v=({ux:+0.2f}, {uy:+0.2f})  ‖v‖={mag / max(length, 1):0.2f}·L  θ={ang * 180 / math.pi:5.1f}°"
    return f"{header}\n{canvas.render()}"


def frame_matrix(t: float, *, cols: int = 40, rows: int = 11) -> str:
    """Hint visual: transform 2×2 (escala/rotação) num grid de pontos."""
    grid = ascii_plot_grid(cols, rows, fill="·")
    cx, cy = cols // 2, rows // 2
    # eixos
    for x in range(cols):
        grid[cy][x] = "─"
    for y in range(rows):
        grid[y][cx] = "│"
    grid[cy][cx] = "┼"
    ang = (t % 1.0) * 2 * math.pi
    sx = 1.0 + 0.35 * math.sin(ang * 2)
    sy = 1.0 + 0.35 * math.cos(ang * 2)
    c, s = math.cos(ang), math.sin(ang)
    # Aplica R(θ) · diag(sx,sy) a um conjunto de pontos
    pts = [(-2, -1), (-1, 2), (2, 1), (1, -2), (0, 2), (2, 0)]
    for px, py in pts:
        # escala
        qx, qy = px * sx, py * sy
        # rotação
        rx = c * qx - s * qy
        ry = s * qx + c * qy
        gx = int(round(cx + rx * 3))
        gy = int(round(cy - ry * 1.6))
        if 0 <= gx < cols and 0 <= gy < rows:
            grid[gy][gx] = "●"
    header = f"A = R({ang * 180 / math.pi:5.1f}°) · diag({sx:0.2f},{sy:0.2f})  y=Ax"
    return f"{header}\n{flatten_grid(grid)}"


_FRAME_FN: dict[str, Callable[..., str]] = {
    "unit_circle": frame_unit_circle,
    "sine_wave": frame_sine_wave,
    "vector": frame_vector,
    "matrix": frame_matrix,
}


def animation_for_room(room_id: str, animation: str | None = None) -> AnimKind:
    """Escolhe animação por campo YAML ou heurística do id da sala."""
    if animation and animation in _FRAME_FN:
        return animation  # type: ignore[return-value]
    rid = room_id.lower()
    if "trigon" in rid or "trig" in rid or "onda" in rid or "sin" in rid:
        return "unit_circle"
    if "vetor" in rid or "vector" in rid:
        return "vector"
    if "algebra" in rid or "matriz" in rid or "matrix" in rid or "matmul" in rid:
        return "matrix"
    if "transform" in rid:
        return "matrix"
    return "none"


def render_frame(kind: AnimKind | str, t: float) -> str:
    fn = _FRAME_FN.get(kind)
    if fn is None:
        return "(sem animação para esta sala — espaço / :anim em salas de math)"
    return fn(t)


def available_animations() -> list[str]:
    return sorted(_FRAME_FN.keys())
