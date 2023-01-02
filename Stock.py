import yfinance as yf


class Stock:
    def __init__(self, symbol, start, end):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.df = yf.download(tickers=self.symbol, start=self.start, end=self.end)



