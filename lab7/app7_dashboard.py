
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("Sales Dashboard")

# Fake data
df = pd.DataFrame({
    "Year": np.random.choice([2022, 2023, 2024], 200),
    "Region": np.random.choice(["North", "South", "East", "West"], 200),
    "Product": np.random.choice(["A", "B", "C"], 200),
    "Sales": np.random.randint(1000, 10000, 200)
})

# Exercise 3: Add a date column
df["Date"] = pd.to_datetime(
    np.random.choice(pd.date_range("2022-01-01", "2024-12-31"), 200)
)

# Sidebar filters
st.sidebar.header("Filters")

year = st.sidebar.multiselect(
    "Year",
    df["Year"].unique(),
    default=df["Year"].unique()
)

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

product = st.sidebar.multiselect(
    "Product",
    df["Product"].unique(),
    default=df["Product"].unique()
)

# Date range filter
start_date = st.sidebar.date_input("Start date", df["Date"].min().date())
end_date = st.sidebar.date_input("End date", df["Date"].max().date())

filtered = df[
    (df["Year"].isin(year)) &
    (df["Region"].isin(region)) &
    (df["Product"].isin(product)) &
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date)
]

# KPIs
c1, c2, c3 = st.columns(3)

c1.metric("Total Sales", f"{filtered['Sales'].sum():,}")
c2.metric(
    "Avg Sales",
    f"{filtered['Sales'].mean():,.0f}" if not filtered.empty else "0"
)
c3.metric("Records", len(filtered))

# Charts
st.subheader("Sales by Region")
st.bar_chart(filtered.groupby("Region")["Sales"].sum())

st.subheader("Sales by Year")
st.line_chart(filtered.groupby("Year")["Sales"].sum())

# Exercise 1: Pie chart of sales by product
st.subheader("Sales by Product")

pie_data = filtered.groupby("Product")["Sales"].sum().reset_index()

if not pie_data.empty:
    fig = px.pie(
        pie_data,
        names="Product",
        values="Sales",
        title="Sales by Product"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data available for the selected filters.")

# Exercise 2: Download filtered CSV
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered CSV",
    csv,
    "filtered_sales.csv",
    "text/csv"
)

st.subheader("Filtered Data")
st.dataframe(filtered)
