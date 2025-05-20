import streamlit as st
from auth.login import login
from auth.register import register
from home import home
from result import show_result
from user_profile import show_user_profile

# Connect to DB
conn = st.connection("postgres")

# Initialize session state
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("resume_uploaded", False)
st.session_state.setdefault("jobdesc_uploaded", False)
st.session_state.setdefault("page", "Upload")

# Logged-in user view
if st.session_state["logged_in"]:
    # Define page options
    PAGES = ["Upload", "Result", "User Profile"]

    # Show sidebar
    st.sidebar.title("CV Insights")
    selected_page = st.sidebar.radio("Select Page", PAGES, index=PAGES.index(st.session_state["page"]))

    # ✅ Only update if changed (prevents unnecessary rerun loop)
    if selected_page != st.session_state["page"]:
        st.session_state["page"] = selected_page
        st.rerun()  # Ensure proper rendering on selection

    # Page Routing
    if selected_page == "Upload":
        home(conn)
    elif selected_page == "Result":
        show_result(conn)
    elif selected_page == "User Profile":
        show_user_profile(conn)


# Guest view: Login/Register
else:
    st.sidebar.title("CV Insights")
    auth_page = st.sidebar.radio("Select Page", ["Login", "Register"])

    if auth_page == "Login":
        login(conn)
    elif auth_page == "Register":
        register(conn)