"""Project-wide paths for the public PRISM repo."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
TABLES_DIR = RESULTS_DIR / "tables"
DOCS_DIR = ROOT / "docs"

PANEL_PATH = PROCESSED_DIR / "panel_state_year.parquet"
MECHANISM_STATE_YEAR_PATH = PROCESSED_DIR / "policy_text_mechanism_state_year_v3.parquet"
BENCHMARK_PATH = PROCESSED_DIR / "mechanism_benchmark.csv"
EVENT_STUDY_PATH = PROCESSED_DIR / "causal_effects_eventstudy.csv"
MODEL_EVAL_PATH = PROCESSED_DIR / "model_eval_summary_v3.csv"
MECHANISM_COMPARISON_PATH = TABLES_DIR / "mechanism_model_comparison.csv"
SCENARIO_FORECAST_PATH = TABLES_DIR / "scenario_forecasts_v3.csv"

