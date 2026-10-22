
import streamlit as st
from db import create_table
from auth import signup, login, reset_password

st.set_page_config(
    page_title="Login Signup App",
    page_icon="🔐"
)

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

    if choice == "Signup":
        st.subheader("Create Account")

        username = st.text_input("Username", key="signup_username")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input(
            "Password", type="password", key="signup_password"
        )
        confirm = st.text_input(
            "Confirm Password", type="password", key="signup_confirm"
        )

        if st.button("Create Account"):
            if not username.strip() or not email.strip() or not password or not confirm:
                st.warning("Please fill in all fields.")

            elif "@" not in email or "." not in email.split("@")[-1]:
                st.warning("Please enter a valid email.")

            elif password != confirm:
                st.error("Passwords do not match.")

            else:
                success, message = signup(
                    username.strip(),
                    email.strip(),
                    password
                )

                if success:
                    st.success(message)
                else:
                    st.error(message)

    else:
        st.subheader("Login")

        username = st.text_input("Username", key="login_username")
        password = st.text_input(
            "Password", type="password", key="login_password"
        )

        if st.button("Login"):
            if username.strip() and password:
                success, result = login(username.strip(), password)

                if success:
                    st.session_state.user = result
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.warning("Enter username and password.")

st.divider()
st.subheader("Reset Password")

reset_username = st.text_input(
    "Username for password reset", key="reset_username"
)
reset_email = st.text_input(
    "Registered Email", key="reset_email"
)
new_password = st.text_input(
    "New Password", type="password", key="reset_password"
)
confirm_new_password = st.text_input(
    "Confirm New Password", type="password", key="confirm_reset_password"
)

if st.button("Reset Password"):
    if not reset_username.strip() or not reset_email.strip() or not new_password or not confirm_new_password:
        st.warning("Please fill in all reset fields.")

    elif new_password != confirm_new_password:
        st.error("Passwords do not match.")

    else:
        success = reset_password(
            reset_username.strip(),
            reset_email.strip(),
            new_password
        )

        if success:
            st.success("Password reset successful!")
        else:
            st.error("Username or email not found.")
