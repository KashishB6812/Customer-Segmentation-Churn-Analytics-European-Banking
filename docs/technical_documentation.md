import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

from src.churn_analysis import (
    high_value_metrics,
    load_data,
    overall_kpis,
    prepare_segments,
    segment_churn_summary,
)


DATA_PATH = Path(__file__).resolve().parent / "data" / "customer_churn_europe.csv"


def main():
    st.set_page_config(page_title="Bank Churn Analytics Dashboard", layout="wide")
    st.title("European Banking Customer Segmentation & Churn Pattern Analytics")

    if not DATA_PATH.exists():
        st.warning("Dataset not found. Run: python data/generate_data.py")
        return

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
        st.warning("No records match the current filter selection.")
        return

    kpis = overall_kpis(filtered)
    st.subheader("Executive KPI Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Customers", f"{kpis['total_customers']:,}")
    col2.metric("Overall Churn Rate", f"{kpis['overall_churn_rate']:.2%}")
    col3.metric("High-Value Churn Ratio", f"{kpis['high_value_churn_ratio']:.2%}")
    col4.metric("Geographic Risk Index", f"{kpis['geographic_risk_index']:.2%}")
    col5.metric("Inactive Churn Risk", f"{kpis['engagement_drop_indicator']:.2%}")

    st.markdown("---")

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
        text_auto=".2%",
        labels={"churn_rate": "Churn Rate"},
    )

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
        text_auto=".2%",
        labels={"churn_rate": "Churn Rate"},
    )

    tenure_summary = (
        filtered.groupby("TenureGroup", as_index=False)["Exited"]
        .agg(churn_rate="mean", customers="size")
        .sort_values("churn_rate", ascending=False)
    )
    fig_tenure = px.bar(
        tenure_summary,
        x="TenureGroup",
        y="churn_rate",
        color="TenureGroup",
        title="Churn Rate by Tenure Group",
        text_auto=".2%",
        labels={"churn_rate": "Churn Rate"},
    )

    col_left, col_center, col_right = st.columns(3)
    col_left.plotly_chart(fig_geography, use_container_width=True)
    col_center.plotly_chart(fig_age, use_container_width=True)
    col_right.plotly_chart(fig_tenure, use_container_width=True)

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

    st.subheader("Salary vs Balance Relationship")
    scatter_fig = px.scatter(
        comp,
        x="EstimatedSalary",
        y="Balance",
        color="ChurnStatus",
        title="Estimated Salary vs Balance by Churn Status",
        opacity=0.7,
    )
    st.plotly_chart(scatter_fig, use_container_width=True)


if __name__ == "__main__":
    main()
