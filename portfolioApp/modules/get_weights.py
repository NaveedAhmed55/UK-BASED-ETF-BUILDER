import pandas as pd
import numpy as np
from portfolioApp.modules.adj_close import adj_close
from portfolioApp.modules.optimized_portfolio import optimized_portfolio

def get_weights(etfs, start, end, total_weight, amount):
    #calculate adj close
    adj_close_df = pd.DataFrame()
    today_prices = []
    for ticker in etfs:
        adj_close_df[ticker] = adj_close(ticker, start, end)
        today_prices.append(adj_close_df[ticker][-1])
    adj_close_df.dropna(axis=0, inplace=True)
    #print("today_prices ", today_prices)
    min_weight = max(today_prices)/amount
    #calculate log returns
    log_returns = np.log(adj_close_df/adj_close_df.shift(1))
    log_returns.dropna()

    #calculate covariance matrix
    cov_matrix = log_returns.cov() * 252

    #optimize portfolio
    risk_free_rate = 0.02
    result = optimized_portfolio(etfs, log_returns, cov_matrix, risk_free_rate, total_weight, min_weight)
    return result