# SQL queries to query df for Dashboard

# Soft/Hard skills query
def get_job_titles_by_field(connection, field: str):
    table = table_map.get(field)
    if not table:
        return []

    result = connection.execute(f"""
        SELECT DISTINCT headline 
        FROM main.{table}
        WHERE headline IS NOT NULL
    """).fetchdf()
    
    return result["headline"].tolist()

def get_description_for_title(connection, title: str):
    result = connection.execute(f"""
        SELECT description
        FROM refined.dim_job_details
        WHERE headline = '{title}'
        AND description IS NOT NULL
        LIMIT 1
    """).fetchdf()
    
    return result["description"].iloc[0] if not result.empty else ""


# Central map to resolve from UI label to mart table
table_map = {
    "Data/IT": "occupation_data_it",
    "Säkerhet och bevakning": "occupation_sakerhet_bevakning",
    "Yrken med social inriktning": "occupation_socialt_arbete"
}
