import os
import logging

from alpha.connect import alpha_postgres_connection


def ingest(pipeline_name):
    conn, cursor = alpha_postgres_connection()

    cursor.execute(f"""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'tb_{pipeline_name}'
        );
    """)
    table_exists = cursor.fetchone()[0]
    
    if not table_exists:
        logging.info(f"Table tb_{pipeline_name} not exists.")    
        with open(f"./alpha/sql/create/tb_{pipeline_name}.sql", "r") as sqlfile:
            create_sql_file = sqlfile.read()
            cursor.execute(create_sql_file)
            logging.info(f"Table tb_{pipeline_name} has been created.")
    else:
        logging.info(f"Table tb_{pipeline_name} exists.")

    return None