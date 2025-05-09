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

def upload_job_description(conn):
    st.subheader("📝 Upload Job Description")

    # if "jobdesc_uploaded" not in st.session_state:
    #     st.session_state["jobdesc_uploaded"] = False

    user_email = st.session_state.get("user_email")
    result = conn.query("SELECT user_id FROM users WHERE email = :email", params={"email": user_email}, ttl=0)

    if result.empty:
        st.error("User not found!")
        return False

    user_id = int(result.iloc[0]["user_id"])
    jd_file = st.file_uploader("Upload your Job Description", type=["pdf", "txt", "docx"], key="jd")

    if jd_file is not None:
        save_folder = "uploaded_files/jobdesc"
        os.makedirs(save_folder, exist_ok=True)

        jd_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{jd_file.name}"
        jd_path = os.path.join(save_folder, jd_filename)

        with open(jd_path, "wb") as f:
            f.write(jd_file.getbuffer())

        # Extract text
        if jd_file.name.endswith(".pdf"):
            jd_text = extract_text_from_pdf(jd_path)
        elif jd_file.name.endswith(".docx"):
            jd_text = read_docx(jd_path)
        else:
            jd_text = jd_file.read().decode("utf-8", errors="ignore")

        # Save into DB
        with conn.session as session:
            session.execute(
                text("INSERT INTO job_description (user_id, file_path, description_text, upload_date) VALUES (:user_id, :file_path, :description_text, :upload_date)"),
                {"user_id": user_id, "file_path": jd_path, "description_text": jd_text, "upload_date": datetime.now()}
            )
            session.commit()

        # Save jd_text to session_state
        st.session_state["jd_text"] = jd_text
        st.session_state["jobdesc_uploaded"] = True
        st.success("✅ Job Description uploaded and saved!")


