
import streamlit as st
import pandas as pd
import numpy as np

st.title("Layouts Demo")

# Sidebar
st.sidebar.header("Settings")
theme = st.sidebar.selectbox("Theme", ["Light", "Dark"])
font_size = st.sidebar.slider("Font Size", 10, 30, 15)

# Columns
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Sales", "25 Lakh")

with col2:
    st.metric("Customers", "1,200")

# Tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Analysis", "About"])

df = pd.DataFrame(
    np.random.randn(10, 2),
    columns=["A", "B"]
)

with tab1:
    st.write("Overview content here")
    st.line_chart(df)

with tab2:
    st.write("Analysis content here")
    st.bar_chart(df)

with tab3:
    st.write("About this app")
    st.line_chart(df)

# Container
with st.container():
    st.write("### Grouped Section")
    st.write("All these elements are inside one container.")

# Exercise 1: Three columns with different widths
st.header("Exercise 1: Three Columns")

c1, c2, c3 = st.columns([1, 2, 1])

with c1:
    st.write("Left (narrow)")

with c2:
    st.write("Center (wide)")

with c3:
    st.write("Right (narrow)")

# Exercise 2: Expander
st.header("Exercise 2: Expander")

with st.expander("Details"):
    st.write("This content is hidden until expanded.")
    st.write("You can put anything here.")

# Exercise 3: Charts inside tabs
# Charts are already added inside all three tabs above.
