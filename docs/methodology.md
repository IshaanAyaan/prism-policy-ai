# Methodology

PRISM is organized around three deliberately separated tasks:

1. Mechanism interpretation of policy text.
2. Historical causal audit around a clean policy event.
3. Next-year crash forecasting under a standardized scenario.

This public repository keeps the outputs and summaries for all three tasks, while limiting the executable surface to the curated artifacts that support the strongest public story.

## Mechanism Benchmark

The benchmark is a frozen 250-row audited dataset of policy text snippets labeled for three mechanisms:

- `price`
- `access`
- `enforcement`

The selected benchmark result in this repo is the audited v3 comparison table. The public package uses that table to regenerate benchmark figures and summary tables.

## Causal Audit

The causal artifact in this repo is an event-study table around the first real-dollar beer-tax increase in treated states. The headline quantity reported in the README is the average post-event coefficient for `rate_impaired_per100k`, paired with the pretrend diagnostic.

## Forecasting

The forecasting artifact in this repo is the held-out model comparison table plus a standardized scenario forecast table. The crash comparison is evaluated on the 2020-2023 test period, and the scenario table reports baseline, shifted forecast, delta, and approximate interval bounds by state.

## Public-Repo Philosophy

This repo is not the raw ETL or full experimentation workspace. It is a public curation that emphasizes:

- clear scientific separation between causal and predictive claims
- audited benchmark outputs
- compact, lab-facing documentation
- small tracked artifacts that can be inspected quickly

