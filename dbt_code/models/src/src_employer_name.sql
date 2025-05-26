
WITH stg_job_ads AS (SELECT employer__name, 
workplace_address__municipality, 
workplace_address__country,
employer__workplace
FROM {{ source('job_ads', 'stg_ads') }})

SELECT 
    employer__name,
    workplace_address__municipality,
    workplace_address__country,
    employer__workplace
FROM stg_job_ads