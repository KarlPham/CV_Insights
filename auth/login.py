import streamlit as st
from sqlalchemy import text
import hashlib

def login(conn):
    st.header("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_submit = st.form_submit_button("Login")

        if login_submit:
            if email and password:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                try:
                    result = conn.query(
                        "SELECT * FROM users WHERE email = :email AND password_hash = :password",
                        params={"email": email, "password": hashed_password}, ttl =0
                    )

                    if len(result) > 0:
                        st.success("✅ Login successful!")
                        st.session_state["logged_in"] = True
                        st.session_state["user_email"] = email
                    else:
                        st.error("❌ Invalid email or password.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("Please fill in all fields.")