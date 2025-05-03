import pandas as pd
import streamlit as st
from datetime import datetime
import authlib

st.title("Streamlit OAuth Playground")

if not st.experimental_user.is_logged_in:
    if st.button("Log in with Google", type="primary", icon=":material/login:"):
        st.login()
else:
    # Display user name
    st.html(f"Hello, <span style='color: orange; font-weight: bold;'>{st.experimental_user.name}</span>!")

    # Documentation for each key
    st.write(st.user.email)

    if st.button("Log out", type="secondary", icon=":material/logout:"):
        st.logout()

st.caption(f"Streamlit version {st.__version__}")
st.caption(f"Authlib version {authlib.__version__}")