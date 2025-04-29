import streamlit as st


conn = st.connection('postgres', type='sql')


def test_connection():
    try:
        result = conn.query("SELECT * FROM users;", ttl=0)
        return result
    except Exception as e:
        st.error(f"❌ Failed to connect to database: {e}")
        return None


st.title("🔌 Test PostgreSQL Connection")

if st.button("Test Connection"):
    test_result = test_connection()
    if test_result is not None:
        st.success("✅ Successfully connected to database!")
        st.write(test_result)
    else:
        st.error("❌ Connection failed. Please check your settings.")