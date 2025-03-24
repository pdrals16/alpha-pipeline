import os
import logging
import json
import pandas as pd

from alpha.src.api import AlphaVantage
from alpha.src.transform import read_daily_stock_json, read_company_overview_json, read_columns, save_as_csv


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("size_logger")


def save_api_content(**kwargs):
    api = AlphaVantage(kwargs["symbol"])
    full_load = kwargs.get("full_load", False)
    date_reference = kwargs.get("ds")

    if kwargs.get("context")=="daily_stocks":
        content = api.get_daily_stock_data(full_load)
    elif kwargs.get("context")=="company_overview":
        content = api.get_company_overview_data()
    else:
        raise(f"Do not exist context {kwargs.get("context")}.")
    
    if full_load:
        context = kwargs.get("context") + "_full_load"
    else:
        context = kwargs.get("context")

    if not os.path.exists(f"{kwargs["airflow_home"]}/data/raw/{context}/{kwargs['symbol']}"):
        os.makedirs(f"{kwargs["airflow_home"]}/data/raw/{context}/{kwargs['symbol']}", exist_ok=True)

    if content is not None:
        logger.info(f"Retrieved data for {kwargs["symbol"]}:")
        with open(f"{kwargs["airflow_home"]}/data/raw/{context}/{kwargs['symbol']}/{date_reference}_{kwargs["symbol"]}.json", "w") as f:
            f.write(json.dumps(content, indent=4))
    return None


def transform_to_csv(**kwargs):
    date_reference = kwargs['ds']
    full_load = kwargs.get('full_load', False)
    
    if full_load:
        context = kwargs.get("context") + "_full_load"
    else:
        context = kwargs.get("context")

    file_name = f"{kwargs["airflow_home"]}/data/raw/{context}/{kwargs['symbol']}/{date_reference}_{kwargs["symbol"]}.json"
    logger.info(f"Processing {file_name}...")

    if kwargs["context"]=="daily_stocks":
        data = read_daily_stock_json(file_name)
        df_ = pd.DataFrame(data)

        if not full_load:
            logger.info("Running a daily mode.")
            df = df_[df_["dt_reference"]==date_reference]
        else:
            logger.info("Running a full load.")
            df = df_

    elif kwargs["context"]=="company_overview":
        data = read_company_overview_json(file_name)
        df_ = pd.DataFrame(data)

        df = read_columns(df_, f"{kwargs["airflow_home"]}/dags/alpha/src/config/rename_company_overview.json")
    else:
        raise(f"Do not exist context {kwargs.get("context")}.")

    if not os.path.exists(f"{kwargs["airflow_home"]}/data/bronze/{context}/{kwargs['symbol']}"):
        os.makedirs(f"{kwargs["airflow_home"]}/data/bronze/{context}/{kwargs['symbol']}", exist_ok=True)

    save_as_csv(df, f"{kwargs["airflow_home"]}/data/bronze/{context}/{kwargs['symbol']}/{date_reference}_{kwargs["symbol"]}.csv", "w")

    return None
