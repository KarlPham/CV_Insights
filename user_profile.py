import streamlit as st
from sqlalchemy import text
import os
import pandas as pd

def show_user_profile(conn):
    st.title("👤 User Profile")

    # Session check
    user_email = st.session_state.get("user_email")
    if not user_email:
        st.error("🚫 You must be logged in to view this page.")
        return

    # Fetch user details
    user_result = conn.query(
        "SELECT * FROM users WHERE email = :email",
        params={"email": user_email},
        ttl=0
    )
    if user_result.empty:
        st.error("⚠️ User not found.")
        return
    user = user_result.iloc[0]
    user_id = int(user["user_id"])  # Ensure native int

    st.subheader("👥 Account Information")
    st.markdown(f"- **First Name**: {user['first_name'] or 'N/A'}")
    st.markdown(f"- **Last Name**: {user['last_name'] or 'N/A'}")
    st.markdown(f"- **Email**: {user['email']}")
    st.markdown(f"- **Joined**: {user['create_at'].strftime('%Y-%m-%d')}")

    st.markdown("---")

    # Fetch 3 most recent match score results
    match_result = conn.query("""
        SELECT ms.match_score, ms.create_at,
               r.file_path AS resume_file,
               jd.file_path AS jd_file
        FROM match_scores ms
        JOIN resume r ON ms.resume_id = r.resume_id
        JOIN job_description jd ON ms.job_desc_id = jd.job_desc_id
        WHERE ms.user_id = :user_id
        ORDER BY ms.create_at DESC
        LIMIT 3
    """, params={"user_id": user_id}, ttl=0)

    st.subheader("📊 Latest Resume–JD Match Scores")

    if match_result.empty:
        st.info("No resume–JD match results found.")
        return

    # --- Truncate long filenames ---
    def truncate_filename(filename, max_length=40):
        base = os.path.basename(filename)
        parts = base.split('_', 1)
        name = parts[1] if len(parts) > 1 else base
        return name if len(name) <= max_length else name[:max_length - 3] + "..."

    df = match_result.copy()
    df["Resume File"] = df["resume_file"].apply(truncate_filename)
    df["JD File"] = df["jd_file"].apply(truncate_filename)
    df["Match Score (%)"] = df["match_score"]
    df["Evaluated At"] = pd.to_datetime(df["create_at"]).dt.strftime("%Y-%m-%d %H:%M")

    # --- Reorder columns: show Match Score first ---
    display_df = df[["Match Score (%)", "Resume File", "JD File", "Evaluated At"]].reset_index(drop=True)
    st.dataframe(display_df, use_container_width=True, height=150)
