from .Stock import *


class Portfolio:
    """Class that represents a Portfolio object"""
    def __init__(self, symbols=[], period="max"):
        self.Symbols = symbols
        self.Stocks = None
        self._downloadStocks()
    
    def _downloadStocks(self):
        self.Stocks = yf.download(self.Symbols, period="1y")["Adj Close"]
        self.Stocks.dropna(inplace=True)


