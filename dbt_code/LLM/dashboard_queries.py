# SQL queries to query df for Dashboard


# Function calling job titles from fields
def get_job_titles_by_field(connection, field: str):
    if field == "Data/IT":
        table = "mart.occupation_data_it"
    elif field == "Säkerhet och bevakning":
        table = "mart.occupation_sakerhet_bevakning"
    elif field == "Yrken med social inriktning":
        table = "mart.occupation_socialt_arbete"
    else:
        return []
 
    query = f"""
        SELECT DISTINCT headline
        FROM {table}
        WHERE headline IS NOT NULL
        ORDER BY headline
    """
    result = connection.execute(query).fetchdf()
    return result["headline"].tolist()

# Function calling company names from fields
def get_employer_name_for_title(connection, title:str, field:str):
    if field == "Data/IT":
        table = "mart.occupation_data_it"
    elif field == "Säkerhet och bevakning":
        table = "mart.occupation_sakerhet_bevakning"
    elif field == "Yrken med social inriktning":
        table = "mart.occupation_socialt_arbete"
    else:
        return "Ett företag"
    
    query = f"""
        SELECT employer_name 
        FROM {table}
        WHERE headline = ? AND employer_name IS NOT NULL 
        LIMIT 1
    """
    result = connection.execute(query, [title]).fetchdf()
    return result["employer_name"].iloc[0] if not result.empty else "ett företag"

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
    JOIN refined.dim_occupation o ON j.headline = o.occupation --using headline to join for now, instead of adjusting dim_occupation to include job_details_id
    WHERE lower(o.occupation_field) = ? AND j.description IS NOT NULL 
"""
    result = connection.execute(query, [field.lower()]).fetchdf()
    return " ".join(result["description"].tolist()) if not result.empty else ""

#with dim_occupation as (
#   select * from {{ ref('src_occupation') }}
#)

# select
#     {{ dbt_utils.generate_surrogate_key(['occupation']) }} as occupation_id,
#     job_details_id,
#     occupation,
#     max(occupation_group) as occupation_group,
#     max(occupation_field) as occupation_field
# from dim_occupation
# group by job_details_id, occupation

