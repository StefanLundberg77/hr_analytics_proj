# SQL queries to query df for Dashboard

# Soft/Hard skills query
def get_job_titles_by_field(connection, field: str):
    if field == "Data/IT":
        table = "main.occupation_data_it"
    elif field == "Säkerhet och bevakning":
        table = "main.occupation_sakerhet_bevakning"
    elif field == "Yrken med social inriktning":
        table = "main.occupation_socialt_arbete"
    else:
        return []

    result = connection.execute(f"""
        SELECT DISTINCT headline
        FROM {table}
        WHERE headline IS NOT NULL
        ORDER BY headline
    """).fetchdf()

    return result["headline"].tolist()

def get_description_for_title(connection, title: str):
    query = """
        SELECT description
        FROM refined.dim_job_details
        WHERE headline = ? AND description IS NOT NULL
        LIMIT 1
    """
    result = connection.execute(query, [title]).fetchdf()
    return result["description"].iloc[0] if not result.empty else ""

# Concatenated descriptions for each of the 3 occupational fields:
def get_descriptions_for_field(connection, field:str):
    query = """
    SELECT j.description
    FROM refined.dim_job_details j 
    JOIN refined.dim_occupation o ON j.job_details_id = o.job_details_id
    WHERE lower(o.occupation_field) = ? AND j.description IS NOT NULL 
"""
    result = connection.execute(query, [field.lower()]).fetchdf()
    return " ".join(result["description"].tolist()) if not result.empty else ""

