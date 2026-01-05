import streamlit as st
import pandas as pd
from io import BytesIO

def export_data(df: pd.DataFrame, log: list):
    st.header("⬇️ Export Cleaned Dataset")

    if df.empty:
        st.warning("Dataset is empty")
        return

    st.subheader("Preview of cleaned data")
    st.dataframe(df.head(10), use_container_width=True)

    st.divider()

    filename = st.text_input(
        "File name (without extension)",
        value="cleaned_data"
    )

    st.divider()

    st.subheader("Transformation log")

    if log:
        for i, entry in enumerate(log, start=1):
            st.write(f"{i}. {entry}")
    else:
        st.info("No transformations applied")

    st.divider()

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📄 Download CSV",
        data=csv,
        file_name=f"{filename}.csv",
        mime="text/csv"
    )

    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Cleaned_Data")

    st.download_button(
        label="📊 Download Excel",
        data=excel_buffer.getvalue(),
        file_name=f"{filename}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
