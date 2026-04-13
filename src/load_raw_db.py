import psycopg2

from src.config import TABLE_MAP, DB_URL, logger

def load_raw_db():

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")

    for file in TABLE_MAP:
        file += ".csv"
        table_name = file.replace('olist_', '').replace('_dataset', '').replace('.csv', '')
        full_table_name = f"raw.{table_name}"



        with open("data/raw/" + file, 'r') as f:
            header = f.readline().strip().split(',')
            columns = ", ".join([f'{h} TEXT' for h in header])

            cur.execute(f"""
                                DO $$ 
                                BEGIN 
                                    IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'raw' AND tablename = '{table_name}') THEN
                                        TRUNCATE TABLE {full_table_name};
                                    ELSE
                                        CREATE TABLE {full_table_name} ({columns});
                                    END IF;
                                END $$;
                            """)

            f.seek(0)
            sql = f"COPY {full_table_name} FROM STDIN WITH CSV HEADER DELIMITER ','"
            cur.copy_expert(sql, f)

    conn.commit()
    cur.close()
    conn.close()
    logger.info("Ingestion finished")