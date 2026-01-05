import streamlit as st
import plotly.express as px
import pandas as pd

def show_visualizations(df: pd.DataFrame):
    st.header("📈 Data Visualisation")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    if df.empty:
        st.warning("Dataset is empty")
        return

    plot_type = st.selectbox(
        "Select visualization type",
        [
            "Histogram",
            "Boxplot (Outliers)",
            "Bar Chart (Categorical)",
            "Scatter Plot (Relationship)"
        ]
    )

    st.divider()

    if plot_type == "Histogram":
        if not numeric_cols:
            st.error("No numeric variables available")
            return

        col = st.selectbox("Select numeric variable", numeric_cols)

        fig = px.histogram(
            df,
            x=col,
            nbins=30,
            title=f"Distribution of {col}",
            marginal="box"
        )

        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Boxplot (Outliers)":
        if not numeric_cols:
            st.error("No numeric variables available")
            return

        col = st.selectbox("Select numeric variable", numeric_cols)

        fig = px.box(
            df,
            y=col,
            title=f"Boxplot of {col}"
        )

        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Bar Chart (Categorical)":
        if not cat_cols:
            st.error("No categorical variables available")
            return

        col = st.selectbox("Select categorical variable", cat_cols)

        value_counts = df[col].value_counts().reset_index()
        value_counts.columns = [col, "Count"]

        fig = px.bar(
            value_counts,
            x=col,
            y="Count",
            title=f"Category distribution of {col}"
        )

        st.plotly_chart(fig, use_container_width=True)


    elif plot_type == "Scatter Plot (Relationship)":
        if len(numeric_cols) < 2:
            st.error("Need at least two numeric variables")
            return

        x = st.selectbox("X axis", numeric_cols)
        y = st.selectbox("Y axis", numeric_cols, index=1)

        fig = px.scatter(
            df,
            x=x,
            y=y,
            title=f"{x} vs {y}",
            trendline="ols"
        )

        st.plotly_chart(fig, use_container_width=True)
