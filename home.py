import streamlit as st
from upload_resume import upload_resume
from upload_jobdes import upload_job_description
from result import show_result

def home(conn):
    st.header(f"Welcome, {st.session_state.get('user_email')}!")
    st.write("Please upload both Resume and Job Description to continue:")

    if "match_score_result" in st.session_state:
        del st.session_state["match_score_result"]
    if "skills_suggestions" in st.session_state:
        del st.session_state["skills_suggestions"]
    if "interview_questions" in st.session_state:
        del st.session_state["interview_questions"]

    if "resume_uploaded" not in st.session_state and "jobdecs_uploaded" not in st.session_state:
        st.session_state.setdefault("resume_uploaded", False)
        st.session_state.setdefault("jobdesc_uploaded", False)

    # Upload components
    upload_resume(conn)
    upload_job_description(conn)

    # If either file was newly uploaded, rerun to reflect changes
    # if resume_uploaded_now or jd_uploaded_now:
    #     st.rerun()

    # Check if both uploaded
    if st.session_state["resume_uploaded"] and st.session_state["jobdesc_uploaded"]:
        st.success("✅ All files uploaded successfully!")
        st.session_state["resume_uploaded"] = False
        st.session_state["jobdesc_uploaded"] = False
        # st.balloons()

        # Redirect to Result page
        st.session_state["page"] = "Result"
        st.rerun()