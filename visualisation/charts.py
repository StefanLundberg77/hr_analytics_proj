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
import plotly_express as px
import plotly.graph_objects as go

#Region SPIDER CHART

# Spider chart logic for soft/hard skills generator
# Soft skills radar chart has a 'occupation field average' as a baseline comparison to
# show whether specific jobs have overlap or differences in desired skills for candidates

def soft_skills_radar(job_skills: dict, field_skills: dict, title: str):
# Convert job-level skills to plotting format

    job_labels = list(job_skills.keys())
    job_scores = list(job_skills.values())

    # Radar charts need the data to be circular
    job_labels.append(job_labels[0])
    job_scores.append(job_scores[0])

    # Convert field-level (average) skills to plot format
    field_labels = list(field_skills.keys())
    field_scores = list(field_skills.values())
    field_labels.append(field_labels[0])
    field_scores.append(field_scores[0])

    #Create radar chart
    fig= go.Figure()

    # Baseline plot for 'industry/field average' soft skills
    fig.add_trace(go.Scatterpolar(
        r=field_scores,
        theta=field_labels,
        fill='toself',
        name='Field Average Soft Skills'
    ))

    # Job-specific soft skills: selected
    fig.add_trace(go.Scatterpolar(
        r=job_scores,
        theta=job_labels,
        fill='toself',
        name='Selected Job' # Selected job
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,10])),
        showlegend=True,
        title=f"Top Soft Skills for: {title} vs Field Average"
    )

    st.plotly_chart(fig, use_container_width=True)

 # HARD skills radar plot
def hard_skills_radar(job_skills: dict, title: str):
    job_labels = list(job_skills.keys())
    job_scores = list(job_skills.values())

    # Radar charts need the data to be circular
    job_labels.append(job_labels[0])
    job_scores.append(job_scores[0])

    fig= go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=job_scores,
        theta=job_labels,
        fill='toself',
        name='Hard Skills'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0,10])
        ),
        showlegend=False,
        title=f"Top Hard Skills for: {title}"
    )

    st.plotly_chart(fig, use_container_width=True)


#endregion

#Region Soft Skills Bar Chart

def soft_skills_field_bar_chart(field_skills: dict, field_name: str):

    df = pd.DataFrame(list(field_skills.items()), columns=["Skill", "Score"])
    df = df.sort_values(by="Score", ascending=False)

    #Plot Bar Chart
    fig = px.bar(
        df,
        x="Skills",
        y="Score",
        text="Score",
        labels={"Skill": "Soft Skill", "Score": "Importance"},
        title=f"Top Soft Skills in {field_name}"
    )
    fig.update_traces(texttemplate='%{text}', textposition='outisde')
    fig.update_layout(yaxis_range=[0, 10], xaxis_tickangle=-30)

    st.plotly_chart(fig, use_container_width=True)


# #from visualisation.kpis import occupation_query, locality_query, total_ads

# # Pie-chart function vacancies/occupational role
# def pie_occupation():

#     df = occupation_query()

#     top = st.checkbox("Visa top 10", value=False) 

#     # check user input
#     if top:
#         # sort df and select top 10
#         df_top = df.sort_values(by="antal",
#                                 ascending=False).head(10)
#         df = df_top


#     fig = px.pie(df, names="beteckning",
#                          values="antal",
#                          labels={"beteckning":"Beteckning", "antal":"Antal lediga tjänster"},
#                          title="Lediga tjänster per yrkesbeteckning")

#     fig.update_traces(
#     textinfo='percent',
#     hoverinfo='label+percent+value',
#     textposition='inside')
#     st.plotly_chart(fig, use_container_width=True)

# def vacancies_per_locality():

#     # create Dataframe from query
#     df = locality_query()
#     # header for chart
#     st.subheader("Antal lediga tjänster per ort")

#     # checkbox for missing city data
#     missing_city_data = st.checkbox("Inkludera annonser där 'Stad ej angiven'", value=False) 

#     # check user input
#     if not missing_city_data:
#         df = df[df["locality"] != "Ej angivet"]
    
#     # Sort values after top 10
#     df_top = df.sort_values(by="sum",
#                             ascending=False).head(10)

#     # create figure
#     fig = px.bar(df_top, 
#                  x="locality",
#                  y="sum",
#                  labels={"locality": "Stad", "sum": "Antal lediga tjänster"},
#                  hover_name='field',
#                  hover_data=[],
#                  color='locality',
#                  text_auto=True)
#     #fig.show()
#     st.plotly_chart(fig)

#     # KPI
#     total_ads(df_top)