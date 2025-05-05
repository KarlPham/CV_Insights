import streamlit as st
from auth.login import login
from auth.register import register
from home import home  # Create this module to handle Home Page (simple page first)

# Connect to DB
conn = st.connection("postgres")

# Check if user logged in already
if st.session_state.get("logged_in"):
    home()
else:
    # Sidebar
    st.sidebar.title("CV Insights")
    page = st.sidebar.radio("Select Page", ["Login", "Register"])

    if page == "Login":
        login(conn)

    elif page == "Register":
        register(conn)