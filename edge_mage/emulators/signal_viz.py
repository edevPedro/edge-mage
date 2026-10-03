"""
signal_viz — Visualizador de sinais biológicos e EEG para terminal (pure Python).

Renderiza formas de onda de séries temporais multicanal (e.g. C3, Cz, C4),
espectro de potência (PSD) com bandas fisiológicas (Delta, Theta, Alpha/Mu,
Beta, Gamma), barras de potência relativa e espectrogramas no terminal.
"""

from __future__ import annotations

import argparse
import cmath
import math
from typing import Sequence


# ── Bandas fisiológicas de EEG ────────────────────────────────────────────────
EEG_BANDS: dict[str, tuple[float, float, str]] = {
    "delta": (0.5, 4.0, "δ (0.5-4 Hz)"),
    "theta": (4.0, 8.0, "θ (4-8 Hz)"),
    "alpha": (8.0, 13.0, "α/µ (8-13 Hz)"),
    "beta":  (13.0, 30.0, "β (13-30 Hz)"),
    "gamma": (30.0, 50.0, "γ (30-50 Hz)"),
}


# ── Renderizadores de Formas de Onda ──────────────────────────────────────────

def render_ascii_wave(
    signal: Sequence[float],
    width: int = 60,
    height: int = 7,
    title: str = "",
    unit: str = "µV",
    sample_rate_hz: float = 250.0,
) -> str:
    """
    Renderiza um sinal 1D como gráfico ASCII com eixo de amplitude e tempo.

    :param signal: Sequência de valores numéricos (e.g. em µV).
    :param width: Largura do gráfico em colunas de texto (excluindo rótulos).
    :param height: Altura do gráfico em linhas (mínimo 3).
    :param title: Título opcional exibido no cabeçalho.
    :param unit: Unidade da amplitude (e.g. 'µV', 'V').
    :param sample_rate_hz: Taxa de amostragem em Hz para o eixo de tempo.
    """
    if not signal:
        return "[Sinal vazio]"

    n_samples = len(signal)
    height = max(3, height)
    plot_w = max(10, width)

    # Subamostragem / interpolação simples para plot_w colunas
    downsampled: list[float] = []
    for c in range(plot_w):
        # Média das amostras correspondentes à coluna c
        idx_start = int(c * n_samples / plot_w)
        idx_end = max(idx_start + 1, int((c + 1) * n_samples / plot_w))
        chunk = signal[idx_start:idx_end]
        downsampled.append(sum(chunk) / len(chunk))

    sig_min = min(downsampled)
    sig_max = max(downsampled)
    if abs(sig_max - sig_min) < 1e-12:
        sig_max += 1.0
        sig_min -= 1.0

    span = sig_max - sig_min

    # Grade de caracteres
    grid = [[" "] * plot_w for _ in range(height)]

    # Linha zero se estiver dentro do intervalo
    zero_row = None
    if sig_min <= 0.0 <= sig_max:
        zero_row = int((sig_max - 0.0) / span * (height - 1) + 0.5)
        for col in range(plot_w):
            grid[zero_row][col] = "┄"

    # Mapear pontos
    for col, val in enumerate(downsampled):
        row_f = (sig_max - val) / span * (height - 1)
        row = max(0, min(height - 1, int(row_f + 0.5)))
        # Se cruzar com a linha zero
        if row == zero_row:
            grid[row][col] = "┼"
        else:
            grid[row][col] = "●"

    lines: list[str] = []
    if title:
        duration_ms = (n_samples / sample_rate_hz) * 1000.0
        lines.append(f"┌─ {title} ({duration_ms:.0f} ms @ {sample_rate_hz:.0f} Hz) " + "─" * max(0, plot_w - len(title) - 25))

    label_w = 11
    for r in range(height):
        lvl = sig_max - r * span / (height - 1)
        lbl = f"{lvl:+6.1f} {unit}"
        sep = "┼" if r == zero_row else "│"
        row_str = "".join(grid[r])
        lines.append(f"{lbl} {sep}{row_str}")

    # Eixo X
    lines.append(" " * label_w + "└" + "─" * plot_w)
    # Ticks de tempo (0 ms ... N ms)
    tot_ms = (n_samples / sample_rate_hz) * 1000.0
    tick_str = f"0 ms" + " " * (plot_w - len(f"0 ms") - len(f"{tot_ms:.0f} ms")) + f"{tot_ms:.0f} ms"
    lines.append(" " * (label_w + 1) + tick_str)

    return "\n".join(lines)


def render_multichannel_waves(
    channels: dict[str, Sequence[float]],
    width: int = 60,
    height_per_ch: int = 4,
    sample_rate_hz: float = 250.0,
    unit: str = "µV",
) -> str:
    """
    Renderiza múltiplos canais de EEG (e.g. C3, Cz, C4) empilhados verticalmente.
    """
    if not channels:
        return "[Nenhum canal fornecido]"

    out_lines: list[str] = []
    plot_w = max(10, width)
    first_ch = next(iter(channels.values()))
    tot_samples = len(first_ch) if first_ch else 0
    duration_s = tot_samples / sample_rate_hz

    header = f"=== Montagem EEG Multicanal ({len(channels)} canais · {duration_s*1000:.0f} ms @ {sample_rate_hz:.0f} Hz) ==="
    out_lines.append(header)

    ch_name_w = max(len(k) for k in channels.keys())
    ch_name_w = max(4, ch_name_w)

    for ch_name, sig in channels.items():
        if not sig:
            out_lines.append(f"{ch_name.ljust(ch_name_w)}: [vazio]")
            continue
        n_samples = len(sig)
        downsampled: list[float] = []
        for c in range(plot_w):
            idx_s = int(c * n_samples / plot_w)
            idx_e = max(idx_s + 1, int((c + 1) * n_samples / plot_w))
            chk = sig[idx_s:idx_e]
            downsampled.append(sum(chk) / len(chk))

        s_min, s_max = min(downsampled), max(downsampled)
        if abs(s_max - s_min) < 1e-12:
            s_max += 1.0; s_min -= 1.0
        span = s_max - s_min

        grid = [[" "] * plot_w for _ in range(height_per_ch)]
        for col, val in enumerate(downsampled):
            row_f = (s_max - val) / span * (height_per_ch - 1)
            row = max(0, min(height_per_ch - 1, int(row_f + 0.5)))
            grid[row][col] = "─" if abs(val) < span * 0.1 else ("▔" if val > 0 else " ")
            grid[row][col] = "●"

        for r in range(height_per_ch):
            prefix = ch_name.ljust(ch_name_w) if r == height_per_ch // 2 else " " * ch_name_w
            out_lines.append(f"{prefix} │{''.join(grid[r])}")
        out_lines.append(" " * ch_name_w + " │" + "┄" * plot_w)

    # Time axis
    out_lines.append(" " * (ch_name_w + 2) + f"0 ms" + " " * (plot_w - len("0 ms") - len(f"{duration_s*1000:.0f} ms")) + f"{duration_s*1000:.0f} ms")
    return "\n".join(out_lines)


# ── Análise Espectral e PSD ───────────────────────────────────────────────────

def compute_simple_psd(
    signal: Sequence[float],
    fs: float = 250.0,
    n_fft: int = 128,
) -> tuple[list[float], list[float]]:
    """
    Calcula a densidade espectral de potência (PSD) simplificada via periodograma com janela Hanning.
    Pure Python (sem dependência de numpy/scipy).

    Retorna (freqs_hz, psd_db).
    """
    n = len(signal)
    if n < n_fft:
        n_fft = max(16, n)

    # Segmento com janela de Hanning
    window = [0.5 * (1.0 - math.cos(2.0 * math.pi * i / (n_fft - 1))) for i in range(n_fft)]
    win_sum_sq = sum(w * w for w in window) or 1.0

    # Média sobre blocos com 50% overlap (Welch lite)
    step = n_fft // 2
    n_half = n_fft // 2 + 1
    power_acc = [0.0] * n_half
    n_blocks = 0

    for start in range(0, n - n_fft + 1, step):
        segment = [signal[start + i] * window[i] for i in range(n_fft)]
        # DFT ingênua para os n_half bins
        for k in range(n_half):
            w = 2.0 * math.pi * k / n_fft
            c_val = sum(segment[t] * cmath.exp(-1j * w * t) for t in range(n_fft))
            power_acc[k] += (abs(c_val) ** 2) / (fs * win_sum_sq)
        n_blocks += 1

    if n_blocks == 0:
        return [0.0], [-100.0]

    freqs = [k * fs / n_fft for k in range(n_half)]
    psd_db: list[float] = []
    for k in range(n_half):
        p = power_acc[k] / n_blocks
        val_db = 10.0 * math.log10(max(1e-12, p))
        psd_db.append(val_db)

    return freqs, psd_db


def compute_bandpowers(
    freqs: Sequence[float],
    psd_db: Sequence[float],
) -> dict[str, float]:
    """
    Calcula a potência média em dB para cada banda fisiológica clássica de EEG.
    """
    band_powers: dict[str, float] = {}
    for band_name, (f_low, f_high, _) in EEG_BANDS.items():
        vals = [
            psd_db[i]
            for i, f in enumerate(freqs)
            if f_low <= f <= f_high
        ]
        if vals:
            band_powers[band_name] = sum(vals) / len(vals)
        else:
            band_powers[band_name] = -100.0
    return band_powers


def render_ascii_spectrum(
    freqs: Sequence[float],
    psd_db: Sequence[float],
    width: int = 60,
    height: int = 8,
    max_freq_hz: float = 60.0,
    title: str = "Densidade Espectral de Potência (PSD)",
) -> str:
    """
    Renderiza um gráfico ASCII da PSD (dB vs Hz) com marcadores de bandas fisiológicas.
    """
    # Filtrar até max_freq_hz
    pairs = [(f, p) for f, p in zip(freqs, psd_db) if f <= max_freq_hz]
    if not pairs:
        return "[Sem dados de espectro]"

    f_filt, p_filt = zip(*pairs)
    plot_w = max(15, width)
    height = max(4, height)

    # Subamostrar para plot_w
    d_psd: list[float] = []
    d_freq: list[float] = []
    for c in range(plot_w):
        idx_s = int(c * len(f_filt) / plot_w)
        idx_e = max(idx_s + 1, int((c + 1) * len(f_filt) / plot_w))
        chunk_p = p_filt[idx_s:idx_e]
        chunk_f = f_filt[idx_s:idx_e]
        d_psd.append(sum(chunk_p) / len(chunk_p))
        d_freq.append(sum(chunk_f) / len(chunk_f))

    p_min = min(d_psd)
    p_max = max(d_psd)
    if abs(p_max - p_min) < 1e-6:
        p_max += 1.0; p_min -= 1.0
    span = p_max - p_min

    grid = [[" "] * plot_w for _ in range(height)]
    for col, val in enumerate(d_psd):
        row_f = (p_max - val) / span * (height - 1)
        row = max(0, min(height - 1, int(row_f + 0.5)))
        grid[row][col] = "█"
        # Preencher abaixo da curva
        for r in range(row + 1, height):
            grid[r][col] = "░"

    lines: list[str] = []
    lines.append(f"┌─ {title} ─ [0..{max_freq_hz:.0f} Hz] " + "─" * max(0, plot_w - len(title) - 20))

    label_w = 9
    for r in range(height):
        lvl = p_max - r * span / (height - 1)
        lbl = f"{lvl:+5.1f} dB"
        lines.append(f"{lbl} │{''.join(grid[r])}")

    lines.append(" " * label_w + "└" + "─" * plot_w)

    # Ticks de frequência e bandas
    # Marcar posições de Alpha (8-13 Hz) e Beta (13-30 Hz)
    tick_line = [" "] * plot_w
    band_line = [" "] * plot_w

    def set_label(s: str, pos: int, target: list[str]) -> None:
        for i, ch in enumerate(s):
            if 0 <= pos + i < len(target):
                target[pos + i] = ch

    for f_tick in [0, 10, 20, 30, 40, 50, int(max_freq_hz)]:
        pos = int(f_tick / max_freq_hz * (plot_w - 1))
        set_label(f"{f_tick}", pos, tick_line)

    # Band indicators
    alpha_center = 10.5
    pos_alpha = int(alpha_center / max_freq_hz * (plot_w - 1))
    set_label("α/µ", max(0, pos_alpha - 1), band_line)

    beta_center = 21.5
    pos_beta = int(beta_center / max_freq_hz * (plot_w - 1))
    set_label("β", pos_beta, band_line)

    lines.append(" " * (label_w + 1) + "".join(tick_line) + " (Hz)")
    lines.append(" " * (label_w + 1) + "".join(band_line))

    return "\n".join(lines)


def render_bandpower_bars(
    band_powers_db: dict[str, float],
    width: int = 35,
) -> str:
    """
    Renderiza um gráfico de barras comparativo da potência em dB em cada banda de EEG.
    """
    if not band_powers_db:
        return "[Sem bandas]"

    vals = list(band_powers_db.values())
    v_min = min(vals)
    v_max = max(vals)
    if abs(v_max - v_min) < 1e-6:
        v_max += 1.0; v_min -= 1.0
    span = v_max - v_min

    lines: list[str] = ["┌─ Distribuição de Potência por Banda ────────────────────┐"]
    for b_key, (_, _, label) in EEG_BANDS.items():
        val = band_powers_db.get(b_key, v_min)
        ratio = max(0.0, min(1.0, (val - v_min) / span))
        bar_len = int(ratio * width)
        bar_str = "█" * bar_len + "░" * (width - bar_len)
        star = " ★" if val == v_max else "  "
        lines.append(f"│ {label.ljust(16)} [{bar_str}] {val:+5.1f} dB{star}│")
    lines.append("└─────────────────────────────────────────────────────────┘")
    return "\n".join(lines)


def render_ascii_spectrogram(
    matrix: list[list[float]],
    freqs: Sequence[float] | None = None,
    width: int = 50,
    height: int = 8,
) -> str:
    """
    Renderiza uma matriz 2D (frequência × tempo) como espectrograma ASCII com blocos de densidade.
    """
    if not matrix or not matrix[0]:
        return "[Matriz de espectrograma vazia]"

    n_freqs = len(matrix)
    n_times = len(matrix[0])
    levels = [" ", "░", "▒", "▓", "█"]

    all_vals = [val for row in matrix for val in row]
    v_min, v_max = min(all_vals), max(all_vals)
    span = max(1e-12, v_max - v_min)

    grid = [[" "] * width for _ in range(height)]
    for r in range(height):
        freq_idx = int((height - 1 - r) * (n_freqs - 1) / max(1, height - 1))
        for c in range(width):
            time_idx = int(c * (n_times - 1) / max(1, width - 1))
            val = matrix[freq_idx][time_idx]
            lvl_idx = int((val - v_min) / span * (len(levels) - 1) + 0.5)
            lvl_idx = max(0, min(len(levels) - 1, lvl_idx))
            grid[r][c] = levels[lvl_idx]

    lines: list[str] = ["┌─ Espectrograma (Frequência ↑ vs Tempo →) ───────────────"]
    for r in range(height):
        f_lbl = f"{freqs[int((height - 1 - r) * (n_freqs - 1) / max(1, height - 1))]:3.0f}Hz" if freqs else f"F{r:02d}"
        lines.append(f"{f_lbl} │{''.join(grid[r])}")
    lines.append("     └" + "─" * width)
    lines.append("      t=0" + " " * (width - 7) + "t=T")
    return "\n".join(lines)


# ── Demo / CLI ────────────────────────────────────────────────────────────────

def _demo() -> None:
    print("=== signal_viz: Visualização de Sinais Biológicos e EEG ===\n")

    # 1. Gerar sinal sintético com ritmo Mu (10 Hz) e artefato
    fs = 250.0
    duration_s = 1.5
    n_pts = int(fs * duration_s)
    t = [i / fs for i in range(n_pts)]

    # Canal C3: 10 Hz Mu burst + ruído
    c3 = [
        15.0 * math.sin(2.0 * math.pi * 10.0 * ti)
        + 3.0 * math.sin(2.0 * math.pi * 22.0 * ti)
        + (math.sin(i * 3.7) * 2.0)
        for i, ti in enumerate(t)
    ]
    # Canal Cz: linha de base mais estável
    cz = [
        5.0 * math.sin(2.0 * math.pi * 10.0 * ti)
        + (math.sin(i * 2.1) * 3.0)
        for i, ti in enumerate(t)
    ]
    # Canal C4: com artefato de piscada nos primeiros 300 ms
    c4 = []
    for i, ti in enumerate(t):
        blink = 80.0 * math.exp(-((ti - 0.2) ** 2) / 0.005)
        c4.append(blink + 12.0 * math.sin(2.0 * math.pi * 10.0 * ti) + (math.sin(i * 1.5) * 2.0))

    # Demo 1: Forma de onda individual (C3 com ritmo Mu)
    print("1. Forma de Onda Individual — Canal C3 (Ritmo Mu / 10 Hz):")
    wave_str = render_ascii_wave(c3, width=55, height=7, title="Canal C3 (Sensório-motor)")
    for line in wave_str.splitlines():
        print("  " + line)
    print()

    # Demo 2: Montagem Multicanal
    print("2. Montagem Multicanal EEG (C3, Cz, C4 — repare na piscada em C4):")
    multi_str = render_multichannel_waves({"C3": c3, "Cz": cz, "C4": c4}, width=55, height_per_ch=3)
    for line in multi_str.splitlines():
        print("  " + line)
    print()

    # Demo 3: Espectro de Potência (PSD)
    print("3. Densidade Espectral de Potência (PSD) — Pico evidente em 10 Hz (Ritmo Mu/Alpha):")
    freqs, psd = compute_simple_psd(c3, fs=fs, n_fft=128)
    spec_str = render_ascii_spectrum(freqs, psd, width=55, height=7, max_freq_hz=45.0)
    for line in spec_str.splitlines():
        print("  " + line)
    print()

    # Demo 4: Barras de Potência por Banda
    print("4. Distribuição Relativa de Potência por Banda Fisiológica:")
    band_powers = compute_bandpowers(freqs, psd)
    bars_str = render_bandpower_bars(band_powers, width=30)
    for line in bars_str.splitlines():
        print("  " + line)
    print()


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="signal_viz: Visualização ASCII de sinais EEG")
    p.parse_args(argv)
    _demo()


if __name__ == "__main__":
    main()
