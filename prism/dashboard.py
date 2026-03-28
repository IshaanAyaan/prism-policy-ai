"""Read-only dashboard for the curated public PRISM repo."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from prism.data import (
    benchmark_label_balance,
    crash_model_comparison,
    headline_metrics,
    load_mechanism_comparison,
    load_mechanism_state_year,
    load_panel,
    load_scenario_forecasts,
    primary_event_study,
)


@st.cache_data
def load_data():
    return {
        "panel": load_panel(),
        "mechanism_state": load_mechanism_state_year(),
        "mechanism_comparison": load_mechanism_comparison(),
        "crash_models": crash_model_comparison(),
        "scenario": load_scenario_forecasts(),
        "event": primary_event_study(),
        "label_balance": benchmark_label_balance(),
        "headline": headline_metrics(),
    }


def main() -> None:
    st.set_page_config(page_title="PRISM", layout="wide")
    data = load_data()
    headline = data["headline"]

    st.title("PRISM")
    st.caption("Curated public dashboard for the mechanism benchmark, causal audit, and crash forecasting outputs.")

    cols = st.columns(3)
    cols[0].metric("Mechanism Macro-F1", f"{headline.mechanism_macro_f1:.3f}")
    cols[1].metric("Best Crash RMSE", f"{headline.best_crash_rmse:.3f}", headline.best_crash_model)
    cols[2].metric("Avg Post Coef", f"{headline.causal_avg_post_coef:.3f}", f"pretrend p={headline.causal_pretrend_p:.3f}")

    states = sorted(data["panel"]["state_abbrev"].unique().tolist())
    state = st.sidebar.selectbox("State", states, index=states.index("CA") if "CA" in states else 0)

    overview_tab, benchmark_tab, forecast_tab = st.tabs(["Overview", "Mechanism Benchmark", "Forecast"])

    with overview_tab:
        state_panel = data["panel"][data["panel"]["state_abbrev"] == state].sort_values("year")
        state_mech = data["mechanism_state"][data["mechanism_state"]["state_abbrev"] == state].sort_values("year")

        fig_outcomes = px.line(
            state_panel,
            x="year",
            y=["rate_impaired_per100k", "rate_alcohol_involved_per100k"],
            markers=True,
            title=f"{state} crash outcomes over time",
        )
        st.plotly_chart(fig_outcomes, use_container_width=True)

        fig_mech = px.line(
            state_mech,
            x="year",
            y=["mech_v3_price_score", "mech_v3_access_score", "mech_v3_enforcement_score"],
            markers=True,
            title=f"{state} mechanism profile over time",
        )
        st.plotly_chart(fig_mech, use_container_width=True)

    with benchmark_tab:
        st.dataframe(data["mechanism_comparison"].sort_values("macro_f1", ascending=False), use_container_width=True)

        fig_ladder = px.bar(
            data["mechanism_comparison"].sort_values("macro_f1"),
            x="macro_f1",
            y="model",
            orientation="h",
            color="selected_model",
            title="Mechanism benchmark comparison",
        )
        st.plotly_chart(fig_ladder, use_container_width=True)

        fig_balance = px.bar(
            data["label_balance"],
            x="mechanism",
            y="positive_rows",
            title="Audited benchmark label balance",
        )
        st.plotly_chart(fig_balance, use_container_width=True)

    with forecast_tab:
        st.dataframe(data["crash_models"], use_container_width=True)

        fig_models = px.bar(
            data["crash_models"].sort_values("test_rmse", ascending=False),
            x="test_rmse",
            y="model",
            orientation="h",
            title="Held-out crash model comparison",
        )
        st.plotly_chart(fig_models, use_container_width=True)

        fig_scenario = px.bar(
            data["scenario"].sort_values("delta").head(15),
            x="delta",
            y="state_abbrev",
            orientation="h",
            title="Top scenario deltas",
            color="delta",
            color_continuous_scale="RdYlGn_r",
        )
        st.plotly_chart(fig_scenario, use_container_width=True)

        fig_event = px.scatter(
            data["event"],
            x="event_time",
            y="coef",
            error_y=data["event"]["ci_high"] - data["event"]["coef"],
            error_y_minus=data["event"]["coef"] - data["event"]["ci_low"],
            title="Primary event-study coefficients",
        )
        st.plotly_chart(fig_event, use_container_width=True)


if __name__ == "__main__":
    main()

