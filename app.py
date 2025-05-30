
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
        
        cols = st.columns(3)
        cols[0].metric(label="Totalt antal jobb", value=total_vacancies)
        cols[1].metric(label="Yrket med flest jobb", value=top_occupation)
        cols[2].metric(label="Kommun med flest jobb", value=top_municipality)

# -- Funktion för diagram-menyn med Streamlit
def chart_dropdown_menu(df):
    st.subheader("📊 Välj diagramtyp:")
    selected_charts = st.multiselect(
        label="Diagramtyper",
        options=["Donut Chart", "Bar Chart"],
        default=["Donut Chart"]
    )

    if "Donut Chart" in selected_charts:
        fig = px.pie(df, names="occupation", values="num_vacancies", title="Fördelning av jobb per yrke", hole=0.4)
        st.plotly_chart(fig)

    if "Bar Chart" in selected_charts:
        fig = px.bar(df, x="municipality", y="num_vacancies", title="Antal jobb per kommun", color="occupation")
        st.plotly_chart(fig)

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
# -- SQL-query baserad på vald bransch
if selected != "Home":
    query = f"""
    SELECT occupation, COUNT(*) AS num_vacancies, municipality, occupation_field
    FROM (
        SELECT occupation, municipality, 'Data/IT' AS occupation_field FROM mart.occupation_data_it
        UNION ALL
        SELECT occupation, municipality, 'Säkerhet och Bevakning' AS occupation_field FROM mart.occupation_sakerhet_bevakning
        UNION ALL
        SELECT occupation, municipality, 'Yrken med Social Inriktning' AS occupation_field FROM mart.occupation_socialt_arbete
    ) AS combined_data
    WHERE lower(occupation_field) = '{selected.lower()}'
    GROUP BY occupation, municipality, occupation_field
    ORDER BY num_vacancies DESC;
    """
    
    df = connection.execute(query).fetchdf()
    
    # -- Visa KPI:er och diagram
    st.title(f"{selected} 🌍")
    show_kpis(df)
    chart_dropdown_menu(df)

connection.close()