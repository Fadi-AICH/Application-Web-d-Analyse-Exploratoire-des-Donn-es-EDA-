import streamlit as st

def show_overview(df_original, df_clean):
    st.header("Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", df_clean.shape[0])
    col2.metric("Columns", df_clean.shape[1])
    col3.metric("Missing Values", df_clean.isna().sum().sum())
    col4.metric(
        "Missing %",
        f"{(df_clean.isna().sum().sum() / df_clean.size) * 100:.2f}%"
    )

    st.divider()

    st.subheader("Preview (first 5 rows)")
    st.dataframe(df_clean.head(), use_container_width=True)

    st.subheader("Data Types")
    st.dataframe(
        df_clean.dtypes.astype(str),
        use_container_width=True
    )

    with st.expander("Compare original vs cleaned dataset"):
        col1, col2 = st.columns(2)
        col1.write("Original")
        col1.dataframe(df_original.head())

        col2.write("Cleaned")
        col2.dataframe(df_clean.head())
