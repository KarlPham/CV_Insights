import streamlit as st
import os
from datetime import datetime
from sqlalchemy import text
from docx import Document
from PIL import Image
import pytesseract
import pdf2image

def extract_text_from_pdf(file_path):
    images = pdf2image.convert_from_path(file_path)
    text = ""
    for page in images:
        text += pytesseract.image_to_string(page)
    return text

def read_docx(file_path):
    doc = Document(file_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return "\n".join(fullText)

def upload_resume(conn):
    st.subheader(" Upload Resume")
    # if "resume_uploaded" not in st.session_state:
    #     st.session_state["resume_uploaded"] = False

    user_email = st.session_state.get("user_email")
    result = conn.query("SELECT user_id FROM users WHERE email = :email", params={"email": user_email}, ttl=0)

    if result.empty:
        st.error("User not found!")
        return False

    user_id = int(result.iloc[0]["user_id"])
    resume_file = st.file_uploader("Upload your Resume", type=["pdf", "txt", "docx"], key="resume")

    if resume_file is not None:
        save_folder = "uploaded_files/resume"
        os.makedirs(save_folder, exist_ok=True)

        resume_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{resume_file.name}"
        resume_path = os.path.join(save_folder, resume_filename)

        with open(resume_path, "wb") as f:
            f.write(resume_file.getbuffer())

        # Extract text
        if resume_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume_path)
        elif resume_file.name.endswith(".docx"):
            resume_text = read_docx(resume_path)
        else:
            resume_text = resume_file.read().decode("utf-8", errors="ignore")

        # Save into DB
        with conn.session as session:
            session.execute(
                text("INSERT INTO resume (user_id, file_path, upload_date) VALUES (:user_id, :file_path, :upload_date)"),
                {"user_id": user_id, "file_path": resume_path, "upload_date": datetime.now()}
            )
            session.commit()

        # Save resume_text to session_state
        st.session_state["resume_text"] = resume_text
        st.session_state["resume_uploaded"] = True
        st.badge("Success", icon=":material/check:", color="green")


