import streamlit as st
from sqlalchemy import text
import hashlib
from datetime import datetime

def register(conn):
    st.header("Register")

    with st.form("register_form"):
        email = st.text_input("Username")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        register_submit = st.form_submit_button("Register")

        if register_submit:

            # Check all fields filled
            if not (email and first_name and last_name and password and confirm_password):
                st.warning("❗ Please fill in all fields.")
                return

            # Check password match
            if password != confirm_password:
                st.error("❌ Passwords do not match.")
                return

            # Hash password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Check if email already exists
            try:
                result = conn.query("SELECT * FROM users WHERE email = :email", params={"email": email}, ttl =0)
                if not result.empty:
                    st.warning("❗ Username already exists.")
                    return
                else:
                    # Insert new user
                    with conn.session as session:
                        session.execute(
                            text("""
                                INSERT INTO users (email, password_hash, first_name, last_name, create_at)
                                VALUES (:email, :password, :first_name, :last_name, :create_at)
                            """),
                            {
                                "email": email,
                                "password": hashed_password,
                                "first_name": first_name,
                                "last_name": last_name,
                                "create_at": datetime.now()
                            }
                        )
                        session.commit()
                    st.success("✅ Registration successful!")
            except Exception as e:
                st.error(f"❌ Error: {e}")