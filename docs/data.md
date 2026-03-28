# Data

This repository keeps only lightweight processed artifacts that support the public story.

## Included Files

- `data/processed/panel_state_year.parquet`
  - `1,071` rows
  - `17` columns
  - one row per jurisdiction-year for the crash-policy panel
- `data/processed/policy_text_mechanism_state_year_v3.parquet`
  - `1,071` rows
  - `39` columns
  - state-year mechanism scores, provenance, and text-derived features
- `data/processed/mechanism_benchmark.csv`
  - `250` rows
  - audited benchmark snippets and final mechanism labels
- `data/processed/causal_effects_eventstudy.csv`
  - `20` rows
  - event-study coefficients and diagnostics for the public causal summary
- `data/processed/model_eval_summary_v3.csv`
  - `13` rows
  - held-out model comparison table including crash and archived auxiliary tasks
- `results/tables/mechanism_model_comparison.csv`
  - `6` rows
  - public benchmark comparison table
- `results/tables/scenario_forecasts_v3.csv`
  - `51` rows
  - baseline and shifted forecasts by state

## Excluded By Design

- raw data downloads
- intermediate ETL products
- presentation decks and design files
- teen-wave artifacts
- manual labeling helpers and API-dependent drafting code

The public repo is intentionally compact so that a reviewer can understand the project quickly.

