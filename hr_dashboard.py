import streamlit as st
import duckdb as db
import os 
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
from pathlib import Path
from streamlit_option_menu import option_menu
from utilities.read_DB import AdsDB
from visualisation.charts import pie_occupation_grouped, vacancies_per_locality, soft_skills_radar, hard_skills_radar
from dbt_code.LLM.dashboard_queries import get_descriptions_for_field, get_job_titles_by_field, get_description_for_title
from dbt_code.LLM.dashboard_logic import generate_field_average_soft_skills, generate_soft_skills, generate_hard_skills
import json
import re #regex to parse JSON

#db = AdsDB()
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model= genai.GenerativeModel("gemini-2.0-flash")
#GEMINI_API_KEY=AIzaSyAayP2C2dXC8BqPyk0xLSUhpmbGOjlYtpU

# Connecting to the data warehouse
db_path = Path(__file__).parent / "ads_data_warehouse.duckdb"
connection = db.connect(database=str(db_path), read_only=True)

# Function for a dropdown menu to select different charts to see
def chart_dropdown_menu(): # why not st.selectbox instead? easier to use
    selected_charts = st.multiselect(
        label='Charts',
        options=['Pie Chart', 'Spider Chart', 'Bar Chart']
    )

    if 'Pie Chart' in selected_charts:
        st.write("Pie Chart")
        #if selected == "Data/IT":
            # pie_occupation_grouped()
            # db.close() # method for closing

    if 'Spider Chart' in selected_charts:
        st.write("Spider Chart")

    if 'Bar Chart' in selected_charts:
        st.write("Bar Chart")
        #if selected == "Data/IT":
            # run barchart for vacancies by city
            # vacancies_per_locality() 
            # db.close()

# Sidebar for different options
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home", "Säkerhet och bevakning", "Yrken med social inriktning", "Data/IT"],
        icons=["house", "fingerprint", "person-arms-up", "pc-display-horizontal"],
        default_index=0
    )

# Changing "page" based on selected option
if selected == "Home":
    st.title (f"{selected}")
if selected == "Säkerhet och bevakning":
    st.title (f"{selected}")
    chart_dropdown_menu()
if selected == "Yrken med social inriktning":
    st.title (f"{selected}")
    chart_dropdown_menu()
if selected == "Data/IT":
    st.title (f"{selected}")
    chart_dropdown_menu()


# HARD skills radar ui logic
job_titles = get_job_titles_by_field(connection, f"{selected}")
selected_job= st.selectbox("Choose a job: ", [""] + job_titles, key="job_title_select")

if selected_job:
        st.markdown("## ✨Hard Skills Generator✨")
        desc = get_description_for_title(connection, selected_job)
        result= generate_hard_skills(desc, selected_job)
        st.markdown(f"### Top 5 Hard Skills for {selected_job}")

        match = re.search(r"\{[\s\S]*?\}", result, re.DOTALL)
        if match:
            raw_json = match.group()
            skills= json.loads(raw_json)
                #sort 5 skills from most to least important
            sorted_skills=dict(sorted(skills.items(), key=lambda x: x[1], reverse=True))

            for skill, score in sorted_skills.items():
                st.markdown(f"- **{skill}**: {score}/10")
        
        else:
            st.error("Could not parse. Try again.")
            st.code(result) 

# SOFT Skills generator

if selected_job:
        st.markdown("## ✨Soft Skills Generator✨")
        desc = get_description_for_title(connection, selected_job)
        result= generate_soft_skills(desc, selected_job)
        st.markdown(f"### Top 5 Soft Skills for {selected_job}")

        match = re.search(r"\{[\s\S]*?\}", result, re.DOTALL)
        if match:
            raw_json = match.group()
            try:
                skills= json.loads(raw_json)
                #sort 5 skills from most to least important
                sorted_skills=dict(sorted(skills.items(), key=lambda x: x[1], reverse=True))

                for skill, score in sorted_skills.items():
                    st.markdown(f"- **{skill}**: {score}/10")

                # ✅ Button to generate spider chart
                if st.button("Generate Soft Skills Spider Chart"):
                    soft_skills_radar(sorted_skills, selected_job)

            except json.JSONDecodeError as e:
                st.error("JSON parse failed. Model output invalid.")
                st.code(result)
        else:
            st.error("Could not parse. Try again.")
            st.code(result) 
# comment out: cmd /
# 





