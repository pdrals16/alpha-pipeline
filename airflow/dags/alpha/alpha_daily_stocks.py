import os
import yaml

from airflow import DAG
from airflow.configuration import conf
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
from alpha.src.api_handler import get_daily_stocks, transform_to_csv
from alpha.src.template import ingest

AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/opt/airflow')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with open("dags/alpha/symbols.yaml", "r") as f:
    job_yaml = yaml.safe_load(f)

    with DAG(
        'alpha_daily_stocks',
        default_args=default_args,
        description='Ingest Alpha Daily Stocks',
        schedule_interval=job_yaml["schedule_interval"],
        start_date=datetime(2024, 11, 1),
        catchup=False,
    ) as dag:
        
        list_tasks = []
        task_names = job_yaml["tasks"]
        for task_name in task_names:
            
            with TaskGroup(group_id=task_name, dag=dag) as task:
                task_api_ingest = PythonOperator(
                    task_id='api_ingest',
                    python_callable=get_daily_stocks,
                    op_kwargs={
                        "symbol": task_name,
                        "airflow_home": AIRFLOW_HOME
                    }
                )

                task_transform_to_csv = PythonOperator(
                    task_id='transform_to_csv',
                    python_callable=transform_to_csv,
                    op_kwargs={
                        "symbol": task_name,
                        "context": "daily_stocks",
                        "airflow_home": AIRFLOW_HOME
                    }
                )

                task_ingest_to_db = PythonOperator(
                    task_id='ingest_to_db',
                    python_callable=ingest,
                    op_kwargs={
                        "symbol": task_name,
                        "context": "daily_stocks",
                        "unique_keys": ["nm_symbol", "dt_reference"],
                        "airflow_home": AIRFLOW_HOME
                    }
                )

                task_api_ingest >> task_transform_to_csv >> task_ingest_to_db