import streamlit as st
import pandas as pd
import numpy as np

def show_insights(df: pd.DataFrame):
    st.header("🧠 Automatic Insights")

    if df.empty:
        st.warning("Dataset is empty")
        return

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        st.info("No numeric variables available for insights")
        return

    st.subheader("High correlations")

    corr = numeric_df.corr().abs()
    corr_pairs = (
        corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        .stack()
        .sort_values(ascending=False)
    )

    high_corr = corr_pairs[corr_pairs > 0.8]

    if high_corr.empty:
        st.success("No strong correlations detected")
    else:
        st.dataframe(
            high_corr.rename("Correlation").reset_index(),
            use_container_width=True
        )

    st.divider()

    st.subheader("High variance variables")

    variance = numeric_df.var().sort_values(ascending=False)
    st.dataframe(
        variance.rename("Variance").reset_index(),
        use_container_width=True
    )

    st.divider()

    st.subheader("Outlier detection (IQR method)")

    outlier_summary = {}

    for col in numeric_df.columns:
        q1 = numeric_df[col].quantile(0.25)
        q3 = numeric_df[col].quantile(0.75)
        iqr = q3 - q1
        outliers = numeric_df[
            (numeric_df[col] < q1 - 1.5 * iqr) |
            (numeric_df[col] > q3 + 1.5 * iqr)
        ]
        outlier_summary[col] = len(outliers)

    outlier_df = (
        pd.DataFrame.from_dict(outlier_summary, orient="index", columns=["Outliers"])
        .sort_values("Outliers", ascending=False)
    )

    st.dataframe(outlier_df, use_container_width=True)
