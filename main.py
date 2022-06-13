import requests
from datetime import datetime

API_KEY_STOCK = 'MUP3M9P3V54U2WGF'

STOCK_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": 'IBM',
    "outputsize": 'full',
    "datatype": 'csv',
    "apikey": API_KEY_STOCK,
}

STOCK_SEARCH_PARAMETERS = {
    "function": "SYMBOL_SEARCH",
    "keywords": 'microsoft',
    "apikey": API_KEY_STOCK,
}

