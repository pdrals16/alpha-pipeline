import os
import logging
import pandas as pd

from alpha.connect import alpha_postgres_connection
from alpha.checkpoint import get_files_to_process, update_checkpoint

def ingest(pipeline_name, unique_keys=None):
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

    files = get_files_to_process(f'data/bronze/{pipeline_name}', '*.csv', f'data/bronze/{pipeline_name}/.checkpoint')
    for file in files:
        print(f"Processing {file}...")

        df = pd.read_csv(file)
        
        values = [tuple(x) for x in df.to_numpy()]
        
        try:
            columns = ','.join(df.columns)
            placeholders = ','.join(['%s'] * len(df.columns))
            
            if unique_keys:
                update_columns = [col for col in df.columns if col not in unique_keys]
                
                if update_columns:
                    update_clause = ", ".join([f"{col} = EXCLUDED.{col}" for col in update_columns])
                    query = f"""
                        INSERT INTO tb_{pipeline_name} ({columns}) 
                        VALUES ({placeholders})
                        ON CONFLICT ({', '.join(unique_keys)}) 
                        DO UPDATE SET {update_clause}
                    """
                else:
                    query = f"""
                        INSERT INTO tb_{pipeline_name} ({columns}) 
                        VALUES ({placeholders})
                        ON CONFLICT ({', '.join(unique_keys)}) 
                        DO NOTHING
                    """
            else:
                query = f"INSERT INTO tb_{pipeline_name} ({columns}) VALUES ({placeholders})"
            
            cursor.executemany(query, values)
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")
            logging.error(f"Error processing {file}: {e}")
        finally:
            pass
        
        update_checkpoint(file, f'data/bronze/{pipeline_name}/.checkpoint')

    # Close connection outside the loop
    cursor.close()
    conn.close()

    return None