import streamlit as st
import google.generativeai as genai

# Configure Gemini using secrets
genai.configure(api_key=st.secrets["google"]["api_key"])


def get_match_score(resume_text, jd_text):
    """
    Analyze resume and job description to generate match score and review.
    """

    prompt = f"""
You are a professional ATS system and recruiter AI assistant, responsible for evaluating student resumes against job descriptions for internship and graduate IT roles.
Given the following resume and job description, perform the following analysis:

Resume:
{resume_text}

Job Description:
{jd_text}

Your evaluation should be STRICTLY STRUCTURED in the following format and should not include unnecessary text or explanations. The output must be always in this JSON format.


  "total_score": X,
  "criteria_scores": 
    "technical_skills": X,
    "soft_skills": X,
    "work_experience": X,
    "education_certifications": X,
    "formatting_clarity": X,
    "overall_fit": X
  ,
  "did_well": "What the candidate did well",
  "not_well": "What was weak or missing",
  "need_improvement": "Suggestions for improvement"

Where:

- total_score: Calculate out of 100 (sum of all criteria scores).
- technical_skills: Score out of 25 based on relevance and presence of technical skills.
- soft_skills: Score out of 20 based on communication, teamwork, adaptability shown in the resume.
- work_experience: Score out of 20 based on relevance and quality of past projects/work.
- education_certifications: Score out of 15 based on relevant degrees/certifications.
- formatting_clarity: Score out of 10 based on clarity and readability of the resume.
- overall_fit: Score out of 10 based on the general impression and alignment with the job.

Rules:

- Be very strict and fair while scoring.
- Always give constructive feedback for "did_well", "not_well", and "need_improvement".
- NEVER return free text. Return ONLY JSON.
- Be clear, consistent because it very important.

"""

    # Load Gemini model
    model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')

    # Generate the response
    response = model.generate_content(prompt,generation_config=genai.types.GenerationConfig(
        temperature=0.0,
        top_p = 1
    ))

    return response.text