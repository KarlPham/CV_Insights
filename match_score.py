from google import genai
from pydantic import BaseModel
import streamlit as st
from sqlalchemy import text
from datetime import datetime
from skills_suggestion import save_skill_suggestions

# 1. Define schema
class MatchCriteria(BaseModel):
    Technical_Skills_Match: int
    Soft_Skills_Communication: int
    Relevant_Work_Experience: int
    Education_Certifications: int
    Resume_Formatting_Clarity: int
    Overall_Fit_for_Role: int

class MatchScoreOutput(BaseModel):
    match_score: int
    criteria: MatchCriteria
    did_well: list[str]
    not_well: list[str]
    need_improve: list[str]

# 2. Configure Gemini client
client = genai.Client(api_key=st.secrets["google"]["api_key"])

# 3. Gemini structured call
def get_match_score(conn, resume_text, jd_text):
    prompt = f"""
You are an AI resume evaluator. Analyze the resume and job description below.

Your task is to evaluate and return a structured JSON object in the following format:
{{
  "match_score": <int 0-100>,
  "criteria": {{
    "Technical_Skills_Match": <0-25>,
    "Soft_Skills_Communication": <0-20>,
    "Relevant_Work_Experience": <0-25>,
    "Education_Certifications": <0-10>,
    "Resume_Formatting_Clarity": <0-10>,
    "Overall_Fit_for_Role": <0-10>
  }},
  "did_well": [...],
  "not_well": [...],
  "need_improve": [...]
}}

Resume:
{resume_text}

Job Description:
{jd_text}
"""
    # gemini - 2.5 - pro - exp - 03 - 25
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-04-17",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": MatchScoreOutput,
            "temperature": 0.0,
            "top_p": 1.0,
        }
    )

    # 4. Save to session
    st.session_state["match_score_result"] = response.parsed

    user_email = st.session_state.get("user_email")
    user_id_result = conn.query("SELECT user_id FROM users WHERE email = :email", params={"email": user_email}, ttl=0)
    if user_id_result.empty:
        st.error("User not found in DB.")
        return response.parsed

    user_id = int(user_id_result.iloc[0]["user_id"])

    resume_id_result = conn.query(
        "SELECT resume_id FROM resume WHERE user_id = :user_id ORDER BY upload_date DESC LIMIT 1",
        params={"user_id": user_id}, ttl=0)
    jobdesc_id_result = conn.query(
        "SELECT job_desc_id FROM job_description WHERE user_id = :user_id ORDER BY upload_date DESC LIMIT 1",
        params={"user_id": user_id}, ttl=0)

    if resume_id_result.empty or jobdesc_id_result.empty:
        st.error("Resume or Job Description not found in DB.")
        return response.parsed

    resume_id = int(resume_id_result.iloc[0]["resume_id"])
    jd_id = int(jobdesc_id_result.iloc[0]["job_desc_id"])

    # Save result to DB
    with conn.session as session:
        result = session.execute(
            text("""
                INSERT INTO match_scores (
                    user_id, resume_id, job_desc_id, match_score,
                    did_well, not_well, need_focus, create_at
                )
                VALUES (
                    :user_id, :resume_id, :jd_id, :match_score,
                    :did_well, :not_well, :need_improve, :analyze_date
                )
                RETURNING match_id
            """),
            {
                "user_id": user_id,
                "resume_id": resume_id,
                "jd_id": jd_id,
                "match_score": response.parsed.match_score,
                "did_well": "\n".join(response.parsed.did_well),
                "not_well": "\n".join(response.parsed.not_well),
                "need_improve": "\n".join(response.parsed.need_improve),
                "analyze_date": datetime.now()
            }
        )

        # ✅ Fetch BEFORE committing
        match_id_row = result.fetchone()
        match_id = match_id_row[0] if match_id_row else None
        session.commit()
        st.session_state["match_id"] = match_id
        if "skills_suggestions" in st.session_state and "match_id" in st.session_state:
            save_skill_suggestions(conn, st.session_state["match_id"], st.session_state["skills_suggestions"])

    return response.parsed