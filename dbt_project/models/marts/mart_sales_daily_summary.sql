with customers as (
    select
        customer_key,
        customer_city,
        customer_state
    from {{ ref('dim_customers') }}
),

fact_orders as (
    select
        customer_key,
        status,
        freight_value,
        (item_value - freight_value) as price, 
        order_date
    from {{ ref('fact_orders') }}
),

joined as (
    select
        c.customer_city,
        c.customer_state,
        date_trunc('month', f.order_date) as period,
        f.status,
        f.price,
        f.freight_value
    from fact_orders f
    inner join customers c on f.customer_key = c.customer_key
)

select
    customer_city,
    customer_state,
    CAST(period AS DATE) as period,
    status,
    sum(price) as total_price,
    sum(freight_value) as total_freight
from joined
group by 1, 2, 3, 4