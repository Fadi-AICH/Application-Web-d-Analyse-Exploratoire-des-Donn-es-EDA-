import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder

def preprocessing_section(df: pd.DataFrame, log: list):
    st.header("⚙️ Data Preprocessing")

    if df.empty:
        st.warning("Dataset is empty")
        return df

    st.subheader("1. Missing Values Treatment")

    col = st.selectbox("Select column", df.columns)

    method = st.selectbox(
        "Select method",
        [
            "None",
            "Fixed value",
            "Mean",
            "Median",
            "Most frequent",
            "Forward fill",
            "Backward fill"
        ]
    )

    if st.button("Apply missing value treatment"):
        if method != "None":
            if method == "Fixed value":
                value = st.text_input("Enter replacement value")
                df[col] = df[col].fillna(value)
            elif method == "Mean":
                df[col] = df[col].fillna(df[col].mean())
            elif method == "Median":
                df[col] = df[col].fillna(df[col].median())
            elif method == "Most frequent":
                df[col] = df[col].fillna(df[col].mode()[0])
            elif method == "Forward fill":
                df[col] = df[col].ffill()
            elif method == "Backward fill":
                df[col] = df[col].bfill()

            log.append(f"{col}: missing values handled using {method}")
            st.success("Missing values processed")

    st.divider()

    st.subheader("2. Categorical Encoding")

    cat_cols = df.select_dtypes(include="object").columns.tolist()

    if cat_cols:
        enc_col = st.selectbox("Select categorical column", cat_cols)
        enc_method = st.radio("Encoding method", ["One-Hot Encoding", "Label Encoding"])

        if st.button("Apply encoding"):
            if enc_method == "One-Hot Encoding":
                df = pd.get_dummies(df, columns=[enc_col])
                log.append(f"{enc_col}: one-hot encoded")
            else:
                le = LabelEncoder()
                df[enc_col] = le.fit_transform(df[enc_col])
                log.append(f"{enc_col}: label encoded")

            st.success("Encoding applied")
    else:
        st.info("No categorical variables available")

    st.divider()

    st.subheader("3. Scaling")

    scale_method = st.radio(
        "Scaling method",
        ["None", "Min-Max Normalization", "Standardization (Z-score)"]
    )

    if st.button("Apply scaling"):
        num_cols = df.select_dtypes(include="number").columns

        if scale_method == "Min-Max Normalization":
            scaler = MinMaxScaler()
            df[num_cols] = scaler.fit_transform(df[num_cols])
            log.append("Numeric features scaled using Min-Max")

        elif scale_method == "Standardization (Z-score)":
            scaler = StandardScaler()
            df[num_cols] = scaler.fit_transform(df[num_cols])
            log.append("Numeric features standardized using Z-score")

        st.success("Scaling applied")

    st.divider()

    st.subheader("Transformation log")

    if log:
        for i, entry in enumerate(log, start=1):
            st.write(f"{i}. {entry}")
    else:
        st.info("No transformations applied yet")

    return df
