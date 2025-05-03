import streamlit as st
from auth.login import login
from auth.register import register

# Connect to DB
conn = st.connection("postgres")

st.sidebar.title("CV Insights")
page = st.sidebar.radio("Select Page", ["Login", "Register"])

if page == "Login":
    login(conn)

elif page == "Register":
    register(conn)