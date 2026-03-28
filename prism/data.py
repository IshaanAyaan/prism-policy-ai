"""Load and summarize curated PRISM artifacts."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from prism.config import (
    BENCHMARK_PATH,
    EVENT_STUDY_PATH,
    MECHANISM_COMPARISON_PATH,
    MECHANISM_STATE_YEAR_PATH,
    MODEL_EVAL_PATH,
    PANEL_PATH,
    SCENARIO_FORECAST_PATH,
)


@dataclass(frozen=True)
class HeadlineMetrics:
    mechanism_macro_f1: float
    best_crash_model: str
    best_crash_rmse: float
    best_crash_r2: float
    causal_avg_post_coef: float
    causal_pretrend_p: float


def load_panel() -> pd.DataFrame:
    return pd.read_parquet(PANEL_PATH)


def load_mechanism_state_year() -> pd.DataFrame:
    return pd.read_parquet(MECHANISM_STATE_YEAR_PATH)


def load_benchmark() -> pd.DataFrame:
    return pd.read_csv(BENCHMARK_PATH)


def load_event_study() -> pd.DataFrame:
    return pd.read_csv(EVENT_STUDY_PATH)


def load_model_eval() -> pd.DataFrame:
    return pd.read_csv(MODEL_EVAL_PATH)


def load_mechanism_comparison() -> pd.DataFrame:
    return pd.read_csv(MECHANISM_COMPARISON_PATH)


def load_scenario_forecasts() -> pd.DataFrame:
    return pd.read_csv(SCENARIO_FORECAST_PATH)


def primary_event_study() -> pd.DataFrame:
    df = load_event_study()
    return (
        df.loc[df["outcome"] == "rate_impaired_per100k", ["event_time", "coef", "ci_low", "ci_high", "p_value", "pretrend_pvalue"]]
        .sort_values("event_time")
        .reset_index(drop=True)
    )


def crash_model_comparison() -> pd.DataFrame:
    df = load_model_eval()
    return (
        df.loc[df["task"] == "crash_rate_next_year", ["model", "val_rmse", "test_rmse", "test_mae", "test_r2", "n_train", "n_val", "n_test"]]
        .sort_values("test_rmse")
        .reset_index(drop=True)
    )


def benchmark_label_balance() -> pd.DataFrame:
    df = load_benchmark()
    rows = []
    for label in ["price", "access", "enforcement"]:
        rows.append(
            {
                "mechanism": label,
                "positive_rows": int(df[f"final_{label}"].sum()),
                "share": float(df[f"final_{label}"].mean()),
            }
        )
    return pd.DataFrame(rows)


def benchmark_source_balance() -> pd.DataFrame:
    df = load_benchmark()
    counts = df["source_type"].value_counts().rename_axis("source_type").reset_index(name="rows")
    counts["share"] = counts["rows"] / counts["rows"].sum()
    return counts


def headline_metrics() -> HeadlineMetrics:
    mechanism = load_mechanism_comparison()
    winner = mechanism.loc[mechanism["selected_model"]].head(1)
    if winner.empty:
        winner = mechanism.sort_values("macro_f1", ascending=False).head(1)

    crash = crash_model_comparison().head(1)
    event = primary_event_study()
    post = event.loc[event["event_time"] >= 0, "coef"]

    return HeadlineMetrics(
        mechanism_macro_f1=float(winner.iloc[0]["macro_f1"]),
        best_crash_model=str(crash.iloc[0]["model"]),
        best_crash_rmse=float(crash.iloc[0]["test_rmse"]),
        best_crash_r2=float(crash.iloc[0]["test_r2"]),
        causal_avg_post_coef=float(post.mean()),
        causal_pretrend_p=float(event["pretrend_pvalue"].dropna().iloc[0]),
    )

