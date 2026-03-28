from prism.data import headline_metrics


def test_headline_metrics_match_public_story():
    metrics = headline_metrics()

    assert round(metrics.mechanism_macro_f1, 3) == 0.962
    assert metrics.best_crash_model == "RandomForestRegressor"
    assert round(metrics.best_crash_rmse, 3) == 0.863
    assert round(metrics.best_crash_r2, 3) == 0.454
    assert round(metrics.causal_avg_post_coef, 3) == -0.379
    assert round(metrics.causal_pretrend_p, 3) == 0.095

