import logging
import pandas as pd

from datetime import datetime
from alpha.api import AlphaVantage
from alpha.template import ingest
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

# if stock_data is not None:
#     print(f"Retrieved data for {symbol}:")
#     with open(f"data/daily_stock_{symbol}.json", "w") as f:
#         f.write(json.dumps(stock_data, indent=4))

# if company_data is not None:
#     print(f"Retrieved data for {symbol}:")
#     with open(f"data/company_overview_{symbol}.json", "w") as f:
#         f.write(json.dumps(company_data, indent=4))


# file_path = "D:/side-projects/alpha-pipeline/data/daily_stock_IBM.json"  
# data = read_daily_stock_json(file_path)
# df = pd.DataFrame(data)
# save_as_csv(df, f"data/{today}_daily_stock_{symbol}.csv", "w")

# file_path = "D:/side-projects/alpha-pipeline/data/company_overview_IBM.json"  
# data = read_company_overview_json(file_path)
# df = pd.DataFrame(data)
# df_renamed = read_columns(df, "alpha/rename_company_overview.json")
# save_as_csv(df_renamed, f"data/{today}_company_overview_{symbol}.csv", "w")

PIPELINE_NAME = "daily_stocks"
ingest(PIPELINE_NAME)

PIPELINE_NAME = "company_overview"
ingest(PIPELINE_NAME)
