from pydantic import BaseModel
from google import genai
import streamlit as st
from datetime import datetime
from sqlalchemy import text

# Define schema for LLM response
class InterviewQuestionsOutput(BaseModel):
    tech_questions: list[str]
    behav_questions: list[str]

# Gemini client
client = genai.Client(api_key=st.secrets["google"]["api_key"])

# Prompt template
def generate_interview_prompt(resume_text, jd_text):
    return f"""
You are a senior IT recruiter preparing a university student for an internship or graduate job interview.

Based on the resume and job description below, generate two types of interview questions in JSON:

- "tech_questions": a list of 3–5 thoughtful technical questions
- "behav_questions": a list of 3–5 thoughtful behavioral questions

Return a JSON object exactly like this:
{{
  "tech_questions": ["..."],
  "behav_questions": ["..."]
}}

Resume:
{resume_text}

Job Description:
{jd_text}
"""

# Core function to generate and optionally save questions
def generate_and_save_interview_questions(conn, resume_text, jd_text, match_id):
    prompt = generate_interview_prompt(resume_text, jd_text)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": InterviewQuestionsOutput,
                "temperature": 0.3
            }
        )

        result: InterviewQuestionsOutput = response.parsed

        # Save to database
        if match_id and result:
            save_interview_questions(conn, match_id, result)

        return result

    except Exception as e:
        st.error(f"❌ Failed to generate interview questions: {e}")
        return InterviewQuestionsOutput(tech_questions=[], behav_questions=[])

# DB insertion function
def save_interview_questions(conn, match_id: int, result: InterviewQuestionsOutput):
    with conn.session as session:
        session.execute(
            text("""
                INSERT INTO interview_question (
                    match_id, tech_questions, behav_questions, create_at
                ) VALUES (
                    :match_id, :tech_questions, :behav_questions, :create_at
                )
            """),
            {
                "match_id": match_id,
                "tech_questions": "\n".join(result.tech_questions),
                "behav_questions": "\n".join(result.behav_questions),
                "create_at": datetime.now()
            }
        )
        session.commit()
