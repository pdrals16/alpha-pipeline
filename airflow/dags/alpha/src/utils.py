import os 


def extract_symbol(filepath):
    """
    Extract the stock symbol from filenames like '20250319_IBM.json' or '20250319_IBM.csv'
    
    Args:
        filename (str): The filename containing the symbol
        
    Returns:
        str: The extracted symbol
    """
    filename = os.path.basename(filepath)

    parts = filename.split('_')
    
    if len(parts) != 2:
        raise ValueError(f"Unexpected filename format: {filename}. Expected format: 'date_SYMBOL.extension'")
    
    symbol_with_ext = parts[1]
    symbol = symbol_with_ext.split('.')[0]
    
    return symbol