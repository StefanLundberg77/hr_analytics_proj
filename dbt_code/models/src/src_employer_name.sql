
WITH stg_job_ads AS (SELECT employer__name, 
workplace_address__municipality, 
workplace_address__country,
employer__workplace
FROM {{ source('job_ads', 'stg_ads') }})

SELECT 
    employer__name as employer_name,
    workplace_address__municipality as workplace_address_municipality,
    workplace_address__country as workplace_address_country,
    employer__workplace as employer_workplace
FROM stg_job_ads