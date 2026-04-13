{{ config(severity = 'warn') }}

SELECT
    order_id,
    delivered_carrier_date,
    delivered_customer_date
FROM {{ ref('orders') }}
WHERE delivered_customer_date < delivered_carrier_date
  AND delivered_customer_date IS NOT NULL
  AND delivered_carrier_date IS NOT NULL