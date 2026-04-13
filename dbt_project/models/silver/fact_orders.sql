{{ config(materialized='table') }}

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

order_items_summarized AS (
    SELECT
        order_id,
        SUM(price) AS total_item_value,
        SUM(freight_value) AS total_freight_value,
        SUM(price + freight_value) AS total_order_item_value
    FROM {{ ref('stg_order_items') }}
    GROUP BY 1
),

customers AS (
    SELECT * FROM {{ ref('dim_customers') }}
),

final AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['o.order_id']) }} as fact_key,
        o.order_id,
        c.customer_key,
        o.status,
        o.purchased_at AS order_date,
        COALESCE(i.total_item_value, 0) AS item_value,
        COALESCE(i.total_freight_value, 0) AS freight_value
    FROM orders o
    LEFT JOIN order_items_summarized i ON o.order_id = i.order_id
    LEFT JOIN customers c ON o.customer_id = c.customer_id
)

SELECT * FROM final