WITH source AS (
    SELECT * FROM {{ source('olist_raw', 'order_items') }}
)

SELECT
    CAST(order_id AS VARCHAR(50)) AS order_id,
    CAST(price AS NUMERIC(16,2)) AS price,
    CAST(freight_value AS NUMERIC(16, 2)) AS freight_value
FROM source