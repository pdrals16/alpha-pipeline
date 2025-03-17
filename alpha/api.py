import os
import sys
import logging
import requests

from dotenv import load_dotenv 
from typing import Dict

load_dotenv()

API_KEY = os.environ.get("ALPHA_API")
BASE_URL = os.environ.get("BASE_URL")


class AlphaVantage:
    def __init__(self, symbol: str):
        self.symbol = symbol
        pass

    def get_request_data(self, params: dict) -> Dict:
        """
        Fetch data from Alpha Vantage API.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'IBM', 'AAPL', 'MSFT')
            
        Returns:
            Dict containing the data, or None if request failed
        """
        reference = f"{params["symbol"]} - {params["function"]}"
        try:
            logging.info(f"Requesting for {reference}.")
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if "Error Message" in data:
                logging.info(f"{reference} API Error: {data['Error Message']}.")
                return None

            size_kb = sys.getsizeof(data) / 1024
            logging.info(f"{reference} API Response has {size_kb:.2f} KB.")
            return data
        
        except requests.exceptions.RequestException as e:
            logging.info(f"Request failed: {e}.")
            return None
        except Exception as e:
            logging.info(f"Unexpected error: {e}.")
            return None


    def get_daily_stock_data(self) -> Dict:
        """
        Fetch daily time series stock data from Alpha Vantage API.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'IBM', 'AAPL', 'MSFT')
            
        Returns:
            Dict containing the daily stock data, or None if request failed
        """
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": self.symbol,
            "apikey": API_KEY,
            "outputsize": "compact"
        }

        data = self.get_request_data(params=params) 
        return data


    def get_company_overview_data(self) -> Dict:
        """
        Fetch Company Overview data from Alpha Vantage API.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'IBM', 'AAPL', 'MSFT')
            
        Returns:
            Dict containing the company overview data, or None if request failed
        """
        params = {
            "function": "OVERVIEW",
            "symbol": self.symbol,
            "apikey": API_KEY
        }

        data = self.get_request_data(params=params) 
        return data
        
        