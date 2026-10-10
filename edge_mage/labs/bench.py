"""Estatística de benchmark honesta: percentis, mediana e detecção de ruído."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MetricSummary:
    name: str
    median: float
    p50: float
    p99: float
    p999: float
    min: float
    max: float
    mean: float
    cv: float  # coeficiente de variação (std/mean)
    samples: int

    def to_dict(self) -> dict:
        return {
            "median": self.median,
            "p50": self.p50,
            "p99": self.p99,
            "p999": self.p999,
            "min": self.min,
            "max": self.max,
            "mean": self.mean,
            "cv": self.cv,
            "samples": self.samples,
        }


@dataclass
class Aggregate:
    metrics: dict[str, MetricSummary] = field(default_factory=dict)
    noisy: bool = False
    noisy_metrics: list[str] = field(default_factory=list)
    valid_runs: int = 0


def percentile(values: list[float], q: float) -> float:
    """Percentil com interpolação linear (q em 0..100)."""
    if not values:
        raise ValueError("percentile de lista vazia")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (q / 100.0) * (len(ordered) - 1)
    lo = int(rank)
    hi = min(lo + 1, len(ordered) - 1)
    frac = rank - lo
    return ordered[lo] + (ordered[hi] - ordered[lo]) * frac


def _summarize(name: str, values: list[float]) -> MetricSummary:
    n = len(values)
    mean = sum(values) / n
    ordered = sorted(values)
    if n > 1 and mean != 0:
        var = sum((x - mean) ** 2 for x in values) / (n - 1)
        cv = (var ** 0.5) / abs(mean)
    else:
        cv = 0.0
    return MetricSummary(
        name=name,
        median=percentile(values, 50),
        p50=percentile(values, 50),
        p99=percentile(values, 99),
        p999=percentile(values, 99.9),
        min=ordered[0],
        max=ordered[-1],
        mean=mean,
        cv=cv,
        samples=n,
    )


def _flatten_run(run: dict, prefix: str = "") -> dict[str, float]:
    """Achata dicts aninhados em chaves pontuadas; ignora não-numéricos/bool."""
    flat: dict[str, float] = {}
    for key, value in run.items():
        name = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            flat[name] = float(value)
        elif isinstance(value, dict):
            flat.update(_flatten_run(value, name))
    return flat


def _is_tail_percentile(key: str) -> bool:
    """p99/p999/max/min de poucas execuções oscilam por amostragem — não indicam máquina ocupada."""
    return key.rsplit(".", 1)[-1] in ("p99", "p999", "max", "min")


def _gates_noise(key: str) -> bool:
    """Métricas que decidem se a máquina está ocupada (estáveis, não derivadas)."""
    if key in ("ops", "correct"):
        return False
    if key.startswith("throughput"):
        return False
    return not _is_tail_percentile(key)


def aggregate_runs(
    runs: list[dict],
    *,
    noise_cv: float = 0.15,
) -> Aggregate:
    """
    Agrega várias execuções independentes do benchmark.

    Regra: nunca uma única execução. Cada métrica vira mediana/min/max/cv
    entre as execuções; cv alto marca a métrica como ruidosa.

    O gate de ruído só usa métricas estáveis (p50): percentis de cauda e
    throughput derivado variam por amostragem/outliers mesmo numa máquina
    ociosa e continuam sendo reportados na evidência como informação.
    """
    agg = Aggregate(valid_runs=len(runs))
    if not runs:
        return agg

    keys: set[str] = set()
    flat_runs = [_flatten_run(r) for r in runs]
    for fr in flat_runs:
        keys.update(fr.keys())

    for key in sorted(keys):
        values = [fr[key] for fr in flat_runs if key in fr]
        if len(values) < 2:
            continue
        summary = _summarize(key, values)
        agg.metrics[key] = summary
        if not _gates_noise(key):
            continue
        if summary.cv > noise_cv:
            agg.noisy = True
            agg.noisy_metrics.append(key)

    return agg


def get_metric(agg: Aggregate, dotted: str) -> MetricSummary | None:
    return agg.metrics.get(dotted)
