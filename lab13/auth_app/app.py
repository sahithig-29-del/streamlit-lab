
import streamlit as st
from db import create_table
from auth import signup, login, reset_password

st.set_page_config(page_title="Login Signup App", page_icon="🔐")

create_table()

st.title("Login / Signup with PostgreSQL")

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user:
    st.success(f"Welcome, {st.session_state.user['username']}!")

    st.write("Role:", st.session_state.user["role"])

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

else:
    choice = st.radio("Choose an option", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            if username.strip() and password:
                success, message = signup(username.strip(), password)
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.warning("Please enter username and password.")

    else:
        if st.button("Login"):
            if username.strip() and password:
                success, result = login(username.strip(), password)

                if success:
                    st.session_state.user = result
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.warning("Please enter username and password.")



st.divider()
st.subheader("Reset Password")

reset_username = st.text_input("Username for password reset")
new_password = st.text_input(
    "New Password",
    type="password",
    key="reset_new_password"
)

if st.button("Reset Password"):
    if reset_username.strip() and new_password:
        success = reset_password(
            reset_username.strip(),
            new_password
        )

        if success:
            st.success("Password reset successful!")
        else:
            st.error("Username not found.")
    else:
        st.warning("Please enter username and new password.")

