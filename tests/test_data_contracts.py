from prism.data import (
    load_benchmark,
    load_mechanism_state_year,
    load_panel,
    load_scenario_forecasts,
)


def test_panel_contract():
    panel = load_panel()
    assert panel.shape == (1071, 17)
    assert {"state_abbrev", "year", "rate_impaired_per100k", "beer_tax_usd_per_gallon"} <= set(panel.columns)


def test_mechanism_state_year_contract():
    mechanism = load_mechanism_state_year()
    assert mechanism.shape[0] == 1071
    assert {"mech_v3_price_score", "mech_v3_access_score", "mech_v3_enforcement_score", "coverage_provenance"} <= set(mechanism.columns)


def test_benchmark_and_scenario_contracts():
    benchmark = load_benchmark()
    scenario = load_scenario_forecasts()

    assert benchmark.shape[0] == 250
    assert {"chunk_text", "final_price", "final_access", "final_enforcement"} <= set(benchmark.columns)
    assert scenario.shape[0] == 51
    assert {"forecast_baseline", "forecast_scenario", "delta"} <= set(scenario.columns)

