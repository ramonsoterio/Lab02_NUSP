WITH source AS (
    SELECT * FROM {{ source('olist_raw', 'orders') }}
)

SELECT
    CAST(order_id AS VARCHAR(50)) AS order_id,
    CAST(customer_id AS VARCHAR(50)) AS customer_id,
    CAST (order_status AS VARCHAR(20)) AS status,
    NULLIF(order_purchase_timestamp, '')::timestamp AS purchased_at
FROM source