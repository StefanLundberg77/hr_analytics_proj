import streamlit as st
import duckdb as db
import os 
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
from pathlib import Path
from streamlit_option_menu import option_menu
from utilities.read_DB import AdsDB
from visualisation.charts import pie_occupation_grouped, vacancies_per_locality, soft_skills_radar
from dbt_code.LLM.dashboard_queries import get_job_titles_by_field, get_description_for_title
from dbt_code.LLM.dashboard_logic import generate_soft_skills
import json

#db = AdsDB()
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model= genai.GenerativeModel("gemini-2.0-flash")
#GEMINI_API_KEY=AIzaSyAayP2C2dXC8BqPyk0xLSUhpmbGOjlYtpU

# Connecting to the data warehouse
db_path = Path(__file__).parent / "ads_data_warehouse.duckdb"
connection = db.connect(database=str(db_path), read_only=True)

# Function for a dropdown menu to select different charts to see
def chart_dropdown_menu():
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

# Skills generator
    job_titles = get_job_titles_by_field(connection, f"{selected}")
    selected_job= st.selectbox("Choose a job: ", job_titles)

    if selected_job:
        if st.button("Generate Spider Chart"):
            desc = get_description_for_title(connection, selected_job)
            result= generate_soft_skills(desc, selected_job)
            st.markdown(f"### Top 5 Soft Skills for {selected_job}")

            import re 
            try:
                match= re.search(r"\{[\s\S]*?\}", result)
                if match:
                    skills= json.loads(match.group())
                    st.json(skills)
                    soft_skills_radar(skills, selected_job)
                else:
                    st.error("No valid json found.")
                    st.code(result)
            except Exception as e:
                st.error("Could not parse. Try again.")
                st.code(result)


st.markdown("## Soft Skills Generator")


