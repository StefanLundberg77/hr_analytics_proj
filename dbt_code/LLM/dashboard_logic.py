# LLM logic for dashboard

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_soft_skills(text_blob, job_title):
    prompt = f"""
    Analyze the following job ad for '{job_title}' 
    and extract **the top 5 soft skills** in **valid JSON format**.
    Format strictly like this example:
    {{
    "Skill 1": 7,
    "Skill 2": 6,
    "Skill 3": 9,
    "Skill 4": 5,
    "Skill 5": 8
    }}
    Only return the JSON object.

    {text_blob}
    """
    return model.generate_content(prompt).text