# Results

## Mechanism Benchmark

- Selected model: `tfidf_semisupervised_ffn`
- Headline score: `Macro-F1 = 0.962`
- Benchmark size: `250` audited rows

The strongest public AI result in PRISM is not a general-purpose pretrained language model. The benchmark winner is a domain-specific model selection outcome on a constrained, audited task.

## Crash Forecasting

- Best held-out model: `RandomForestRegressor`
- Test RMSE: `0.863`
- Test R²: `0.454`

The important result is that the best crash forecaster is a strong tabular baseline. That is part of the scientific story rather than an inconvenience.

## Causal Audit

- Outcome: `rate_impaired_per100k`
- Average post-event coefficient: `-0.379`
- Pretrend diagnostic: `p = 0.095`

The sign is consistent with harm reduction after beer-tax increases, but the evidence is not definitive. The public repo keeps that framing explicit.

## Scenario Engine

The checked-in scenario table provides state-level baseline and shifted forecasts under a standardized policy adjustment. Those deltas are predictive summaries meant for comparison, not causal treatment effects.

