import streamlit as st
from upload_resume import upload_resume
from upload_jobdes import upload_job_description
from result import show_result

def home(conn):
    st.header(f"Welcome, {st.session_state.get('user_email')}!")
    st.write("Please upload both Resume and Job Description to continue:")

    # Initialize session state if not exist
    if "resume_uploaded" not in st.session_state:
        st.session_state["resume_uploaded"] = False
    if "jobdesc_uploaded" not in st.session_state:
        st.session_state["jobdesc_uploaded"] = False

    upload_resume(conn)
    upload_job_description(conn)

    if st.session_state["resume_uploaded"] and st.session_state["jobdesc_uploaded"]:
        st.success("✅ All files uploaded successfully!")

    # Logout
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        if st.user.is_logged_in:
            st.logout()
        st.rerun()