import os
import logging
import psycopg2

from dotenv import load_dotenv 

load_dotenv()


db_params = {
    'host': os.environ.get("ALPHA_POSTGRES_HOST"),
    'database': os.environ.get("ALPHA_POSTGRES_DB"),
    'user': os.environ.get("ALPHA_POSTGRES_USER"),
    'password': os.environ.get("ALPHA_POSTGRES_PASSWORD"),
    'port': os.environ.get("ALPHA_POSTGRES_PORT")
}

def alpha_postgres_connection():
    try:
        conn = psycopg2.connect(**db_params)
        logging.info("Connection established successfully!")
        conn.autocommit = True
        return conn, conn.cursor()
    
    except Exception as e:
        logging.info(f"Error connecting to PostgreSQL database: {e}")