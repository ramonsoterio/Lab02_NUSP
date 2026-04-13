# Olist pipeline de dados com DBT

## Instruções para executar

Criar arquivo .env na raiz do projeto, conforme exemplo:

```yaml
KAGGLE_USERNAME={{kaggle_user}}
KAGGLE_KEY={{kaggle_key}}

DBT_DB_HOST=olist_db
DBT_DB_USER=admin
DBT_DB_PASS=admin
DBT_DB_PORT=5432
```
Executar o pipeline pelo docker-compose, através do comando ``docker-compose up --build``.

## Estrutura gerada
```plantuml
@startuml

!theme plain
left to right direction
skinparam linetype ortho

class stg_customers {
   customer_id: varchar(50)
   customer_unique_id: varchar(50)
   customer_city: varchar(50)
   customer_state: varchar(2)
}
class stg_order_items {
   order_id: varchar(50)
   price: numeric(16,2)
   freight_value: numeric(16,2)
}
class stg_orders {
   order_id: varchar(50)
   customer_id: varchar(50)
   status: varchar(20)
   purchased_at: timestamp
}

@enduml

```