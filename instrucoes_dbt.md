# DBT

## PASSO 01 - Camada Silver
 
- Baixar base de dados - Bookings
- Subir docker do banco Postgres com a carga de dados

## PASSO 02 - Instalação, configuração e teste DBT

- Criar pasta dbt-demo

```
$ mkdir dbt-demo
$ cd dbt-demo

# instalar dbt
pip install dbt-core dbt-postgres
dbt --version

# desinstalar se necesário
pip uninstall dbt-core dbt-postgres
```

Desinstalar:

Limpar as Configurações de Perfil (profiles.yml) O dbt armazena suas credenciais de banco de dados e perfis de conexão em uma pasta oculta no seu usuário. Pressione Win + R, digite %USERPROFILE% e dê Enter. Procure pela pasta chamada .dbt.

Delete a pasta inteira.

Nota: Isso apagará todas as suas senhas e conexões salvas do dbt.

B - Configuração
Instanciar o projeto
dbt init nome_do_seu_projeto

dbt init dbt_project
Projeto: dbt_project

Data base: dbt_wh

Schema: dbt_schema

Validar conexão:
cd dbt_project

dbt debug
Instalação de Bibliotecas
Criar arquivo na raiz do projeto dbt chamado: packages.yml

Dentro do arquivo adicionar:

packages:
  - package: dbt-labs/dbt_utils
    version: 1.3.3
dbt deps
C - Organização do projeto:
1 - Arquivo dbt_project.yml

2 - Estrutura dos diretórios em models:

  models/staging 
  models/intermediate
  models/marts 
3 - Testar

dbt run
4 - Configuração dbo_project.yml

version: '1.0.0'
name: 'dbt_project' # Nome do seu pacote (use o mesmo no profiles.yml se desejar)

# O profile deve bater com o nome que está no seu ~/.dbt/profiles.yml
profile: 'dbt_project'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

clean-targets:
  - "target"
  - "dbt_packages"

# --- CONFIGURAÇÃO DE MODELOS ---
# Aqui definimos as regras por pasta (Hierarquia de Pastas)
models:
  dbt_project: # Nome do projeto definido na linha 2
    
    # 1. Camada Staging: Quase sempre materializada como VIEW (Economia de custos)
    staging:
      +materialized: view
      +schema: staging         # Cria automaticamente um sufixo _staging no seu banco
    
    # 2. Camada Marts: Tabelas Finais (Devem ser TABLE para performance de BI)
    marts:
      +materialized: table
      +schema: analytics       # Cria automaticamente um sufixo _analytics
      +tags: ["gold", "bi_ready"]

## PASSO 03 - Sources
Propósito: Linhagem de dados, Validação a priori - tests, Documentação

```sql
--SQL – models/stg_vendas.sql
SELECT * FROM raw_database.vendas_schema.tabela_vendas -- ❌ Ruim de manter
```
```sql
--SQL – models/stg_vendas.sql
SELECT * FROM {{ source('sistema_vendas', 'vendas') }} -- ✅ Profissional e Seguro
```

No seu arquivo nome_aquivo_sources.yml:

YAML - Estrutura
```yaml
sources:
  - name: nome_referencia_source
    database: database_origem
    schema: schema_origem
    tables:
      - name: tabela1_origem
        description: "Descrição da tabela 1 de origem."
        columns: 
          - name: coluna_origem
            description: "Descrição da coluna, metadados"
            tests:
              - unique
              - not_null
      - name: tabela2_origem
          description: "Descrição da tabela 2 de origem."
      ...
```

Onde definir as sources?
```mermaid
models/
├── staging/                # Camada RAW (Bruta)
│   ├── google_ads/
│   │   ├── _sources.yml    <-- As SOURCES ficam AQUI
│   │   ├── stg_google_ads__campaigns.sql
│   │   └── stg_google_ads__ad_groups.sql
│   └── booking_system/
│       ├── _sources.yml    <-- E AQUI para outra origem
│       └── stg_bookings.sql
├── intermediate/           # Camada de Transformação (Joins complexos)
│   ├── finance/
│   │   ├── _int_finance_models.yml
│   │   └── int_payments_pivoted.sql
└── marts/                  # Camada de Negócio (Final/Gold)
    ├── marketing/
    │   ├── _marts_marketing.yml
    │   └── fct_ad_performance.sql
    └── finance/
        └── dim_customers.sql
```

No nosso exemplo, dentro da staging criar arquivo booking_sources.yml
```yaml
version: 2

sources:
  - name: booking_sources
    database: dbt_lab2
    schema: bookings
    description: "Camada Raw (bruta) do sistema de aviação, contendo reservas, tickets e voos."
    
    tables:
      # --- Tabela de Reservas ---
      - name: bookings
        description: "Registros de reservas realizadas no sistema."
        columns: 
          - name: book_ref
            description: "Identificador alfanumérico único da reserva."
            tests:
              - unique
              - not_null
          - name: book_date
            description: "Data em que a reserva foi confirmada."
            tests:
              - not_null

      # --- Tabela de Bilhetes (Tickets) ---
      - name: tickets
        description: "Bilhetes individuais emitidos para passageiros vinculados a uma reserva."
        columns:
          - name: ticket_no
            description: "Número do bilhete (Chave Primária)."
            tests:
              - unique
              - not_null
          - name: passenger_name
            description: "Nome completo do passageiro conforme documento."
            tests:
              - not_null
          - name: book_ref
            description: "Chave estrangeira vinculando o bilhete à reserva."
            tests:
              - not_null
              - relationships:
                  to: source('booking_sources', 'bookings')
                  field: book_ref

      # --- Tabela de Segmentos de Voo (Ticket Flights) ---
      - name: ticket_flights
        description: "Relacionamento muitos-para-muitos entre tickets e voos."
        columns:
          - name: ticket_no
            description: "Número do bilhete vinculado ao voo."
            tests:
              - not_null
              - relationships:
                  to: source('booking_sources', 'tickets')
                  field: ticket_no
          - name: flight_id
            description: "ID do voo associado ao bilhete."
            tests:
              - not_null
              - relationships:
                  to: source('booking_sources', 'flights')
                  field: flight_id

      # --- Tabela de Voos ---
      - name: flights
        description: "Cronograma de voos com status, horários e aeronaves."
        columns:
          - name: flight_id
            description: "Identificador único do voo."
            tests:
              - unique
              - not_null
          - name: flight_no
            description: "Código do voo (ex: PG0013)."
            tests:
              - not_null

      # --- Tabela de Aeroportos ---
      - name: airports
        description: "Cadastro de aeroportos (Origem/Destino)."
        columns:
          - name: airport_code
            description: "Código IATA de 3 letras (ex: SJP, GRU)."
            tests:
              - unique
              - not_null
```

## PASSO 04 - Models
Dentro de marts, criar arquivo fact_ticket_flight.sql

```sql
with ticket_flights as (
    select * from {{ source('booking_sources', 'ticket_flights') }}
),
flights as (
    select * from {{ source('booking_sources', 'flights') }}
),
tickets as (
    select * from {{ source('booking_sources', 'tickets') }}
)

select
    tf.ticket_no,
    tf.flight_id,
    t.book_ref,
    f.aircraft_code,
    tf.fare_conditions,
    tf.amount,
    f.scheduled_departure,
    f.scheduled_arrival,
    f.actual_departure,
    f.actual_arrival

from ticket_flights tf
join flights f on tf.flight_id = f.flight_id
join tickets t on tf.ticket_no = t.ticket_no
```
Executar para executar
```
$ dbt run
```

## PASSO 05 - Macros
Criar arquivo chamado na pasta macros: get_flight_duration.sql

{% macro get_flight_duration(departure_column, arrival_column) %}
    -- Calcula a duração em minutos, retornando NULL se algum campo for nulo
    CASE 
        WHEN {{ departure_column }} IS NOT NULL AND {{ arrival_column }} IS NOT NULL 
        THEN EXTRACT(EPOCH FROM ({{ arrival_column }} - {{ departure_column }})) / 60
        ELSE NULL 
    END
{% endmacro %}
Modificar modelo fact_ticket_flight.sql

with ticket_flights as (
    select * from {{ source('booking_sources', 'ticket_flights') }}
),
flights as (
    select * from {{ source('booking_sources', 'flights') }}
),
tickets as (
    select * from {{ source('booking_sources', 'tickets') }}
)

select
    tf.ticket_no,
    tf.flight_id,
    t.book_ref,
    f.aircraft_code,
    tf.fare_conditions,
    tf.amount,
    f.scheduled_departure,
    f.scheduled_arrival,
    f.actual_departure,
    f.actual_arrival,

    -- Usando a Macro para duração planejada
    {{ get_flight_duration('f.scheduled_departure', 'f.scheduled_arrival') }} as scheduled_duration_minutes,
    
    -- Usando a Macro para duração real (pode ser NULL)
    {{ get_flight_duration('f.actual_departure', 'f.actual_arrival') }} as actual_duration_minutes

from ticket_flights tf
join flights f on tf.flight_id = f.flight_id
join tickets t on tf.ticket_no = t.ticket_no
PASSO 06 - Tests
Testes genéricos: Criar arquivo no mesmo diretório dos modelos: generic_tests.yml

version: 2

models:
  - name: fact_ticket_flight
    description: "Tabela fato que consolida as vendas de passagens por segmento de voo."
    columns:
      # 1. Chave Composta (Ticket + Voo) deve ser única
      - name: "(ticket_no || '-' || flight_id)"
        description: "Chave primária composta"
        tests:
          - unique
          - not_null

      # 2. Integridade Referencial (Garantir que o ticket existe na origem)
      - name: ticket_no
        tests:
          - not_null
          - relationships:
              to: source('booking_sources', 'tickets')
              field: ticket_no

      # 3. Validação de Regra de Negócio (O valor da passagem não pode ser negativo)
      - name: amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              inclusive: true

      # 4. Validação de Classe de Viagem
      - name: fare_conditions
        tests:
          - not_null
          - accepted_values:
              values: ['Economy', 'Comfort', 'Business']
              quote: true

Testes Singulares: Testes no dbt retornam falha se a query retornar QUALQUER linha. Portanto, buscamos o que está ERRADO.

Criar arquivo no diretório de tests: verificar_chegada_apos_saida.sql

select
    flight_id,
    scheduled_departure,
    scheduled_arrival
from {{ ref('fact_ticket_flight') }}
where scheduled_arrival <= scheduled_departure
Para executar testes

dbt test
Passo 07 - Gerar e visualizar Documentação
1. Compila o projeto e gera o arquivo ‘catalog.json’ com os metadados do banco
dbt docs generate
2. Inicia um servidor web local para você visualizar a documentação no navegador
dbt docs serve
dbt docs serve --port 8001