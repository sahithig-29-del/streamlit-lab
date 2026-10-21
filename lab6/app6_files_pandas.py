
import streamlit as st
import pandas as pd

st.title("Upload CSV and Analyze")

file = st.file_uploader("Upload a CSV file", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.subheader("Data Preview")
    st.dataframe(df)

    st.subheader("Statistics")
    st.write(df.describe())

    st.subheader("Filter by Column")
    col = st.selectbox("Choose column", df.columns)
    value = st.text_input("Filter value")

    if value:
        filtered = df[
            df[col].astype(str).str.contains(value, case=False, na=False)
        ]
        st.dataframe(filtered)

    # Exercise 1: Display the number of rows and columns
    st.subheader("Dataset Information")
    st.write("Number of rows:", df.shape[0])
    st.write("Number of columns:", df.shape[1])

    # Exercise 2: Sort the data
    st.subheader("Sort Data")
    sort_col = st.selectbox("Choose column to sort", df.columns)
    ascending = st.checkbox("Sort ascending", value=True)
    st.dataframe(df.sort_values(by=sort_col, ascending=ascending))

    # Exercise 3: Select columns to display
    st.subheader("Select Columns")
    selected_cols = st.multiselect(
        "Choose columns to display",
        df.columns.tolist(),
        default=df.columns.tolist()
    )

    if selected_cols:
        st.dataframe(df[selected_cols])
