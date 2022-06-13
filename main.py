import requests
import pandas as pd
from datetime import datetime

API_KEY_STOCK = 'MUP3M9P3V54U2WGF'

STOCK_ENDPOINT = "https://www.alphavantage.co/query"

STOCK_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": 'IVV',
    "outputsize": 'full',
    "datatype": 'json',
    "apikey": API_KEY_STOCK,
}

STOCK_SEARCH_PARAMETERS = {
    "function": "SYMBOL_SEARCH",
    "keywords": 'microsoft',
    "apikey": API_KEY_STOCK,
}

response_stocks = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMETERS)
response_stocks.raise_for_status()
data = response_stocks.json()
data = data["Time Series (Daily)"]
df = pd.DataFrame.from_dict(data)
df = df.transpose()
df = df.rename(columns={"1. open": "open", "2. high": "high", "3. low": "low", "4. close": "close", "5. volume": "volume"})
print(df.head())

