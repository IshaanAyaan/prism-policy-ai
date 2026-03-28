from prism.publish import build_results


def test_build_results_writes_expected_files(tmp_path):
    figures_dir = tmp_path / "figures"
    tables_dir = tmp_path / "tables"

    outputs = build_results(figures_dir=figures_dir, tables_dir=tables_dir)

    expected = {
        "pipeline_arch",
        "mechanism_ladder",
        "event_study",
        "forecast_comparison",
        "scenario_deltas",
        "headline_metrics",
        "causal_event_study_primary",
        "crash_model_comparison",
        "mechanism_benchmark_overview",
        "mechanism_benchmark_sources",
    }
    assert set(outputs) == expected
    for path in outputs.values():
        assert path.exists()

