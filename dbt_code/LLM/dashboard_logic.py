# LLM logic for dashboard

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

#Soft SKills
# Prompt logic to generate top 5 SOFT skills from google gemini LLM
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

#HARD Skills
# Prompt logic to generate top 5 HARD skills from google gemini LLM
def generate_hard_skills(text_blob, job_title):
    prompt = f"""
    Analyze the following job ad for the role of '{job_title}'.
    Identify the **top 5 hard skills** that the ideal candidate should have.
    These are **technical or task-specific** skills (not soft skills like communication or teamwork).

    Return your answer in **JSON format**, like this:
    {{
    "Skill A": 9,
    "Skill B": 8,
    "Skill C": 6,
    "Skill D": 6,
    "Skill E": 5
    }}

    Only include skills that are clearly mentioned or strongly implied in the description.
    Score each skill from 1 to 10 based on importance.

    Job Description:
    {text_blob}
    """
    return model.generate_content(prompt).text

# Field average prompt logic
def generate_field_average_soft_skills(text_blob, field):
    prompt = f"""
    Analyze these job descriptions for the occupational field '{field}'.
    Return the **top 5 soft skills** most frequently emphasized across all roles. 
    Format the output as valid JSON like this example:
    {{
    "Skill 1": 7,
    "Skill 2": 6,
    "Skill 3": 9,
    "Skill 4": 5,
    "Skill 5": 8
    }}
    
    Job Descriptions:
    {text_blob}
    """
    return model.generate_content(prompt).text