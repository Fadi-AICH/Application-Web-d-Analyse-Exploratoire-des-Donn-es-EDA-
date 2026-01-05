import streamlit as st
import pandas as pd

def load_data():
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success("Dataset loaded")
            return df
        except Exception as e:
            st.sidebar.error("Failed to load file")
            st.sidebar.error(str(e))
            return None

    return None
