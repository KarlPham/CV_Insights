import streamlit as st

def show_result():
    st.title("Still empty like your life")
    if st.session_state["jobdesc_uploaded"] and st.session_state["resume_uploaded"]:
        st.write(st.session_state["resume_text"])
        st.divider()
        st.write(st.session_state["jd_text"])