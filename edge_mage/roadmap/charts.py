"""Gráficos SVG e Markdown, zero dependências (§11).

SVG à mão (Python puro) para `wsh view`; tabelas Markdown para README. Sem
Tauri, sem libs de plot. A curva de p99 no tempo vem do evidence log (histórico
append-only) — um único ponto nunca é suficiente (§7).
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

_PALETTE = ["#3b82f6", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6", "#64748b"]


def _esc(s: str) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _svg_open(width: int, height: int, title: str) -> list[str]:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        "<style>text{font-family:ui-monospace,SFMono-Regular,monospace;font-size:11px;fill:#334155}"
        ".axis{stroke:#cbd5e1}.grid{stroke:#e2e8f0}</style>",
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
    ]
    if title:
        parts.append(f'<text x="18" y="18" font-weight="bold" font-size="13">{_esc(title)}</text>')
    return parts


def bar_chart_svg(
    labels: list,
    values: list,
    *,
    title: str = "",
    width: int = 540,
    height: int = 190,
    color: str = _PALETTE[0],
    value_fmt: str = "{:.0f}",
) -> str:
    n = max(len(values), 1)
    pad_l, pad_r, pad_t, pad_b = 34, 16, 30, 30
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    base_y = pad_t + plot_h
    maxv = max(values) if values and max(values) > 0 else 1.0
    bw = plot_w / n
    parts = _svg_open(width, height, title)
    parts.append(f'<line class="axis" x1="{pad_l}" y1="{base_y}" x2="{width-pad_r}" y2="{base_y}"/>')
    best = n - 1 if n > 1 else 0
    prev = len(values) - 1 if values else -1
    for i, val in enumerate(values):
        h = plot_h * (val / maxv)
        x = pad_l + i * bw + bw * 0.15
        w = bw * 0.7
        y = base_y - h
        fill = color if i != prev else "#1d4ed8"
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" rx="2"/>')
        parts.append(f'<text x="{x + w/2:.1f}" y="{base_y + 14}" text-anchor="middle">{_esc(labels[i])}</text>')
        if val:
            parts.append(f'<text x="{x + w/2:.1f}" y="{y - 3:.1f}" text-anchor="middle">{_esc(value_fmt.format(val))}</text>')
    parts.append("</svg>")
    return "".join(parts)


def line_chart_svg(
    points: list,
    *,
    title: str = "",
    width: int = 560,
    height: int = 210,
    color: str = _PALETTE[1],
    value_fmt: str = "{:.4g}",
) -> str:
    pad_l, pad_r, pad_t, pad_b = 48, 16, 30, 34
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    base_y = pad_t + plot_h
    parts = _svg_open(width, height, title)
    parts.append(f'<line class="axis" x1="{pad_l}" y1="{base_y}" x2="{width-pad_r}" y2="{base_y}"/>')
    parts.append(f'<line class="axis" x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{base_y}"/>')
    if not points:
        parts.append(f'<text x="{width/2:.0f}" y="{height/2:.0f}" text-anchor="middle">sem dados</text>')
        parts.append("</svg>")
        return "".join(parts)
    vals = [float(v) for _, v in points]
    labels = [lab for lab, _ in points]
    vmin, vmax = min(vals), max(vals)
    span = (vmax - vmin) or (abs(vmax) or 1.0)
    n = len(points)
    step = plot_w / (n - 1) if n > 1 else 0

    def px(i: int) -> float:
        return pad_l + i * step

    def py(v: float) -> float:
        return base_y - plot_h * ((v - vmin) / span)

    parts.append(f'<text x="{pad_l-6}" y="{py(vmax)+4:.1f}" text-anchor="end">{_esc(value_fmt.format(vmax))}</text>')
    parts.append(f'<text x="{pad_l-6}" y="{py(vmin)+4:.1f}" text-anchor="end">{_esc(value_fmt.format(vmin))}</text>')
    poly = " ".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(vals))
    parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{poly}"/>')
    for i, v in enumerate(vals):
        parts.append(f'<circle cx="{px(i):.1f}" cy="{py(v):.1f}" r="2.5" fill="{color}"/>')
    for i, lab in enumerate(labels):
        if n <= 8 or i in (0, n - 1) or i % max(1, n // 6) == 0:
            parts.append(f'<text x="{px(i):.1f}" y="{base_y + 16}" text-anchor="middle">{_esc(lab[-5:])}</text>')
    parts.append("</svg>")
    return "".join(parts)


def weekly_bar_svg(labels: list, counts: list, *, title: str = "evidências PASS por dia") -> str:
    return bar_chart_svg(labels, counts, title=title)


def metric_series(
    records: list,
    *,
    challenge_id: str | None = None,
    metric: str | None = None,
    stat: str = "p99",
) -> list[tuple[str, float]]:
    """Série (data, valor) do histórico de evidências para uma métrica/estatística."""
    pts: list[tuple[str, float]] = []
    for r in sorted(records, key=lambda x: x.timestamp):
        if not getattr(r, "is_pass", False) or not r.metrics or not r.timestamp:
            continue
        if challenge_id and r.challenge_id != challenge_id:
            continue
        name = metric
        if name is None:
            for k, v in r.metrics.items():
                if isinstance(v, dict) and stat in v:
                    name = k
                    break
        if not name:
            continue
        entry = r.metrics.get(name)
        if isinstance(entry, dict) and stat in entry:
            try:
                pts.append((r.timestamp.split("T", 1)[0], float(entry[stat])))
            except (TypeError, ValueError):
                continue
    return pts


def week_labels(start: date) -> list[str]:
    from datetime import timedelta

    return [(start + timedelta(days=i)).strftime("%a")[:3] for i in range(7)]


def write_svg(path: Path, svg: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    return path


def markdown_table(headers: list[str], rows: list[list]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out)
