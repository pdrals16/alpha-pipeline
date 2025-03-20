import os
import logging
import psycopg2

from airflow.models import Variable 


db_params = {
    'host': Variable.get("ALPHA_POSTGRES_HOST"),
    'database': Variable.get("ALPHA_POSTGRES_DB"),
    'user': Variable.get("ALPHA_POSTGRES_USER"),
    'password': Variable.get("ALPHA_POSTGRES_PASSWORD"),
    'port': Variable.get("ALPHA_POSTGRES_PORT")
}

def alpha_postgres_connection():
    try:
        conn = psycopg2.connect(**db_params)
        logging.info("Connection established successfully!")
        conn.autocommit = True
        return conn, conn.cursor()
    
    except Exception as e:
        logging.info(f"Error connecting to PostgreSQL database: {e}")