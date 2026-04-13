{{ config(materialized='table') }}

with raw_seed as (
    select * from {{ ref('stg_customers') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['customer_unique_id']) }} AS customer_key,
    customer_id AS customer_id,
    customer_unique_id AS customer_unique_id,
    customer_city,
    customer_state
from raw_seed