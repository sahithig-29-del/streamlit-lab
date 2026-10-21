
import streamlit as st

st.set_page_config(
    page_title="Hello App",
    page_icon="H",
    layout="wide"
)

st.title("Hello Streamlit!")
st.header("Welcome to Streamlit")
st.subheader("This is a basic Streamlit application")

st.write("Streamlit makes it easy to create web applications using Python.")

name = st.text_input("Enter your name")
if name:
    st.write(f"Hello, {name}!")

age = st.number_input("Enter your age", min_value=0, max_value=100)

if st.button("Submit"):
    st.write("Your name is:", name)
    st.write("Your age is:", age)

st.divider()

st.subheader("Python Code Example")

st.code("""
def greet(name):
    return f"Hello, {name}!"
""", language="python")
