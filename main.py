import os
import logging
import json
import pandas as pd

from datetime import datetime
from alpha.api import AlphaVantage
from alpha.template import ingest
from alpha.checkpoint import get_files_to_process, update_checkpoint
from alpha.transform import read_daily_stock_json, read_company_overview_json, read_columns, save_as_csv


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("size_logger")


symbol = "IBM" 
today = datetime.now().strftime("%Y%m%d")
# api = AlphaVantage(symbol)
# stock_data = api.get_daily_stock_data()
# company_data = api.get_company_overview_data()

# if not os.path.exists("data/raw/daily_stocks"):
#     os.makedirs("data/raw/daily_stocks", exist_ok=True)

# if stock_data is not None:
#     print(f"Retrieved data for {symbol}:")
#     with open(f"data/raw/daily_stocks/{today}_{symbol}.json", "w") as f:
#         f.write(json.dumps(stock_data, indent=4))


# if not os.path.exists("data/raw/company_overview"):
#     os.makedirs("data/raw/company_overview", exist_ok=True)

# if company_data is not None:
#     print(f"Retrieved data for {symbol}:")
#     with open(f"data/raw/company_overview/{today}_{symbol}.json", "w") as f:
#         f.write(json.dumps(company_data, indent=4))


def process_data():
    files = get_files_to_process('data/raw/daily_stocks', '*.json', 'data/raw/daily_stocks/.checkpoint')
    
    for file in files:
        print(f"Processing {file}...")

        data = read_daily_stock_json(file)
        df = pd.DataFrame(data)

        if not os.path.exists("data/bronze/daily_stocks"):
            os.makedirs("data/bronze/daily_stocks", exist_ok=True)

        save_as_csv(df, f"data/bronze/daily_stocks/{today}_{symbol}.csv", "w")

        update_checkpoint(file, 'data/raw/daily_stocks/.checkpoint')

process_data()


def process_data():
    files = get_files_to_process('data/raw/company_overview', '*.json', 'data/raw/company_overview/.checkpoint')
    
    for file in files:
        print(f"Processing {file}...")

        data = read_company_overview_json(file)
        df = pd.DataFrame(data)

        df_renamed = read_columns(df, "alpha/config/rename_company_overview.json")

        if not os.path.exists("data/bronze/company_overview"):
            os.makedirs("data/bronze/company_overview", exist_ok=True)

        save_as_csv(df_renamed, f"data/bronze/company_overview/{today}_{symbol}.csv", "w")

        update_checkpoint(file, 'data/raw/company_overview/.checkpoint')

process_data()

PIPELINE_NAME = "daily_stocks"
UNIQUE_KEYS = ["nm_symbol","dt_reference"]
ingest(PIPELINE_NAME, UNIQUE_KEYS)

PIPELINE_NAME = "company_overview"
UNIQUE_KEYS = ["nm_symbol"]
ingest(PIPELINE_NAME, UNIQUE_KEYS)
