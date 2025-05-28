{{ config(materialized='view') }}

with fct as (
    select * from {{ ref('fct_job_ads') }}
),
occ as (
    select * from {{ ref('dim_occupation') }}
),
emp as (
    select * from {{ ref('dim_employer_name') }}
),
job as (
    select * from {{ ref('dim_job_details') }}
),
aux as (
    select * from {{ ref('dim_auxiliary_attributes') }}
)

select
    fct.job_details_id,
    job.headline,
    occ.occupation,
    occ.occupation_field,
    emp.employer__name,
    emp.municipality,
    emp.country,
    fct.vacancies,
    fct.application_deadline,
    fct.relevance,
    job.salary_type,
    job.salary_description,
    job.working_hours_type,
    aux.experience_required_text,
    aux.driver_license_text,
    aux.access_to_own_car_text

from fct
left join occ on fct.occupation_id = occ.occupation_id
left join emp on fct.employer_id = emp.employer_id
left join job on fct.job_details_id = job.job_details_id
left join aux on fct.auxiliary_attributes_id = aux.auxiliary_attributes_id

where lower(occ.occupation_field) = 'säkerhet och bevakning'
