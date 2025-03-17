import json
import pandas as pd


def read_daily_stock_json(file_path) -> list[dict]:
    """
    Parse daily stock time series JSON data from Alpha Vantage into a structured format.
    
    Args:
        file_path: Path to the JSON file containing daily stock data
            
    Returns:
        List of dictionaries, each representing a day's stock data with standardized fields:
        date, open, high, low, close, and volume
    """
    with open(file_path, "r") as file:
        json_str = file.read()
    
    json_data = json.loads(json_str)
    
    rows = []
    for date, values in json_data["Time Series (Daily)"].items():
        row = {
            "date": date,
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"]),
            "volume": int(values["5. volume"])
        }
        rows.append(row)
    return rows

def read_company_overview_json(file_path) -> list[dict]:
    """
    Extract company overview information from Alpha Vantage JSON data.
    
    Args:
        file_path: Path to the JSON file containing company overview data
            
    Returns:
        List containing a single dictionary with company overview information
    """
    with open(file_path, "r") as file:
        json_str = file.read()

    json_data = json.loads(json_str)
    return [json_data]


def read_columns(df, file_reference):
    """
    Rename DataFrame columns based on a JSON mapping file.
    
    Args:
        df: Pandas DataFrame whose columns need to be renamed
        file_reference: Path to a JSON file containing column mapping information
            
    Returns:
        DataFrame with renamed columns according to the mapping
    """
    with open(file_reference, "r") as file:
        json_str = file.read()
    json_data = json.loads(json_str)
    
    df_renamed = df.rename(columns=json_data)
    return df_renamed

def save_as_csv(data, table_name, mode):
    """
    Save data to a CSV file with specified parameters.
    
    Args:
        data: Pandas DataFrame to be saved
        table_name: Name of the output CSV file
        mode: File write mode ('w' for write/overwrite, 'a' for append)
            
    Returns:
        Boolean indicating success (True) or failure (False) of the operation
    """
    if isinstance(data, pd.DataFrame):
        data.to_csv(table_name, index=False, mode=mode, header=True)
        return True
    else:
        return False

