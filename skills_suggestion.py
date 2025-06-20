from pydantic import BaseModel
from google import genai
import streamlit as st
from datetime import datetime
from sqlalchemy import text

class SkillSuggestionsOutput(BaseModel):
    tech_skills: list[str]
    soft_skills: list[str]
    work_exp: list[str]

client = genai.Client(api_key=st.secrets["google"]["api_key"])

def get_skill_suggestions(conn, resume_text, jd_text):
        if not resume_text.strip() or not jd_text.strip():
            return None
        prompt = f"""    
You are an expert career advisor and IT recruiter evaluating student resumes for job readiness.

Your task is to analyze the resume against the job description and identify **gaps or weak areas** that reduce the candidate's match for the role. Focus on three categories:
- **Technical Skills** – tools, languages, frameworks, or platforms that are missing or not well-demonstrated.
- **Soft Skills** – interpersonal or professional qualities that are lacking or unclear.
- **Work Experience in Australia** – mention if local experience, internships, or projects are missing or weak.

Return the result as a structured JSON object **exactly** in this format:
  "tech_skills": ["skill1", "skill2"],
  "soft_skills": ["skill3", "skill4"],
  "work_exp": ["experience1", "experience2"]

Do NOT describe what the resume already contains.

Instead, focus ONLY on **missing or underrepresented items** based on the job description expectations.

Resume:
{resume_text}

Job Description:
{jd_text}
    """
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": SkillSuggestionsOutput,
                "temperature": 0.3
            }
        )
        result = response.parsed
        st.session_state["skills_suggestions"] = response.parsed
        match_id = st.session_state.get("match_id")
        if match_id:
            save_skill_suggestions(conn, match_id, result)
        return result


def save_skill_suggestions(conn, match_id: int, result):
    with conn.session as session:
        session.execute(
            text("""
                INSERT INTO suggestion (
                    match_id, tech_skills, soft_skills, work_exp, create_at
                ) VALUES (
                    :match_id, :tech_skills, :soft_skills, :work_exp, :create_at
                )
            """),
            {
                "match_id": match_id,
                "tech_skills": "\n".join(result.tech_skills),
                "soft_skills": "\n".join(result.soft_skills),
                "work_exp": "\n".join(result.work_exp),
                "create_at": datetime.now()
            }
        )
        session.commit()

