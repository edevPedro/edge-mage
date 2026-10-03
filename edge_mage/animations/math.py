"""Animações educativas de matemática / EE / ML (frames em texto)."""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import Literal

from edge_mage.animations.canvas import BrailleCanvas, ascii_plot_grid, flatten_grid

AnimKind = Literal[
    "unit_circle",
    "sine_wave",
    "vector",
    "matrix",
    "circuit_pulse",
    "adc_ladder",
    "gradient_descent",
    "softmax_bars",
    "robot_transform",
    "sampling_dots",
    "derivative_slope",
    "probability_bars",
    "quantize_steps",
    "memory_grid",
    "rhythm_bands",
    "filter_freq_response",
    "dipole_field",
    "spike_to_lfp",
    "mi_erds",
    "closed_loop_timeline",
    "volume_blur",
    "artifact_trace",
    "none",
]


def frame_unit_circle(t: float, *, cols: int = 36, rows: int = 12) -> str:
    """Círculo unitário com raio varrendo o ângulo θ = t."""
    canvas = BrailleCanvas(cols, rows)
    cx, cy = canvas.px_w / 2, canvas.px_h / 2
    r = min(cx, cy) - 2
    canvas.circle(cx, cy, r, steps=80)
    canvas.line(2, cy, canvas.px_w - 3, cy)
    canvas.line(cx, 1, cx, canvas.px_h - 2)
    theta = (t % 1.0) * 2 * math.pi
    px = cx + r * math.cos(theta)
    py = cy - r * math.sin(theta)
    canvas.line(cx, cy, px, py)
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
    canvas.line(ox, 1, ox, canvas.px_h - 2)
    canvas.line(2, oy, canvas.px_w - 2, oy)
    ang = (t % 1.0) * 2 * math.pi
    length = min(canvas.px_w, canvas.px_h) * 0.55
    vx = length * math.cos(ang)
    vy = -length * math.sin(ang)
    ex, ey = ox + vx, oy + vy
    canvas.line(ox, oy, ex, ey)
    tip_ang = math.atan2(vy, vx)
    for da in (2.5, -2.5):
        ax = ex - 5 * math.cos(tip_ang + da * 0.35)
        ay = ey - 5 * math.sin(tip_ang + da * 0.35)
        canvas.line(ex, ey, ax, ay)
    canvas.line(ox, oy, ex, oy)
    canvas.line(ex, oy, ex, ey)
    mag = math.hypot(vx, vy)
    ux, uy = math.cos(ang), math.sin(ang)
    header = f"v=({ux:+0.2f}, {uy:+0.2f})  ‖v‖={mag / max(length, 1):0.2f}·L  θ={ang * 180 / math.pi:5.1f}°"
    return f"{header}\n{canvas.render()}"


def frame_matrix(t: float, *, cols: int = 40, rows: int = 11) -> str:
    """Hint visual: transform 2×2 (escala/rotação) num grid de pontos."""
    grid = ascii_plot_grid(cols, rows, fill="·")
    cx, cy = cols // 2, rows // 2
    for x in range(cols):
        grid[cy][x] = "─"
    for y in range(rows):
        grid[y][cx] = "│"
    grid[cy][cx] = "┼"
    ang = (t % 1.0) * 2 * math.pi
    sx = 1.0 + 0.35 * math.sin(ang * 2)
    sy = 1.0 + 0.35 * math.cos(ang * 2)
    c, s = math.cos(ang), math.sin(ang)
    pts = [(-2, -1), (-1, 2), (2, 1), (1, -2), (0, 2), (2, 0)]
    for px, py in pts:
        qx, qy = px * sx, py * sy
        rx = c * qx - s * qy
        ry = s * qx + c * qy
        gx = int(round(cx + rx * 3))
        gy = int(round(cy - ry * 1.6))
        if 0 <= gx < cols and 0 <= gy < rows:
            grid[gy][gx] = "●"
    header = f"A = R({ang * 180 / math.pi:5.1f}°) · diag({sx:0.2f},{sy:0.2f})  y=Ax"
    return f"{header}\n{flatten_grid(grid)}"


def frame_circuit_pulse(t: float, *, cols: int = 42, rows: int = 10) -> str:
    """Pulso em circuito Ohm: V → I através de R."""
    grid = ascii_plot_grid(cols, rows, fill=" ")
    mid = rows // 2
    # fio + resistor
    for x in range(2, cols - 2):
        grid[mid][x] = "─"
    r0 = cols // 2 - 3
    for i, ch in enumerate("┌─┐"):
        grid[mid - 1][r0 + i] = ch
    for i, ch in enumerate("│R│"):
        grid[mid][r0 + i] = ch
    for i, ch in enumerate("└─┘"):
        grid[mid + 1][r0 + i] = ch
    # pulso viajando
    phase = int((t % 1.0) * (cols - 6)) + 2
    if 0 <= phase < cols:
        grid[mid - 2][phase] = "▼"
        grid[max(0, mid - 3)][phase] = "V"
    v = 5.0
    r = 220.0
    i_amp = v / r * 1000  # mA
    pulse = 0.5 + 0.5 * math.sin(t * 2 * math.pi)
    header = f"V={v:0.1f}V  R={r:0.0f}Ω  I={i_amp * pulse:0.2f} mA  (I=V/R)"
    return f"{header}\n{flatten_grid(grid)}"


def frame_adc_ladder(t: float, *, cols: int = 40, rows: int = 10) -> str:
    """Escada ADC: níveis de quantização sobem."""
    grid = ascii_plot_grid(cols, rows, fill="·")
    bits = 3
    levels = 2**bits
    vin = (t % 1.0)
    code = min(levels - 1, int(vin * levels))
    for lvl in range(levels):
        y = rows - 2 - lvl
        if y < 0:
            continue
        width = 4 + lvl * 3
        for x in range(2, min(cols - 2, 2 + width)):
            grid[y][x] = "█" if lvl <= code else "░"
    tip_y = rows - 2 - code
    tip_x = min(cols - 3, 6 + code * 3)
    if 0 <= tip_y < rows:
        grid[tip_y][tip_x] = "◀"
    vref = 3.3
    step = vref / levels
    header = f"ADC {bits}-bit  Vin={vin * vref:0.2f}V  code={code}  Δ={step:0.3f}V"
    return f"{header}\n{flatten_grid(grid)}"


def frame_gradient_descent(t: float, *, cols: int = 42, rows: int = 11) -> str:
    """Partícula descendo uma parábola (gradiente)."""
    canvas = BrailleCanvas(cols, rows)
    mid = canvas.px_h // 2
    # parábola y = (x-c)^2
    last = None
    for i in range(canvas.px_w):
        x = (i / max(1, canvas.px_w - 1)) * 2 - 1  # [-1,1]
        y = x * x
        py = mid + int(y * (mid - 2))
        if last is not None:
            canvas.line(last[0], last[1], i, py)
        last = (i, py)
    # ponto descendo
    prog = min(0.95, t % 1.0)
    x = 0.9 * (1 - prog)  # de +0.9 → 0
    # lado alterna
    if int(t * 2) % 2 == 0:
        x = -x
    y = x * x
    px = int((x + 1) / 2 * (canvas.px_w - 1))
    py = mid + int(y * (mid - 2))
    canvas.set_pixel(px, py)
    # “bola”
    for dx, dy in ((0, 0), (1, 0), (0, 1), (-1, 0)):
        canvas.set_pixel(px + dx, py + dy)
    header = f"min f(x)=x²  x={x:+0.3f}  f'={2 * x:+0.3f}  passo↓"
    return f"{header}\n{canvas.render()}"


def frame_softmax_bars(t: float, *, cols: int = 36, rows: int = 10) -> str:
    """Barras softmax animadas (logits → probs)."""
    logits = [1.0, 2.0 + math.sin(t * 2 * math.pi), 0.5, -0.2]
    m = max(logits)
    exps = [math.exp(z - m) for z in logits]
    s = sum(exps)
    probs = [e / s for e in exps]
    grid = ascii_plot_grid(cols, rows, fill=" ")
    bar_w = max(3, (cols - 4) // len(probs))
    for i, p in enumerate(probs):
        h = max(1, int(p * (rows - 3)))
        x0 = 2 + i * bar_w
        for y in range(rows - 2, rows - 2 - h, -1):
            for x in range(x0, min(cols - 1, x0 + bar_w - 1)):
                grid[y][x] = "█"
        label = f"{p:0.2f}"
        for j, ch in enumerate(label):
            if x0 + j < cols:
                grid[rows - 1][x0 + j] = ch
    header = "softmax(z)  " + "  ".join(f"p{i}={p:0.2f}" for i, p in enumerate(probs))
    return f"{header}\n{flatten_grid(grid)}"


def frame_robot_transform(t: float, *, cols: int = 36, rows: int = 12) -> str:
    """Elo 2D rotacionando (cinemática / transform)."""
    canvas = BrailleCanvas(cols, rows)
    ox, oy = canvas.px_w // 4, canvas.px_h // 2
    canvas.line(2, oy, canvas.px_w - 2, oy)
    canvas.line(ox, 1, ox, canvas.px_h - 2)
    th = (t % 1.0) * 2 * math.pi
    L = min(canvas.px_w, canvas.px_h) * 0.4
    ex = ox + L * math.cos(th)
    ey = oy - L * math.sin(th)
    canvas.line(ox, oy, ex, ey)
    # “garra”
    for da in (0.4, -0.4):
        canvas.line(
            ex,
            ey,
            ex + 6 * math.cos(th + da),
            ey - 6 * math.sin(th + da),
        )
    header = f"T(θ) elo  θ={th * 180 / math.pi:5.1f}°  (x,y)=({math.cos(th):+.2f},{math.sin(th):+.2f})·L"
    return f"{header}\n{canvas.render()}"


def frame_sampling_dots(t: float, *, cols: int = 48, rows: int = 10) -> str:
    """Seno contínuo + amostras discretas (Nyquist hint)."""
    canvas = BrailleCanvas(cols, rows)
    mid = canvas.px_h // 2
    amp = mid - 2
    canvas.line(0, mid, canvas.px_w - 1, mid)
    phase = (t % 1.0) * 2 * math.pi
    last = None
    for i in range(canvas.px_w):
        ang = (i / max(1, canvas.px_w - 1)) * 4 * math.pi + phase
        y = mid - amp * math.sin(ang)
        if last is not None:
            canvas.line(last[0], last[1], i, y)
        last = (i, y)
    # amostras
    n_samp = 8 + int(4 * abs(math.sin(t * math.pi)))
    for k in range(n_samp):
        i = int(k / max(1, n_samp - 1) * (canvas.px_w - 1))
        ang = (i / max(1, canvas.px_w - 1)) * 4 * math.pi + phase
        y = mid - amp * math.sin(ang)
        canvas.set_pixel(i, int(y))
        canvas.set_pixel(i, int(y) - 1)
    header = f"amostragem  N={n_samp} pts/view  fase={phase * 180 / math.pi:4.0f}°"
    return f"{header}\n{canvas.render()}"


def frame_derivative_slope(t: float, *, cols: int = 40, rows: int = 11) -> str:
    """Tangente a uma curva suave."""
    canvas = BrailleCanvas(cols, rows)
    mid = canvas.px_h // 2
    last = None
    for i in range(canvas.px_w):
        x = (i / max(1, canvas.px_w - 1)) * 2 * math.pi
        y = math.sin(x)
        py = mid - y * (mid - 2)
        if last is not None:
            canvas.line(last[0], last[1], i, py)
        last = (i, py)
    x0 = (t % 1.0) * 2 * math.pi
    y0 = math.sin(x0)
    dy = math.cos(x0)
    px = int((t % 1.0) * (canvas.px_w - 1))
    py = mid - y0 * (mid - 2)
    # segmento tangente
    span = 10
    canvas.line(px - span, py + span * dy * 0.6, px + span, py - span * dy * 0.6)
    canvas.set_pixel(px, int(py))
    header = f"f=sin  f'={dy:+0.3f}  em x={x0:0.2f}"
    return f"{header}\n{canvas.render()}"


def frame_probability_bars(t: float, *, cols: int = 36, rows: int = 10) -> str:
    """Distribuição discreta pulsando."""
    n = 5
    base = [0.1, 0.15, 0.4, 0.2, 0.15]
    wobble = [0.05 * math.sin(t * 2 * math.pi + i) for i in range(n)]
    raw = [max(0.01, b + w) for b, w in zip(base, wobble)]
    s = sum(raw)
    probs = [r / s for r in raw]
    grid = ascii_plot_grid(cols, rows, fill=" ")
    bar_w = max(3, (cols - 4) // n)
    for i, p in enumerate(probs):
        h = max(1, int(p * (rows - 3)))
        x0 = 2 + i * bar_w
        for y in range(rows - 2, rows - 2 - h, -1):
            for x in range(x0, min(cols - 1, x0 + bar_w - 1)):
                grid[y][x] = "▓"
    header = "P(X=k)  " + " ".join(f"{p:0.2f}" for p in probs)
    return f"{header}\n{flatten_grid(grid)}"


def frame_quantize_steps(t: float, *, cols: int = 42, rows: int = 10) -> str:
    """Sinal contínuo vs degraus int8-like."""
    canvas = BrailleCanvas(cols, rows)
    mid = canvas.px_h // 2
    amp = mid - 2
    levels = 8
    last_c = last_q = None
    for i in range(canvas.px_w):
        x = (i / max(1, canvas.px_w - 1)) * 2 * math.pi + t * 2 * math.pi
        y = math.sin(x)
        cy = mid - y * amp
        # quantiza
        q = round(y * (levels / 2)) / (levels / 2)
        qy = mid - q * amp
        if last_c is not None:
            canvas.line(last_c[0], last_c[1], i, cy)
        if last_q is not None and i % 2 == 0:
            canvas.line(last_q[0], last_q[1], i, qy)
        last_c = (i, cy)
        last_q = (i, qy)
    header = f"quantização L={levels}  contínuo→degrau  t={t:0.2f}"
    return f"{header}\n{canvas.render()}"


def frame_memory_grid(t: float, *, cols: int = 40, rows: int = 10) -> str:
    """Layout de memória: linha vs coluna sendo varridas."""
    grid = ascii_plot_grid(cols, rows, fill="·")
    bw, bh = 8, 6
    ox, oy = 4, 2
    for y in range(bh):
        for x in range(bw):
            grid[oy + y][ox + x * 2] = "□"
    # cursor row-major
    n = bw * bh
    idx = int((t % 1.0) * n) % n
    cy, cx = divmod(idx, bw) if False else (idx // bw, idx % bw)
    grid[oy + cy][ox + cx * 2] = "■"
    header = f"N · C layout  idx={idx}  row={cy} col={cx}  (cache-friendly →)"
    return f"{header}\n{flatten_grid(grid)}"


def frame_rhythm_bands(t: float, *, cols: int = 48, rows: int = 10) -> str:
    """Séries com overlays α/β/γ (toy)."""
    canvas = BrailleCanvas(cols, rows)
    mid = canvas.px_h // 2
    canvas.line(0, mid, canvas.px_w - 1, mid)
    phase = (t % 1.0) * 2 * math.pi
    bands = ((10.0, 1.0), (20.0, 0.55), (40.0, 0.25))  # µ/α, β, γ-ish
    for freq, amp_s in bands:
        last = None
        amp = (mid - 2) * amp_s
        for i in range(canvas.px_w):
            ang = (i / max(1, canvas.px_w - 1)) * 4 * math.pi * (freq / 10.0) + phase
            y = mid - amp * math.sin(ang)
            if last is not None and i % 2 == 0:
                canvas.line(last[0], last[1], i, y)
            last = (i, y)
    header = "ritmos toy  α/µ≈10  β≈20  γ≈40 Hz  (não clínico)"
    return f"{header}\n{canvas.render()}"


def frame_filter_freq_response(t: float, *, cols: int = 48, rows: int = 10) -> str:
    """Curva de magnitude com banda mu destacada."""
    grid = ascii_plot_grid(cols, rows, fill=" ")
    lo, hi = 8, 12
    sweep = 0.15 + 0.85 * ((t * 0.5) % 1.0)
    for i in range(int(cols * sweep)):
        f = i / max(1, cols - 1) * 50.0  # 0..50 Hz
        # crude bandpass gain
        if lo <= f < hi:
            g = 1.0
        elif f < lo:
            g = max(0.05, 1.0 - (lo - f) / lo)
        else:
            g = max(0.05, 1.0 - (f - hi) / 40.0)
        h = max(1, int(g * (rows - 3)))
        for y in range(rows - 2, rows - 2 - h, -1):
            grid[y][i] = "▓" if lo <= f < hi else "·"
    header = f"|H(f)| toy  banda µ {lo}–{hi} Hz destacada  t={t:0.2f}"
    return f"{header}\n{flatten_grid(grid)}"


def frame_dipole_field(t: float, *, cols: int = 40, rows: int = 12) -> str:
    """Dipolo sob camadas → mapa de escalpo; amplitudes dos eletrodos mudam com θ."""
    canvas = BrailleCanvas(cols, rows)
    cx, cy = canvas.px_w / 2, canvas.px_h * 0.65
    r = min(cx, cy) * 0.7
    # skull arc
    canvas.circle(cx, cy - 2, r, steps=60)
    # dipole orientation θ
    ang = (t % 1.0) * math.pi - math.pi / 2
    dx, dy = 6 * math.cos(ang), -6 * math.sin(ang)
    canvas.line(cx - dx, cy - dy, cx + dx, cy + dy)
    dlen = math.hypot(dx, dy) or 1.0
    ux, uy = dx / dlen, dy / dlen
    # scalp samples: stem height ∝ |projection| — changes with θ
    amp_labels: list[str] = []
    for k in range(7):
        a = math.pi * (0.15 + 0.7 * k / 6)
        px = cx + r * math.cos(a)
        py = cy - 2 - r * math.sin(a) * 0.35
        ex, ey = px - cx, py - cy
        elen = math.hypot(ex, ey) or 1.0
        proj = (ux * ex + uy * ey) / elen
        amp = abs(proj)
        amp_labels.append(f"{amp:0.2f}")
        stem = max(1, int(round(amp * 5)))
        ix, iy = int(px), int(py)
        canvas.set_pixel(ix, iy)
        for h in range(1, stem + 1):
            canvas.set_pixel(ix, iy - h)
    header = (
        f"dipolo→escalpo  θ={ang * 180 / math.pi:5.1f}°  "
        f"amps=[{', '.join(amp_labels)}]  (borrão espacial)"
    )
    return f"{header}\n{canvas.render()}"


def frame_spike_to_lfp(t: float, *, cols: int = 48, rows: int = 12) -> str:
    """Spike → corrente/PSP sináptica → LFP lento. LFP ≠ AP filtrado."""
    canvas = BrailleCanvas(cols, rows)
    h = canvas.px_h
    y_spike = int(h * 0.22)
    y_psp = int(h * 0.50)
    y_lfp = int(h * 0.78)
    canvas.line(0, y_spike, canvas.px_w - 1, y_spike)
    canvas.line(0, y_psp, canvas.px_w - 1, y_psp)
    canvas.line(0, y_lfp, canvas.px_w - 1, y_lfp)
    phase = int((t % 1.0) * 8)
    # spikes (AP)
    spike_xs: list[int] = []
    for i in range(0, canvas.px_w, 7):
        if (i // 7 + phase) % 3 == 0:
            canvas.line(i, y_spike, i, y_spike - 6)
            spike_xs.append(i)
    # synaptic / PSP: exponential-ish bumps after each spike
    last = None
    for i in range(canvas.px_w):
        psp = 0.0
        for sx in spike_xs:
            dt = i - sx
            if 0 <= dt < 18:
                psp += math.exp(-dt / 5.0) * math.sin(dt / 3.0 + 0.2)
        y = y_psp - int(5 * psp)
        if last is not None:
            canvas.line(last[0], last[1], i, y)
        last = (i, y)
    # slow LFP: smoothed / summed synaptic currents (not a filtered AP copy)
    last = None
    for i in range(canvas.px_w):
        y = y_lfp + int(4 * math.sin(i / 10 + t * 2 * math.pi))
        for sx in spike_xs:
            dt = i - sx
            if 0 <= dt < 28:
                y -= int(2.5 * math.exp(-dt / 10.0))
        if last is not None:
            canvas.line(last[0], last[1], i, y)
        last = (i, y)
    header = (
        "AP (cima) → PSP/sinapse (meio) → LFP (baixo)  |  "
        "LFP ≠ potencial de ação filtrado"
    )
    return f"{header}\n{canvas.render()}"


def frame_mi_erds(t: float, *, cols: int = 42, rows: int = 10) -> str:
    """Cartoon ERD↓ then ERS↑ rebound above baseline (educational MI)."""
    grid = ascii_plot_grid(cols, rows, fill=" ")
    baseline = 0.55
    pulse = 0.5 + 0.5 * math.sin(t * 2 * math.pi)
    for i in range(cols):
        x = i / max(1, cols - 1)
        cue = 0.28
        mid = 0.62
        if x < cue:
            p = baseline
        elif x < mid:
            # ERD: dip below baseline during imagery
            u = (x - cue) / (mid - cue)
            p = baseline - 0.35 * math.sin(u * math.pi) * (0.7 + 0.3 * pulse)
        else:
            # ERS rebound: overshoot above baseline, then settle
            u = min(1.0, (x - mid) / (1.0 - mid))
            p = baseline + 0.28 * math.sin(u * math.pi) * (0.75 + 0.25 * pulse)
            p = p - 0.08 * u  # gentle settle toward baseline at end
        h = max(1, int(max(0.08, min(0.95, p)) * (rows - 3)))
        for y in range(rows - 2, rows - 2 - h, -1):
            grid[y][i] = "▓"
        # baseline guide (sparse)
        by = rows - 2 - max(1, int(baseline * (rows - 3)))
        if 0 <= by < rows and grid[by][i] == " ":
            grid[by][i] = "·"
    header = "MI cartoon  µ power  ERD↓ (abaixo baseline) · ERS↑ rebound (acima)  — educacional"
    return f"{header}\n{flatten_grid(grid)}"


def frame_artifact_trace(t: float, *, cols: int = 42, rows: int = 10) -> str:
    """Blink / line-noise spikes on a quieter EEG-like baseline (≠ rhythm_bands)."""
    canvas = BrailleCanvas(cols, rows)
    cy = canvas.px_h * 0.55
    last = None
    phase = t * 2 * math.pi
    for i in range(canvas.px_w):
        x = i / max(1, canvas.px_w - 1)
        y = cy + 1.2 * math.sin(x * 18 + phase)  # quiet baseline
        # ocular blink blobs
        for bx in (0.22, 0.7):
            y -= 5.5 * math.exp(-((x - bx) ** 2) / 0.0018) * (0.6 + 0.4 * math.sin(phase))
        # 50/60-ish ripple bursts
        if 0.4 < x < 0.55:
            y += 1.8 * math.sin(x * 90 + phase * 3)
        if last is not None:
            canvas.line(last[0], last[1], i, y)
        last = (i, y)
    header = "artefatos  blink/EOG (picos) + ripple de linha  — não é mapa de ritmos α/β"
    return f"{header}\n{canvas.render()}"


def frame_closed_loop_timeline(t: float, *, cols: int = 48, rows: int = 8) -> str:
    """Sense / decide / act bars vs deadline."""
    grid = ascii_plot_grid(cols, rows, fill=" ")
    deadline = int(cols * 0.75)
    for y in range(1, rows - 1):
        grid[y][deadline] = "│"
    stages = [("S", 0.20, 2), ("D", 0.35, 4), ("A", 0.15, 6)]
    x = 2
    pulse = int((t % 1.0) * 3)
    for i, (label, frac, row) in enumerate(stages):
        w = max(2, int(frac * (deadline - 4)))
        for j in range(w):
            if 0 <= x + j < cols and 0 <= row < rows:
                grid[row][x + j] = "█" if i == pulse else "▓"
        if x < cols:
            grid[row][min(cols - 1, x)] = label
        x += w + 1
    miss = x > deadline
    header = f"sense→decide→act  deadline@{deadline}  {'MISS' if miss else 'ok'}  t={t:0.2f}"
    return f"{header}\n{flatten_grid(grid)}"


def frame_volume_blur(t: float, *, cols: int = 40, rows: int = 10) -> str:
    """Fonte fina vs mapa de escalpo suave (cartoon — not a FEM solver)."""
    canvas = BrailleCanvas(cols, rows)
    # sharp sources
    for sx in (cols * 0.35, cols * 0.65):
        canvas.set_pixel(int(sx * (canvas.px_w / cols)), int(canvas.px_h * 0.3))
    # blurred scalp line
    cy = canvas.px_h * 0.75
    last = None
    for i in range(canvas.px_w):
        x = i / max(1, canvas.px_w - 1)
        y = cy - 4 * (
            math.exp(-((x - 0.35) ** 2) / 0.02) + math.exp(-((x - 0.65) ** 2) / 0.02)
        ) * (0.7 + 0.3 * math.sin(t * 2 * math.pi))
        if last is not None:
            canvas.line(last[0], last[1], i, y)
        last = (i, y)
    header = (
        "fonte fina (cima) vs borrão de volume no escalpo (baixo)  |  "
        "cartoon 2D — não é FEM/condutividade real"
    )
    return f"{header}\n{canvas.render()}"


_FRAME_FN: dict[str, Callable[..., str]] = {
    "unit_circle": frame_unit_circle,
    "sine_wave": frame_sine_wave,
    "vector": frame_vector,
    "matrix": frame_matrix,
    "circuit_pulse": frame_circuit_pulse,
    "adc_ladder": frame_adc_ladder,
    "gradient_descent": frame_gradient_descent,
    "softmax_bars": frame_softmax_bars,
    "robot_transform": frame_robot_transform,
    "sampling_dots": frame_sampling_dots,
    "derivative_slope": frame_derivative_slope,
    "probability_bars": frame_probability_bars,
    "quantize_steps": frame_quantize_steps,
    "memory_grid": frame_memory_grid,
    "rhythm_bands": frame_rhythm_bands,
    "filter_freq_response": frame_filter_freq_response,
    "dipole_field": frame_dipole_field,
    "spike_to_lfp": frame_spike_to_lfp,
    "mi_erds": frame_mi_erds,
    "closed_loop_timeline": frame_closed_loop_timeline,
    "volume_blur": frame_volume_blur,
    "artifact_trace": frame_artifact_trace,
}

# heurísticas por id de sala
_HEURISTICS: list[tuple[tuple[str, ...], str]] = [
    (("trigon", "trig"), "unit_circle"),
    (("onda", "sin", "wave"), "sine_wave"),
    (("vetor", "vector"), "vector"),
    (("algebra", "matriz", "matrix", "matmul"), "matrix"),
    (("transform",), "robot_transform"),
    (("ohm", "divisao", "tensao"), "circuit_pulse"),
    (("adc", "potencia"), "adc_ladder"),
    (("gradiente",), "gradient_descent"),
    (("derivad",), "derivative_slope"),
    (("softmax",), "softmax_bars"),
    (("amostr", "nyquist"), "sampling_dots"),
    (("probab",), "probability_bars"),
    (("quantiz", "fixed"), "quantize_steps"),
    (("memory", "layout"), "memory_grid"),
    (("cinematica", "sensor", "robo"), "robot_transform"),
]


def animation_for_room(room_id: str, animation: str | None = None) -> AnimKind:
    """Escolhe animação por campo YAML ou heurística do id da sala."""
    if animation and animation in _FRAME_FN:
        return animation  # type: ignore[return-value]
    if animation == "none":
        return "none"
    rid = room_id.lower()
    for keys, kind in _HEURISTICS:
        if any(k in rid for k in keys):
            return kind  # type: ignore[return-value]
    return "none"


def render_frame(kind: AnimKind | str, t: float) -> str:
    fn = _FRAME_FN.get(kind)
    if fn is None:
        return "(sem animação para esta sala — espaço / :anim em salas com visual)"
    return fn(t)


def available_animations() -> list[str]:
    return sorted(_FRAME_FN.keys())
