import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def ask_gemini(prompt):
    model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
    response = model.generate_content(prompt)
    return response.text