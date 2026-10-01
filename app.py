import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from pathlib import Path

from src.churn_analysis import (
    load_data,
    prepare_segments,
    overall_kpis,
    segment_churn_summary,
    high_value_metrics,
)


DATA_PATH = Path(__file__).resolve().parent / "data" / "customer_churn_europe.csv"


def main():
    st.set_page_config(page_title="Bank Churn Analytics Dashboard", layout="wide")
    st.title("European Banking Customer Segmentation & Churn Pattern Analytics")

    df = load_data(DATA_PATH)
    df = prepare_segments(df)

    st.sidebar.header("Filters")
    geography = st.sidebar.multiselect(
        "Geography",
        sorted(df["Geography"].unique()),
        default=sorted(df["Geography"].unique()),
    )
    genders = st.sidebar.multiselect(
        "Gender",
        sorted(df["Gender"].unique()),
        default=sorted(df["Gender"].unique()),
    )
    age_min, age_max = st.sidebar.slider(
        "Age range",
        int(df["Age"].min()),
        int(df["Age"].max()),
        (int(df["Age"].min()), int(df["Age"].max())),
    )

    filtered = df[
        df["Geography"].isin(geography)
        & df["Gender"].isin(genders)
        & df["Age"].between(age_min, age_max)
    ].copy()

    if filtered.empty:
        st.warning("No records match the current filters.")
        return

    kpis = overall_kpis(filtered)
    st.subheader("Executive KPI Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Overall Churn Rate", f"{kpis['overall_churn_rate']:.2%}")
    col2.metric("Segment Churn Rate", f"{kpis['segment_churn_rate']:.2%}")
    col3.metric("High-Value Churn Ratio", f"{kpis['high_value_churn_ratio']:.2%}")
    col4.metric("Geographic Risk Index", f"{kpis['geographic_risk_index']:.2f}")
    col5.metric("Engagement Drop Indicator", f"{kpis['engagement_drop_indicator']:.2%}")

    region_summary = (
        filtered.groupby("Geography", as_index=False)["Exited"]
        .agg(churn_rate="mean", customers="size")
        .sort_values("churn_rate", ascending=False)
    )
    fig_geography = px.bar(
        region_summary,
        x="Geography",
        y="churn_rate",
        color="Geography",
        title="Churn Rate by Geography",
        text_auto='.2%',
        labels={"churn_rate": "Churn Rate"},
    )
    st.plotly_chart(fig_geography, use_container_width=True)

    age_summary = (
        filtered.groupby("AgeGroup", as_index=False)["Exited"]
        .agg(churn_rate="mean", customers="size")
        .sort_values("churn_rate", ascending=False)
    )
    fig_age = px.bar(
        age_summary,
        x="AgeGroup",
        y="churn_rate",
        color="AgeGroup",
        title="Churn Rate by Age Group",
        text_auto='.2%',
        labels={"churn_rate": "Churn Rate"},
    )
    st.plotly_chart(fig_age, use_container_width=True)

    balance_summary = (
        filtered.groupby("BalanceSegment", as_index=False)["Exited"]
        .agg(churn_rate="mean", customers="size")
        .sort_values("churn_rate", ascending=False)
    )
    fig_balance = px.bar(
        balance_summary,
        x="BalanceSegment",
        y="churn_rate",
        color="BalanceSegment",
        title="Churn Rate by Balance Segment",
        text_auto='.2%',
        labels={"churn_rate": "Churn Rate"},
    )
    st.plotly_chart(fig_balance, use_container_width=True)

    st.subheader("Segment-Level Churn Analysis")
    seg_summary = segment_churn_summary(filtered)
    st.dataframe(seg_summary.head(25), use_container_width=True)

    st.subheader("High-Value Customer Churn Explorer")
    hv = high_value_metrics(filtered)
    st.dataframe(hv, use_container_width=True)

    st.subheader("Customer Profile Comparison")
    comp = filtered.assign(ChurnStatus=np.where(filtered["Exited"] == 1, "Exited", "Retained"))
    profile_fig = px.histogram(
        comp,
        x="Balance",
        color="ChurnStatus",
        barmode="overlay",
        title="Balance Distribution by Churn Status",
        nbins=35,
    )
    st.plotly_chart(profile_fig, use_container_width=True)


if __name__ == "__main__":
    main()
