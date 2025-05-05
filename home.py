import streamlit as st

def home():
    st.header("🏠 Home Page")
    st.write(f"Welcome, {st.session_state.get('user_email')}!")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        if st.user.is_logged_in:
            st.logout()
        st.rerun()