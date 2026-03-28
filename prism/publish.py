"""Generate public-facing figures and summary tables."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from prism.config import FIGURES_DIR, TABLES_DIR
from prism.data import (
    benchmark_label_balance,
    benchmark_source_balance,
    crash_model_comparison,
    headline_metrics,
    load_mechanism_comparison,
    load_scenario_forecasts,
    primary_event_study,
)
from prism.io import ensure_dir


def _box(ax, x: float, y: float, w: float, h: float, text: str, face: str, edge: str) -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.025",
        linewidth=1.4,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(patch)
    ax.text(x + (w / 2.0), y + (h / 2.0), text, ha="center", va="center", fontsize=11, weight="bold")


def _arrow(ax, start: tuple[float, float], end: tuple[float, float]) -> None:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=14, linewidth=1.3, color="#2f3e46"))


def _save_pipeline_architecture(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    _box(ax, 0.04, 0.63, 0.22, 0.18, "Policy Text\nBenchmark", "#dbeafe", "#1d4ed8")
    _box(ax, 0.39, 0.63, 0.22, 0.18, "Causal Audit\nEvent Study", "#dcfce7", "#15803d")
    _box(ax, 0.74, 0.63, 0.22, 0.18, "Crash Forecast\nScenario Engine", "#fee2e2", "#b91c1c")

    _box(ax, 0.04, 0.20, 0.22, 0.16, "Audited\nBenchmark", "#eff6ff", "#2563eb")
    _box(ax, 0.39, 0.20, 0.22, 0.16, "State-Year\nCrash Panel", "#f0fdf4", "#16a34a")
    _box(ax, 0.74, 0.20, 0.22, 0.16, "Public Figures\nAnd Tables", "#fff7ed", "#ea580c")

    _arrow(ax, (0.15, 0.63), (0.15, 0.36))
    _arrow(ax, (0.50, 0.63), (0.50, 0.36))
    _arrow(ax, (0.85, 0.63), (0.85, 0.36))
    _arrow(ax, (0.26, 0.72), (0.39, 0.72))
    _arrow(ax, (0.61, 0.72), (0.74, 0.72))

    ax.text(
        0.5,
        0.92,
        "PRISM Public Research Stack",
        ha="center",
        va="center",
        fontsize=16,
        weight="bold",
        color="#111827",
    )
    ax.text(
        0.5,
        0.07,
        "The public repo keeps the strongest mechanism, causal, and forecasting outputs separate.",
        ha="center",
        va="center",
        fontsize=10,
        color="#374151",
    )

    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _save_mechanism_ladder(path: Path) -> None:
    df = load_mechanism_comparison().sort_values("macro_f1")
    colors = ["#9ca3af"] * len(df)
    winner_idx = df.index[df["selected_model"]].tolist()
    if winner_idx:
        colors[df.index.get_loc(winner_idx[0])] = "#1d4ed8"

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.barh(df["model"], df["macro_f1"], color=colors)
    ax.set_xlabel("Macro-F1")
    ax.set_title("Mechanism Benchmark Comparison")
    ax.set_xlim(0, 1.0)
    for y, value in enumerate(df["macro_f1"]):
        ax.text(value + 0.01, y, f"{value:.3f}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _save_event_study(path: Path) -> None:
    df = primary_event_study()

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.axhline(0, color="#111827", linewidth=1)
    ax.axvline(-1, color="#6b7280", linestyle="--", linewidth=1)
    ax.errorbar(
        df["event_time"],
        df["coef"],
        yerr=[df["coef"] - df["ci_low"], df["ci_high"] - df["coef"]],
        fmt="o",
        color="#047857",
        ecolor="#10b981",
        capsize=4,
    )
    ax.set_xlabel("Event Time")
    ax.set_ylabel("Coefficient")
    ax.set_title("Causal Audit: Alcohol-Impaired Fatality Rate")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _save_forecast_comparison(path: Path) -> None:
    df = crash_model_comparison().sort_values("test_rmse", ascending=False)
    winner = df["model"].iloc[df["test_rmse"].argmin()]
    colors = ["#9ca3af" if model != winner else "#b91c1c" for model in df["model"]]

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.barh(df["model"], df["test_rmse"], color=colors)
    ax.set_xlabel("Test RMSE")
    ax.set_title("Held-Out Crash Forecast Comparison")
    for y, value in enumerate(df["test_rmse"]):
        ax.text(value + 0.015, y, f"{value:.3f}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _save_scenario_deltas(path: Path) -> None:
    df = load_scenario_forecasts().sort_values("delta").head(12)
    colors = ["#15803d" if value <= 0 else "#dc2626" for value in df["delta"]]

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.barh(df["state_abbrev"], df["delta"], color=colors)
    ax.axvline(0, color="#111827", linewidth=1)
    ax.set_xlabel("Predicted Delta")
    ax.set_title("Scenario Forecast Deltas")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _headline_metrics_table() -> pd.DataFrame:
    metrics = headline_metrics()
    return pd.DataFrame(
        [
            {
                "metric": "mechanism_macro_f1",
                "value": round(metrics.mechanism_macro_f1, 6),
                "display": f"{metrics.mechanism_macro_f1:.3f}",
                "note": "Selected benchmark model on the audited mechanism dataset.",
            },
            {
                "metric": "best_crash_model",
                "value": metrics.best_crash_model,
                "display": metrics.best_crash_model,
                "note": "Lowest held-out test RMSE on the crash task.",
            },
            {
                "metric": "best_crash_rmse",
                "value": round(metrics.best_crash_rmse, 6),
                "display": f"{metrics.best_crash_rmse:.3f}",
                "note": "Held-out crash forecasting error.",
            },
            {
                "metric": "best_crash_r2",
                "value": round(metrics.best_crash_r2, 6),
                "display": f"{metrics.best_crash_r2:.3f}",
                "note": "Held-out crash forecasting fit.",
            },
            {
                "metric": "causal_avg_post_coef",
                "value": round(metrics.causal_avg_post_coef, 6),
                "display": f"{metrics.causal_avg_post_coef:.3f}",
                "note": "Average post-event coefficient for impaired fatality rate.",
            },
            {
                "metric": "causal_pretrend_p",
                "value": round(metrics.causal_pretrend_p, 6),
                "display": f"{metrics.causal_pretrend_p:.3f}",
                "note": "Pretrend diagnostic for the primary causal audit.",
            },
        ]
    )


def build_results(figures_dir: Path | None = None, tables_dir: Path | None = None) -> dict[str, Path]:
    figures_dir = ensure_dir(figures_dir or FIGURES_DIR)
    tables_dir = ensure_dir(tables_dir or TABLES_DIR)

    outputs = {
        "pipeline_arch": figures_dir / "pipeline_arch.png",
        "mechanism_ladder": figures_dir / "mechanism_ladder.png",
        "event_study": figures_dir / "event_study_pub.png",
        "forecast_comparison": figures_dir / "forecast_comparison.png",
        "scenario_deltas": figures_dir / "scenario_deltas.png",
        "headline_metrics": tables_dir / "headline_metrics.csv",
        "causal_event_study_primary": tables_dir / "causal_event_study_primary.csv",
        "crash_model_comparison": tables_dir / "crash_model_comparison.csv",
        "mechanism_benchmark_overview": tables_dir / "mechanism_benchmark_overview.csv",
        "mechanism_benchmark_sources": tables_dir / "mechanism_benchmark_sources.csv",
    }

    _save_pipeline_architecture(outputs["pipeline_arch"])
    _save_mechanism_ladder(outputs["mechanism_ladder"])
    _save_event_study(outputs["event_study"])
    _save_forecast_comparison(outputs["forecast_comparison"])
    _save_scenario_deltas(outputs["scenario_deltas"])

    _headline_metrics_table().to_csv(outputs["headline_metrics"], index=False)
    primary_event_study().to_csv(outputs["causal_event_study_primary"], index=False)
    crash_model_comparison().to_csv(outputs["crash_model_comparison"], index=False)
    benchmark_label_balance().to_csv(outputs["mechanism_benchmark_overview"], index=False)
    benchmark_source_balance().to_csv(outputs["mechanism_benchmark_sources"], index=False)

    return outputs

