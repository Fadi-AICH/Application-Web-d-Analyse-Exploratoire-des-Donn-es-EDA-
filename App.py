import streamlit as st

from modules.insights import show_insights
from modules.data_loader import load_data
from modules.data_overview import show_overview
from modules.visualization import show_visualizations
from modules.missing_values import missing_analysis
from modules.preprocessing import preprocessing_section
from modules.export import export_data

st.set_page_config(
    page_title="EDA Pro Application",
    page_icon="📈",
    layout="wide"
)

if "df_original" not in st.session_state:
    st.session_state.df_original = None

if "df_clean" not in st.session_state:
    st.session_state.df_clean = None

if "log" not in st.session_state:
    st.session_state.log = []

st.title("📊 Exploratory Data Analysis Application")
st.caption("Interactive data exploration, cleaning, transformation and export")

st.sidebar.header("Navigation")

section = st.sidebar.radio(
    "Go to",
    [
    "📁 Upload & Overview",
    "📈 Visualization",
    "🧩 Missing Values",
    "⚙️ Preprocessing",
    "🧠 Insights",
    "⬇️ Export"
]
)

st.sidebar.divider()

if st.sidebar.button("🔄 Reset dataset"):
    st.session_state.df_original = None
    st.session_state.df_clean = None
    st.session_state.log = []
    st.rerun()

df = load_data()

if df is not None:
    if st.session_state.df_original is None:
        st.session_state.df_original = df.copy()
        st.session_state.df_clean = df.copy()

if st.session_state.df_clean is not None:
    if section == "📁 Upload & Overview":
        show_overview(
            st.session_state.df_original,
            st.session_state.df_clean
        )

    elif section == "📈 Visualization":
        show_visualizations(st.session_state.df_clean)

    elif section == "🧩 Missing Values":
        missing_analysis(st.session_state.df_clean)

    elif section == "⚙️ Preprocessing":
        st.session_state.df_clean = preprocessing_section(
            st.session_state.df_clean,
            st.session_state.log
        )
    elif section == "🧠 Insights":
        show_insights(st.session_state.df_clean)

    elif section == "⬇️ Export":
        export_data(st.session_state.df_clean, st.session_state.log)

else:
    st.info("Please upload a CSV file to start.")
