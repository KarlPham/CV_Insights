import streamlit as st
from ai import ask_gemini
from db import get_db_connection

st.title("AI Resume Analyzer")

resume = st.text_area("Paste your Resume")
job_desc = st.text_area("Paste the Job Description")

if st.button("Analyze"):
    prompt = f"Compare this resume to the job: {resume} --- {job_desc}"
    result = ask_gemini(prompt)
    st.write(result)