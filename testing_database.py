import streamlit as st
from sqlalchemy import text

# Connect to database
conn = st.connection("postgres", type="sql")

st.title("🧪 Database CRUD Test - test_users Table")

# ------------------------------
# Create (Insert)
# ------------------------------
st.header("Add User (CREATE)")

with st.form("Insert User"):
    email = st.text_input("Email")
    name = st.text_input("Name")
    submitted = st.form_submit_button("Add User")

    if submitted and email and name:
        with conn.session as session:
            session.execute(
                text("INSERT INTO test_users (email, name) VALUES (:email, :name);"),
                {"email": email, "name": name}
            )
            session.commit()
            st.success("✅ User added successfully!")

            # Check inserted user
            result = conn.query("SELECT * FROM test_users;", ttl=0)
            st.dataframe(result)

# ------------------------------
# Read (Select)
# ------------------------------
st.header("View Users (READ)")

if st.button("Show All Users"):
    result = conn.query("SELECT * FROM test_users;", ttl=0)
    st.dataframe(result)

st.header("Test currentdatebase")

if st.button("Show"):
    result = conn.query("SELECT current_database();", ttl=0)
    st.dataframe(result)


# ------------------------------
# Update
# ------------------------------
st.header("Update User (UPDATE)")

with st.form("Update User"):
    email_to_update = st.text_input("Email of User to Update")
    new_name = st.text_input("New Name")
    update_btn = st.form_submit_button("Update User")

    if update_btn and email_to_update and new_name:
        with conn.session as session:
            session.execute(
            text("UPDATE test_users SET name = :new_name WHERE email = :email_to_update;"),
            {"new_name": new_name, "email_to_update": email_to_update}
            )
            session.commit()
            st.success("✅ User updated successfully!")

# ------------------------------
# Delete
# ------------------------------
st.header("Delete User (DELETE)")

with st.form("Delete User"):
    email_to_delete = st.text_input("Email of User to Delete")
    delete_btn = st.form_submit_button("Delete User")

    if delete_btn and email_to_delete:
        with conn.session as session:
            session.execute(
            text("DELETE FROM test_users WHERE email = :email_to_delete;"),
            {"email_to_delete": email_to_delete}
            )
            session.commit()
            st.success("✅ User deleted successfully!")