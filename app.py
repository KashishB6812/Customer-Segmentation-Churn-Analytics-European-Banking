from pathlib import Path
import numpy as np
import pandas as pd


def load_data(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "Exited" not in df.columns:
        raise ValueError("The dataset must contain an 'Exited' column for the churn target.")
    return df


def prepare_segments(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    def age_group(age: int) -> str:
        if age < 30:
            return "<30"
        elif age < 46:
            return "30-45"
        elif age < 61:
            return "46-60"
        return "60+"

    def credit_band(score: int) -> str:
        if score < 500:
            return "Low"
        elif score < 700:
            return "Medium"
        return "High"

    def tenure_group(tenure: int) -> str:
        if tenure < 3:
            return "New"
        elif tenure < 7:
            return "Mid-term"
        return "Long-term"

    def balance_segment(balance: float) -> str:
        if balance <= 0:
            return "Zero-balance"
        elif balance < 50000:
            return "Low-balance"
        return "High-balance"

    out["AgeGroup"] = out["Age"].map(age_group)
    out["CreditScoreBand"] = out["CreditScore"].map(credit_band)
    out["TenureGroup"] = out["Tenure"].map(tenure_group)
    out["BalanceSegment"] = out["Balance"].map(balance_segment)
    return out


def overall_kpis(df: pd.DataFrame) -> dict:
    total_customers = len(df)
    churn_rate = df["Exited"].mean()

    segment_summary = (
        df.groupby(["Geography", "AgeGroup", "CreditScoreBand", "TenureGroup", "BalanceSegment"], dropna=False)
        .agg(customers=("CustomerId", "count"), churn_rate=("Exited", "mean"))
        .reset_index()
    )
    segment_churn_rate = (
        np.average(segment_summary["churn_rate"], weights=segment_summary["customers"])
        if not segment_summary.empty
        else 0.0
    )

    high_value_threshold = df["Balance"].quantile(0.75)
    high_value = df[df["Balance"] >= high_value_threshold]
    high_value_churn_ratio = high_value["Exited"].mean() if not high_value.empty else 0.0

    geographic_risk = df.groupby("Geography")["Exited"].mean()
    geographic_risk_index = geographic_risk.mean() if not geographic_risk.empty else 0.0

    inactive = df[df["IsActiveMember"] == 0]
    engagement_drop_indicator = inactive["Exited"].mean() if not inactive.empty else 0.0

    return {
        "total_customers": total_customers,
        "overall_churn_rate": churn_rate,
        "segment_churn_rate": segment_churn_rate,
        "high_value_churn_ratio": high_value_churn_ratio,
        "high_value_threshold": high_value_threshold,
        "geographic_risk_index": geographic_risk_index,
        "engagement_drop_indicator": engagement_drop_indicator,
    }


def segment_churn_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby(["Geography", "AgeGroup", "CreditScoreBand", "TenureGroup", "BalanceSegment"], as_index=False, dropna=False)
        .agg(customers=("CustomerId", "count"), churn_rate=("Exited", "mean"))
        .sort_values("churn_rate", ascending=False)
        .reset_index(drop=True)
    )
    return summary


def high_value_metrics(df: pd.DataFrame) -> pd.DataFrame:
    threshold = df["Balance"].quantile(0.75)
    high_value = df[df["Balance"] >= threshold].copy()
    if high_value.empty:
        return pd.DataFrame(columns=["BalanceThreshold", "Geography", "Customers", "ExitedRate", "AvgBalance", "AvgSalary"])

    high_value_summary = (
        high_value.groupby("Geography", as_index=False)
        .agg(
            Customers=("CustomerId", "count"),
            ExitedRate=("Exited", "mean"),
            AvgBalance=("Balance", "mean"),
            AvgSalary=("EstimatedSalary", "mean"),
        )
        .sort_values("ExitedRate", ascending=False)
        .reset_index(drop=True)
    )
    high_value_summary["BalanceThreshold"] = threshold
    return high_value_summary


def churn_profile_summary(df: pd.DataFrame) -> pd.DataFrame:
    profile = (
        df.groupby("ChurnStatus", as_index=False)
        .agg(
            AvgAge=("Age", "mean"),
            AvgBalance=("Balance", "mean"),
            AvgSalary=("EstimatedSalary", "mean"),
            AvgTenure=("Tenure", "mean"),
            Customers=("CustomerId", "count"),
        )
    )
    return profile
