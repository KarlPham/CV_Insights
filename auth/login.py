import streamlit as st
from sqlalchemy import text
import hashlib
from datetime import datetime
import authlib

def login(conn):
    st.header("Login")

    with st.form("login_form"):

        # Username and password inputs
        email = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Social login buttons - side by side
        col1, col2 = st.columns(2)

        with col1:
            google_login = st.form_submit_button(" Continue with Google", icon=":material/g_mobiledata:")

        # with col2:
        #     microsoft_login = st.form_submit_button("🪟 Continue with Microsoft")

        # Main login button
        login_submit = st.form_submit_button("Login",type="primary")

        # ---------------------------------------
        # Email/Password login logic
        if login_submit:
            if email and password:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                try:
                    result = conn.query(
                        "SELECT * FROM users WHERE email = :email AND password_hash = :password",
                        params={"email": email, "password": hashed_password}, ttl=0
                    )

                    if len(result) > 0:
                        st.success("✅ Login successful!")
                        st.session_state["logged_in"] = True
                        st.session_state["user_email"] = email
                        st.rerun()

                    else:
                        st.error("❌ Invalid email or password.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("Please fill in all fields.")

        # ---------------------------------------
        # Google login logic
        if google_login:
            # Trigger Google login
            if not st.user.is_logged_in:
                st.login()

    if st.user.is_logged_in:
        google_email = st.user.email
        password = "123"
        given_name = st.user.given_name or ""
        family_name = st.user.family_name or ""

        result = conn.query(
            "SELECT * FROM users WHERE email = :email",
            params={"email": google_email},
            ttl=0
        )

        if len(result) == 0:
            # Insert new user
            with conn.session as session:
                session.execute(
                    text(
                        "INSERT INTO users (email, password_hash, first_name, last_name, create_at) VALUES (:email, :password, :first_name, :last_name, :create_at)"
                    ),
                    {"email": google_email, "password": password, "first_name": given_name,
                     "last_name": family_name,
                     "create_at": datetime.now()}
                )
                session.commit()
            st.success("✅ Google account registered and logged in!")
        else:
            st.success("✅ Google account logged in!")

        st.session_state["logged_in"] = True
        st.session_state["user_email"] = google_email
        st.rerun()


