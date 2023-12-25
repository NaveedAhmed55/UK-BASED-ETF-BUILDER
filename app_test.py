import unittest
import yfinance as yf
from portfolioApp.modules.adj_close import adj_close
from portfolioApp.modules.convert_currency import convert_currency
from portfolioApp.modules.divident import divident
from portfolioApp.modules.expenseRatioAnnual import expenseRatioAnnual
from portfolioApp.modules.fetch_live_price import fetch_live_price
from portfolioApp.modules.get_shares_amount import get_shares_amount
from portfolioApp.modules.getNumberOfEtf import getNumberOfEtf
from portfolioApp.modules.getPortfolios import getPortfolios
import numpy as np
import math
class MyTestCases(unittest.TestCase):
    def test_adj_close(self):
        AAPL_PRICES = yf.download("AAPL", "2020-01-01", "2020-01-06", progress=False)["Adj Close"]
        self.assertEqual(np.round(adj_close("AAPL", "2020-01-01", "2020-01-06")[-1]), np.round(AAPL_PRICES[-1]))
        self.assertEqual(np.round(adj_close("AAPL", "2020-01-01", "2020-01-06")[0]), np.round(AAPL_PRICES[0]))
    
    def test_convert_currency(self):
        GBP_USD = 1.27 # 1 GBP = 1.27 USD
        self.assertEqual(np.round(convert_currency(1, "GBP", "USD"), 2), GBP_USD)
        self.assertEqual(np.round(convert_currency(2, "GBP", "USD"), 2), GBP_USD*2)
        self.assertEqual(np.round(convert_currency(1, "USD", "GBP"), 2), np.round(1/GBP_USD, 2))
    
    def test_dividend(self):
        AAPL_DIVIDEND = yf.Ticker("AAPL").dividends.resample('Y').sum()[-1]
        self.assertEqual(np.round(divident(["AAPL"], [1]), 2), np.round(AAPL_DIVIDEND, 2))
        self.assertEqual(np.round(divident(["AAPL"], [2]), 2), np.round(AAPL_DIVIDEND*2, 2))
        self.assertEqual(np.round(divident(["AAPL"], [3]), 3), np.round(AAPL_DIVIDEND*3, 2))
    
    def test_expenseRatioAnnual(self):
        exp_ratio = ["0.01%", "0.02%", "0.03%"]
        prices = [100, 200, 300]
        self.assertEqual(np.round(expenseRatioAnnual(exp_ratio, prices), 2), 0.14)
    
    def test_fetch_live_price(self):
        AAPL_PRICE = yf.Ticker("AAPL").info["previousClose"]
        QQQ_PRICE = yf.Ticker("QQQ").info["previousClose"]
        INVALID_PRICE = math.inf
        self.assertTrue(np.round(abs(fetch_live_price("AAPL")-AAPL_PRICE))<=1)
        self.assertTrue(np.round(abs(fetch_live_price("QQQ")-QQQ_PRICE))<=1)
        self.assertEqual(fetch_live_price("INVALID"), INVALID_PRICE)
    
    def test_get_share_amount(self):
        prices = [100, 200, 300]
        weights = [0.5, 0.2, 0.3]
        amount = 1000
        no_shares = [5, 1, 1]
        total_amount = [500, 200, 300]
        self.assertEqual(get_shares_amount(prices, weights, amount), (no_shares, total_amount))
    
    def test_getNumberOfEtf(self):
        self.assertEqual(getNumberOfEtf(1), 5)
        self.assertEqual(getNumberOfEtf(1000), 5)
        self.assertEqual(getNumberOfEtf(5000), 5)
        self.assertEqual(getNumberOfEtf(5001), 10)
        self.assertEqual(getNumberOfEtf(10000), 10)
        self.assertEqual(getNumberOfEtf(20000), 10)
        self.assertEqual(getNumberOfEtf(20001), 15)
        self.assertEqual(getNumberOfEtf(25000), 15)
    
    def test_getPortfolios(self):
        etfs = ["AAPL", "QQQ", "SPY", "FAIL", "CRUD"]
        self.assertEqual(len(getPortfolios(1, etfs)), 10)
        self.assertEqual(len(getPortfolios(2, etfs)), 10)
        self.assertEqual(len(getPortfolios(3, etfs)), 10)
        self.assertEqual(len(getPortfolios(4, etfs)), 10)
        self.assertEqual(len(getPortfolios(5, etfs)), 1)