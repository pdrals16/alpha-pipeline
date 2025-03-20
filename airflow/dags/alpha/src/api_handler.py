import os
import logging
import json
import pandas as pd

from datetime import datetime
from alpha.src.api import AlphaVantage
from alpha.src.checkpoint import get_files_to_process, update_checkpoint
from alpha.src.transform import read_daily_stock_json, read_company_overview_json, read_columns, save_as_csv


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("size_logger")
TODAY = datetime.now().strftime("%Y%m%d")

def get_daily_stocks(**kwargs):
    api = AlphaVantage(kwargs["symbol"])
    stock_data = api.get_daily_stock_data()

    if not os.path.exists(f"{kwargs["airflow_home"]}/data/raw/daily_stocks/{kwargs['symbol']}"):
      os.makedirs(f"{kwargs["airflow_home"]}/data/raw/daily_stocks/{kwargs['symbol']}", exist_ok=True)

    if stock_data is not None:
        print(f"Retrieved data for {kwargs["symbol"]}:")
        with open(f"{kwargs["airflow_home"]}/data/raw/daily_stocks/{kwargs['symbol']}/{TODAY}_{kwargs["symbol"]}.json", "w") as f:
            f.write(json.dumps(stock_data, indent=4))


def get_company_overview(**kwargs):
    api = AlphaVantage(kwargs["symbol"])
    stock_data = api.get_company_overview_data()

    if not os.path.exists(f"{kwargs["airflow_home"]}/data/raw/company_overview/{kwargs['symbol']}"):
      os.makedirs(f"{kwargs["airflow_home"]}/data/raw/company_overview/{kwargs['symbol']}", exist_ok=True)

    if stock_data is not None:
        print(f"Retrieved data for {kwargs["symbol"]}:")
        with open(f"{kwargs["airflow_home"]}/data/raw/company_overview/{kwargs['symbol']}/{TODAY}_{kwargs["symbol"]}.json", "w") as f:
            f.write(json.dumps(stock_data, indent=4))


def transform_to_csv(**kwargs):
    files = get_files_to_process(f"{kwargs["airflow_home"]}/data/raw/{kwargs["context"]}/{kwargs['symbol']}", "*.json", f"{kwargs["airflow_home"]}/data/raw/{kwargs["context"]}/{kwargs['symbol']}/.checkpoint")
    
    for file in files:
        print(f"Processing {file}...")

        if kwargs["context"]=="daily_stocks":
            data = read_daily_stock_json(file)
            df = pd.DataFrame(data)
        elif kwargs["context"]=="company_overview":
            data = read_company_overview_json(file)
            df_ = pd.DataFrame(data)
            df = read_columns(df_, f"{kwargs["airflow_home"]}/dags/alpha/src/config/rename_company_overview.json")
        else:
            raise("There is no dataframe!")

        if not os.path.exists(f"{kwargs["airflow_home"]}/data/bronze/{kwargs["context"]}/{kwargs['symbol']}"):
            os.makedirs(f"{kwargs["airflow_home"]}/data/bronze/{kwargs["context"]}/{kwargs['symbol']}", exist_ok=True)

        save_as_csv(df, f"{kwargs["airflow_home"]}/data/bronze/{kwargs["context"]}/{kwargs['symbol']}/{TODAY}_{kwargs["symbol"]}.csv", "w")

        update_checkpoint(file, f"{kwargs["airflow_home"]}/data/raw/{kwargs["context"]}/{kwargs['symbol']}/.checkpoint")
