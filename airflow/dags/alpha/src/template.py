import logging
import pandas as pd

from alpha.src.connect import alpha_postgres_connection

def ingest(**kwargs):
    date_reference = kwargs["ds"]
    full_load = kwargs.get('full_load', False)
    
    if full_load:
        context = kwargs.get("context") + "_full_load"
    else:
        context = kwargs.get("context")


    conn, cursor = alpha_postgres_connection()

    cursor.execute(f"""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'tb_{kwargs["context"]}'
        );
    """)
    table_exists = cursor.fetchone()[0]
    
    if not table_exists:
        logging.info(f"Table tb_{kwargs["context"]} not exists.")    
        with open(f"{kwargs["airflow_home"]}/dags/alpha/src/sql/create/tb_{kwargs["context"]}.sql", "r") as sqlfile:
            create_sql_file = sqlfile.read()
            cursor.execute(create_sql_file)
            logging.info(f"Table tb_{kwargs["context"]} has been created.")
    else:
        logging.info(f"Table tb_{kwargs["context"]} exists.")

    file_name = f"{kwargs["airflow_home"]}/data/bronze/{context}/{kwargs['symbol']}/{date_reference}_{kwargs["symbol"]}.csv"
    logging.info(f"Processing {file_name}...")

    df = pd.read_csv(file_name)
    
    values = [tuple(x) for x in df.to_numpy()]
    logging.info(f"There are {len(values)} to ingest at table tb_{kwargs["context"]}.")
    
    try:
        columns = ','.join(df.columns)
        placeholders = ','.join(['%s'] * len(df.columns))
        
        unique_keys = kwargs.get("unique_keys", None)
        if unique_keys:
            logging.info(f"There are unique columns: {unique_keys}")
            update_columns = [col for col in df.columns if col not in unique_keys]
            
            if update_columns:
                update_clause = ", ".join([f"{col} = EXCLUDED.{col}" for col in update_columns])
                query = f"""
                    INSERT INTO tb_{kwargs["context"]} ({columns}) 
                    VALUES ({placeholders})
                    ON CONFLICT ({', '.join(unique_keys)}) 
                    DO UPDATE SET {update_clause}
                """
            else:
                query = f"""
                    INSERT INTO tb_{kwargs["context"]} ({columns}) 
                    VALUES ({placeholders})
                    ON CONFLICT ({', '.join(unique_keys)}) 
                    DO NOTHING
                """
        else:
            query = f"INSERT INTO tb_{kwargs["context"]} ({columns}) VALUES ({placeholders})"
        
        cursor.executemany(query, values)
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        logging.info(f"Error: {e}")
        logging.error(f"Error processing {file_name}: {e}")
    finally:
        pass
   
    cursor.close()
    conn.close()

    return None