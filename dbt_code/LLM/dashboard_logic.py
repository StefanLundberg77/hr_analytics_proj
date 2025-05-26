# LLM logic for dashboard

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_soft_skills(text_blob, job_title):
    prompt = f"""
    Analyze this job ad for '{job_title}' 
    and extract the top 5 soft skills.
    Return as JSON in the format:{{"skill": score (0-10)}}.

    {text_blob}
    """
    return model.generate_content(prompt).text