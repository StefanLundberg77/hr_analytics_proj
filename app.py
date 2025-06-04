#----Källa----
# URL: https://duckdb.org/docs/stable/clients/python/dbapi
# URL: https://docs.streamlit.io/get-started/fundamentals/main-concepts
# --Hur man ändrar styles ⬇️, exstension emojisense--
# URL: https://github.com/victoryhb/streamlit-option-menu/blob/master/streamlit_option_menu/__init__.py
# --AIgineerAB den föregående python kursen--
# URL: https://github.com/AIgineerAB/Python_OPA24/tree/main/10_plotly_express

import streamlit as st
import duckdb
from pathlib import Path
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd

db_path = Path(__file__).parent / "ads_data_warehouse.duckdb"
connection = duckdb.connect(database=str(db_path), read_only=True)

# --- Anslutning till google Gemini LLM
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# -- Funktion för att skapa KPI:er med Streamlit-kolumner
def show_kpis(df):
    if df.empty:
        st.warning("Ingen data hittades för det valda yrkesområdet!")
    else:
        total_vacancies = df["num_vacancies"].sum()
        top_occupation = df.iloc[0]["occupation"]
        top_municipality = df.iloc[0]["municipality"]

        st.subheader("🚀 Viktiga KPI:er för Talent Acquisition")
        
        cols1 = st.columns(1)
        cols1[0].metric(label="Totalt antal jobb", value=total_vacancies, border=True)
        cols2 = st.columns(1)
        cols2[0].metric(label="Yrket med flest jobb", value=top_occupation, border=True)
        cols3 = st.columns(1)
        cols3[0].metric(label="Kommun med flest jobb", value=top_municipality, border=True)

        # cols = st.columns(3)
        # cols[0].metric(label="Totalt antal jobb", value=total_vacancies, label_visibility="visible", border=True, help=str(df["num_vacancies"].sum()))
        # cols[0].metric(label="Yrket med flest jobb", value=top_occupation, label_visibility="visible", border=True, help=str(df.iloc[0]["occupation"]))
        # cols[0].metric(label="Kommun med flest jobb", value=top_municipality, label_visibility="visible", border=True, help=str(df.iloc[0]["municipality"]))

#-- Funktion för diagram-menyn med Streamlit
def chart_dropdown_menu(df):
    st.subheader("📊 Välj vad du vill visualisera:")
    visualize_option = st.selectbox(
        "Vad vill du visualisera?",
        options=[
            "Antal jobb per kommun",
            "Fördelning av jobb per yrke",
            "Lönetyp",
            "Omfattning"
        ]
    )
    
    plot_df = df
    
    if visualize_option == "Antal jobb per kommun":
        #--Filtrerar efter land
        countries = df['country'].dropna().unique().tolist()
        countries.sort()
        selected_country = st.selectbox("Välj land:", options=["Alla"] + countries)
        
        if selected_country != "Alla":
            df_filtered = df[df['country'] == selected_country]
        else:
            df_filtered = df.copy()
        


            others_sum = others_df['num_vacancies'].sum()
            others_row = {'municipality': 'Övriga', 'num_vacancies': others_sum}
            selected_grouped = selected_df.groupby(['municipality', 'occupation'], as_index=False)['num_vacancies'].sum()
            others_df_grouped = pd.DataFrame([others_row])
            plot_df = pd.concat([selected_grouped, others_df_grouped], ignore_index=True)
        else:
            #--Visar top 10 yrken + övriga om inga yrken är valda
            grouped = df_filtered.groupby(['municipality', 'occupation'], as_index=False)['num_vacancies'].sum()
            top10 = grouped.groupby('municipality')['num_vacancies'].sum().nlargest(10).index
            top10_df = grouped[grouped['municipality'].isin(top10)]
            others_df = grouped[~grouped['municipality'].isin(top10)]
            others_sum = others_df['num_vacancies'].sum()
            others_row = {'municipality': 'Övriga', 'num_vacancies': others_sum}
            others_df_grouped = pd.DataFrame([others_row])
            plot_df = pd.concat([top10_df, others_df_grouped], ignore_index=True)

    elif visualize_option == "Fördelning av jobb per yrke":
        #--Filtrerar efter yrken
        jobs = df['occupation'].dropna().unique().tolist()
        jobs.sort()
        selected_jobs = st.multiselect("Välj yrke/yrken (övriga grupperas)", jobs)
        
        if selected_jobs:
            #--Varje yrke blir grupperat + samlar ihop resten som övrigt
            selected_df = df[df['occupation'].isin(selected_jobs)]
            others_df = df[~df['occupation'].isin(selected_jobs)]
            others_sum = others_df['num_vacancies'].sum()
            others_row = {'occupation': 'Övriga', 'num_vacancies': others_sum}
            selected_grouped = selected_df.groupby(['occupation'], as_index=False)['num_vacancies'].sum()
            others_df_grouped = pd.DataFrame([others_row])
            plot_df = pd.concat([selected_grouped, others_df_grouped], ignore_index=True)
        else:
            #--Visar top 10 yrken + övriga om inga yrken är valda
            grouped = df.groupby(['occupation'], as_index=False)['num_vacancies'].sum()
            top10 = grouped.nlargest(10, 'num_vacancies')['occupation']
            top10_df = grouped[grouped['occupation'].isin(top10)]
            others_df = grouped[~grouped['occupation'].isin(top10)]
            others_sum = others_df['num_vacancies'].sum()
            others_row = {'occupation': 'Övriga', 'num_vacancies': others_sum}
            others_df_grouped = pd.DataFrame([others_row])
            plot_df = pd.concat([top10_df, others_df_grouped], ignore_index=True)

    elif visualize_option == "Lönetyp":
        plot_df = df.groupby(['salary_type'], as_index=False)['num_vacancies'].sum()
    elif visualize_option == "Omfattning":
        plot_df = df.groupby(['working_hours_type'], as_index=False)['num_vacancies'].sum()
    
    #--Val för vilka charts man vill se
    st.subheader("📊 Välj diagramtyp:")
    selected_charts = st.multiselect(
        label="Diagramtyper",
        options=["Donut Chart", "Bar Chart", "Scatter Plot"],
        default=["Donut Chart"]
    )
    
    #--Donut chart visas om vald
    if "Donut Chart" in selected_charts:
        if visualize_option == "Antal jobb per kommun":
            fig = px.pie(plot_df, names="municipality", values="num_vacancies", title="Jobb per kommun", hole=0.4)
        elif visualize_option == "Fördelning av jobb per yrke":
            fig = px.pie(plot_df, names="occupation", values="num_vacancies", title="Jobb per yrke", hole=0.4)
        elif visualize_option == "Lönetyp":
            fig = px.pie(plot_df, names="salary_type", values="num_vacancies", title="Lönetyp", hole=0.4)
        elif visualize_option == "Omfattning":
            fig = px.pie(plot_df, names="working_hours_type", values="num_vacancies", title="Omfattning", hole=0.4)
        st.plotly_chart(fig)

    #--Bar chart visas om vald
    if "Bar Chart" in selected_charts:
        if visualize_option == "Antal jobb per kommun":
            fig = px.bar(plot_df, x="municipality", y="num_vacancies", color="occupation", title="Jobb per kommun", 
                    labels={"municipality": "Kommun", "num_vacancies": "Antal lediga tjänster"},
                    hover_name='occupation',
                    hover_data={"occupation": False, "municipality":True, "num_vacancies": True},
                    text_auto=True)
            
        elif visualize_option == "Fördelning av jobb per yrke":
            fig = px.bar(plot_df, x="occupation", y="num_vacancies", color="occupation", title="Jobb per yrke",
                    labels={"occupation": "Beteckning", "num_vacancies": "Antal lediga tjänster"},
                    hover_name='occupation',
                    hover_data={"occupation": False, "num_vacancies": True},
                    text_auto=True)

        elif visualize_option == "Lönetyp":
            fig = px.bar(plot_df, x="salary_type", y="num_vacancies", color="salary_type", title="Lönetyp",
                    labels={"salary_type": "Lönetyp", "num_vacancies": "Antal lediga tjänster"},
                    hover_name='salary_type',
                    hover_data={"salary_type": False, "num_vacancies": True},
                    text_auto=True)
            
        elif visualize_option == "Omfattning":
            fig = px.bar(plot_df, x="working_hours_type", y="num_vacancies", color="working_hours_type", title="Omfattning",
                    labels={"working_hours_type": "Beteckning", "num_vacancies": "Antal lediga tjänster"},
                    hover_name='working_hours_type',
                    hover_data={"working_hours_type": False, "num_vacancies": True},
                    text_auto=True)
        st.plotly_chart(fig)

# -- Scatterplot visas om vald
    if "Scatter Plot" in selected_charts:
        if visualize_option == "Antal jobb per kommun":
            fig = px.scatter(plot_df, x="municipality", y="num_vacancies", color="occupation", size="num_vacancies",
                        title=" Jobb per kommun  Scatterplot")
        elif visualize_option == "Fördelning av jobb per yrke":
            fig = px.scatter(plot_df, x="occupation", y="num_vacancies", color="occupation", size="num_vacancies",
                        title=" Yrkesfördelning  Scatterplot")
        elif visualize_option == "Lönetyp":
            fig = px.scatter(plot_df, x="salary_type", y="num_vacancies", color="salary_type", size="num_vacancies",
                        title=" Lönetyp  Scatterplot")
        elif visualize_option == "Omfattning":
            fig = px.scatter(plot_df, x="working_hours_type", y="num_vacancies", color="working_hours_type", size="num_vacancies",
                        title=" Omfattning  Scatterplot")
        st.plotly_chart(fig)
    #--Uppdaterar layout och hover-effekter
        fig.update_layout(dragmode="zoom", hovermode="closest")
        fig.update_traces(marker=dict(line=dict(width=1)))


# -- Sidomeny med option_menu, marinblå färg
with st.sidebar:
    selected = option_menu(
        menu_title="🔍 Välj bransch",
        options=["Home", "Säkerhet och bevakning", "Yrken med social inriktning", "Data/IT"],
        icons=["house", "shield-lock", "people", "pc-display-horizontal"],
        menu_icon="chat-left-text",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "icon": {"color": "#002147", "font-size": "20px"},  # marinblå ikon
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px",
                "color": "black"
            },
            "nav-link-selected": {
                "background-color": "#002147", 
                "color": "white"
            },
        }
    )

st.write(f"Du valde: {selected}")
# Initial front page with company name and slogan
st.markdown("# HiRe\u2122 Talangverktyg") #python unicode for 'TM' emoji
st.markdown("### \U0001F50D Sök") #unicode looking glass emoji
st.markdown("### \U0001F4CA Visualisera") # unicode bar chart emoji
st.markdown("### \u2705 Matcha") # unicode check mark emoji
st.markdown("### - Rätt Kandidat till Rätt Jobb")

if selected != "Home":
    # SQL-fråga
    query = f"""
    SELECT occupation, COUNT(*) AS num_vacancies, municipality, country, occupation_field, salary_type, working_hours_type
    FROM (
        SELECT occupation, municipality, country, salary_type, working_hours_type, 'Data/IT' AS occupation_field FROM mart.occupation_data_it
        UNION ALL
        SELECT occupation, municipality, country, salary_type, working_hours_type, 'Säkerhet och bevakning' AS occupation_field FROM mart.occupation_sakerhet_bevakning
        UNION ALL
        SELECT occupation, municipality, country, salary_type, working_hours_type, 'Yrken med social inriktning' AS occupation_field FROM mart.occupation_socialt_arbete
    ) AS combined_data
    WHERE lower(occupation_field) = lower('{selected}')
    GROUP BY occupation, municipality, country, occupation_field, salary_type, working_hours_type
    ORDER BY num_vacancies DESC;
    """

    df = connection.execute(query).fetchdf()

    st.title(f"{selected} 🌍")
    show_kpis(df)
    chart_dropdown_menu(df)

#----- Spider/Radar Chart sektion under visualiseringar ----

if selected != "Home":
    st.markdown("## Analysera kompetenser \U0001F9E0 ") # Python Unicode for brain emoji
    st.markdown(get_ai_intro())

    dashboard_field = selected

# Job selector based on occupation field selected from side bar
    job_titles = get_job_titles_by_field(connection, dashboard_field)
    selected_job = st.selectbox(label="",
                                options=["Välj ett yrke att analysera:"] + job_titles,
                                index=0
                                )

# Skill generation
    if selected_job != "Välj ett yrke att analysera:":
        desc = get_description_for_title(connection, selected_job)
        employer_name = get_employer_name_for_title(connection, selected_job, dashboard_field)
    
        st.subheader(f"{employer_name} söker en {selected_job}")
        
        #Gemini summary based on hard skills from selected job
        personality_summary = generate_hard_skills_summary(employer_name, selected_job, desc)
        st.markdown(f" {personality_summary}")
        st.markdown(f"#### Topp 5 Färdigheter (Hard Skills) för rollen som {selected_job} ")

        hard_result = generate_hard_skills(desc, selected_job)
        hard_json = re.search(r"\{[\s\S]*?\}", hard_result, re.DOTALL)
        if hard_json:
            hard_skills = json.loads(hard_json.group())
            for skill, score in hard_skills.items():
                st.markdown(f"- **{skill}**: {score}/10")
        
        st.markdown("#### Mjuka värden (Soft Skills)")
        st.markdown(get_ai_soft_skills())

        soft_result = generate_soft_skills(desc, selected_job)
        soft_json = re.search(r"\{[\s\S]*?\}", soft_result, re.DOTALL)
        if soft_json:
            soft_skills = json.loads(soft_json.group())
            cleaned_soft = clean_skill_labels(soft_skills)
            for skill, score in cleaned_soft.items():
                st.markdown(f"- **{skill}**: {score}/10")

        st.markdown(get_ai_soft_skills_summary(selected_job))

    # --- Button to trigger spider chart ---
        if st.button("Visa i Spider Chart"):
            field_blob = get_descriptions_for_field(connection, dashboard_field)
            field_result = generate_field_average_soft_skills(field_blob, dashboard_field)
            match_field = re.search(r"\{[\s\S]*?\}", field_result, re.DOTALL)

            if match_field:
                field_skills = json.loads(match_field.group())
                cleaned_field_skills = clean_skill_labels(field_skills)
                soft_skills_radar(
                    job_skills=cleaned_soft,
                    field_skills=cleaned_field_skills,
                    title=selected_job
                )
            else:
                st.error("Kunde inte skapa fältgenomsnitt.")

connection.close()