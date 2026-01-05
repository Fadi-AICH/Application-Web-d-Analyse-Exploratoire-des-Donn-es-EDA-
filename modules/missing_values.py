import streamlit as st
import pandas as pd
import plotly.express as px

def missing_analysis(df: pd.DataFrame):
    st.header("🧩 Missing Values Analysis")

    if df.empty:
        st.warning("Dataset is empty")
        return

    missing_count = df.isna().sum()
    missing_pct = (missing_count / len(df)) * 100

    missing_df = pd.DataFrame({
        "Missing Count": missing_count,
        "Missing %": missing_pct
    }).sort_values("Missing %", ascending=False)

    missing_df = missing_df[missing_df["Missing Count"] > 0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Missing Values", int(missing_count.sum()))
    col2.metric(
        "Columns Affected",
        int((missing_count > 0).sum())
    )
    col3.metric(
        "Worst Column %",
        f"{missing_pct.max():.2f}%" if not missing_df.empty else "0%"
    )

    st.divider()

    if missing_df.empty:
        st.success("No missing values detected in the dataset")
        return

    st.subheader("Missing values per column")
    st.dataframe(
        missing_df.style.format({"Missing %": "{:.2f}%"})
    )

    st.subheader("Missing values distribution")

    fig = px.bar(
        missing_df.reset_index(),
        x="index",
        y="Missing %",
        title="Percentage of missing values per column",
        labels={"index": "Column"},
        color="Missing %",
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Impact severity")

    def severity(p):
        if p < 5:
            return "Low"
        elif p <= 30:
            return "Medium"
        return "Critical"

    missing_df["Severity"] = missing_df["Missing %"].apply(severity)

    st.dataframe(
        missing_df[["Missing %", "Severity"]]
        .style.applymap(
            lambda x: (
                "color: #16a34a" if x == "Low"
                else "color: #eab308" if x == "Medium"
                else "color: #dc2626"
            ),
            subset=["Severity"]
        )
    )

    st.subheader("Most impacted variables")
    st.dataframe(
        missing_df[missing_df["Severity"] == "Critical"]
    )
