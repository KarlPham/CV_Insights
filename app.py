import streamlit as st
from auth.login import login
from auth.register import register
from home import home
from result import show_result

# Connect to DB
conn = st.connection("postgres")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "resume_uploaded" not in st.session_state:
    st.session_state["resume_uploaded"] = False

if "jobdesc_uploaded" not in st.session_state:
    st.session_state["jobdesc_uploaded"] = False

if "page" not in st.session_state:
    st.session_state["page"] = "Upload"

# If user is logged in, show Home or Result
if st.session_state.get("logged_in"):

    # Sidebar navigation for Home
    st.sidebar.title("CV Insights")
    page = st.sidebar.radio("Select Page", ["Upload", "Result"])

    if page != st.session_state["page"]:
        st.session_state["page"] = page

    # Upload page
    if st.session_state["page"] == "Upload":
        home(conn)

    # Result page
    elif st.session_state["page"] == "Result":
        show_result(conn)

else:
    # Sidebar for login/register
    st.sidebar.title("CV Insights")
    page = st.sidebar.radio("Select Page", ["Login", "Register"])

    if page == "Login":
        login(conn)

    elif page == "Register":
        register(conn)