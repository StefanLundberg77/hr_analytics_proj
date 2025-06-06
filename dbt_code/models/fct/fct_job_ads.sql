with job_ads as (select * from {{ ref('src_job_ads') }})

select
    {{ dbt_utils.generate_surrogate_key(['occupation_label']) }} as occupation_id,
    {{ dbt_utils.generate_surrogate_key(['id']) }} as job_details_id,
    {{ dbt_utils.generate_surrogate_key(['id']) }} as auxiliary_attributes_id,
    {{ dbt_utils.generate_surrogate_key(['employer_workplace', 'workplace_address_municipality']) }}
    as employer_id,
    vacancies,
    relevance,
    application_deadline
from job_ads

-- need to add auxilliary_attributes...