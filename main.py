import json
import logging

from alpha.api import AlphaVantage


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("size_logger")

symbol = "IBM" 
api = AlphaVantage(symbol)
stock_data = api.get_daily_stock_data()
company_data = api.get_company_overview_data()

if stock_data is not None:
    print(f"Retrieved data for {symbol}:")
    with open(f"data/daily_stock_{symbol}.json", "w") as f:
        f.write(json.dumps(stock_data, indent=4))

if company_data is not None:
    print(f"Retrieved data for {symbol}:")
    with open(f"data/company_overview_{symbol}.json", "w") as f:
        f.write(json.dumps(company_data, indent=4))