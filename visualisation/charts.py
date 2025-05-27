# For
# instance, try to produce visualizations to answer these questions:
# for a specific occupation field (i.e. Data/IT), which occupation (i.e. data engineer) has a higher
# number of vacanies?
# which cities has a higher number of vacancies?
# etc
# You should include at least four meaningful KPI/metrics and visualizations on your dashboard that are able
# to improve efficiency of the work of talent acquisition specialists in this HR agency.

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly_express as px
import plotly.graph_objects as go
from utilities.read_DB import AdsDB
import numpy as np

# init db connection
db = AdsDB()


# Pie-chart function for top 10 number of vacancies/occupational role
def pie_occupation_grouped(df, top_n=10):

    
    # sort df and select top 10
    df_top = df.sort_values(by="antal",
                            ascending=False).head(top_n)


    fig = px.pie(df_top, names="beteckning",
                         values="antal",
                         labels={"beteckning":"Beteckning", "antal":"Antal lediga tjänster"},
                         title="Topp 10 lediga tjänster per yrkesbeteckning")

    fig.update_traces(
    textinfo='percent',
    hoverinfo='label+percent+value',
    textposition='inside')
    st.plotly_chart(fig, use_container_width=True)


# WTH hur många ads finns de??
# SKA MAN HA EN KPIS MED MASSA BRA GRUNDDATA?

def vacancies_per_locality():

    # create Dataframe from query
    df = db.query("""SELECT
                  SUM(vacancies) as sum,
                  occupation_field as field,
                  workplace_city as locality
                  FROM marts.mart_data_it
                  GROUP BY locality, field
                  ORDER BY sum DESC
                  """)
    # header for chart
    st.subheader("Antal lediga tjänster per ort")

    # checkbox for missing city data
    missing_city_data = st.checkbox("Inkludera annonser där 'Stad ej angiven'", value=False) 

    # check user input
    if not missing_city_data:
        df = df[df["locality"] != "stad ej angiven"]
    
    # Sort values after top top 10
    df_top = df.sort_values(by="sum",
                            ascending=False).head(10)

    # create figure
    fig = px.bar(df_top, 
                 x="locality",
                 y="sum",
                 labels={"locality": "Stad", "sum": "Antal lediga tjänster"},
                 #title="Top 10 Vacancies per Locality",
                 hover_name='field',
                 hover_data=[],
                 color='locality',
                 text_auto=True)
    #fig.show()
    st.plotly_chart(fig)

    # KPI
    total_ads = df["sum"].sum()
    st.metric(label="Totalt antal lediga tjänster", value=int(total_ads))


# Spider chart logic

def soft_skills_radar(skills: dict, title: str):
    labels = list(skills.keys())
    scores = list(skills.values())

    # Radar charts need the data to be circular
    labels.append(labels[0])
    scores.append(scores[0])

    fig= go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=labels,
        fill='toself',
        name='Soft Skills'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0,10])
        ),
        showlegend=False,
        title=f"Top Soft Skills for: {title}"
    )

    st.plotly_chart(fig, use_container_width=True)