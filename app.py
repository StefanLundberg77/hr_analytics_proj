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
import seaborn as sns

db_path = Path(__file__).parent / "ads_data_warehouse.duckdb"
connection = duckdb.connect(database=str(db_path), read_only=True)

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
        

        #--Filtrerar efter kommun
        kommuner = df_filtered['municipality'].dropna().unique().tolist()
        kommuner.sort()
        selected_kommuner = st.multiselect("Välj kommun(er) att visa separat (övriga grupperas)", kommuner)
        
        if selected_kommuner:
            #--Varje yrke blir grupperat + samlar ihop resten som övrigt
            selected_df = df_filtered[df_filtered['municipality'].isin(selected_kommuner)]
            others_df = df_filtered[~df_filtered['municipality'].isin(selected_kommuner)]
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
            fig = px.bar(plot_df, x="municipality", y="num_vacancies", color="occupation", title="Jobb per kommun")
        elif visualize_option == "Fördelning av jobb per yrke":
            fig = px.bar(plot_df, x="occupation", y="num_vacancies", title="Jobb per yrke")
        elif visualize_option == "Lönetyp":
            fig = px.bar(plot_df, x="salary_type", y="num_vacancies", title="Lönetyp")
        elif visualize_option == "Omfattning":
            fig = px.bar(plot_df, x="working_hours_type", y="num_vacancies", title="Omfattning")
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

connection.close()