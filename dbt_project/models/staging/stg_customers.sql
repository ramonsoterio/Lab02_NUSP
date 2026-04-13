WITH source AS (
    SELECT * FROM {{ source('olist_raw', 'customers') }}
)

SELECT
    CAST(customer_id AS VARCHAR(50)) AS customer_id,
    CAST(customer_unique_id AS VARCHAR(50)) AS customer_unique_id,
    CAST(customer_city AS VARCHAR(50)) AS customer_city,
    CAST(customer_state AS VARCHAR(2)) AS customer_state
FROM source