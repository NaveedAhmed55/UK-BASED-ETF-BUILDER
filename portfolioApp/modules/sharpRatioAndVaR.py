from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from portfolioApp.modules.adj_close import adj_close
from portfolioApp.modules.optimized_portfolio import optimized_portfolio
from portfolioApp.modules.get_weights import get_weights
def get_VaR(log_returns, weights, amount):
  historical_returns = (log_returns * weights).sum(axis =1)
  days = 5
  range_returns = historical_returns.rolling(window = days).sum()
  # print("before " , range_returns)
  range_returns = range_returns.dropna()
  confidence_interval = 0.99
  return -np.percentile(range_returns, 100 - (confidence_interval * 100))*amount
def sharpRatioAndVaR(amount, years, etfs, category_div, category_freq):
  end = datetime.today() - timedelta(days=3)
  start = end - timedelta(days=(years*1.5)*365)
  print(etfs)
  dis_etfs = []
  start_i = 0
  for i in category_freq:
    
    dis_etfs.append(etfs[start_i:start_i+i])
    start_i = start_i + i
  print("dis_etfs ", dis_etfs)
  result = None
  for i in range(len(dis_etfs)):
    temp = get_weights(dis_etfs[i], start, end, category_div[i], amount)
    if result is None:
      result = temp
    else:
      result["weights"] = list(result["weights"]) + list(temp["weights"])
      # result["return"] = result["return"] + temp["return"]
      # result["volatility"] = result["volatility"] + temp["volatility"]
      result["sharpRatio"] = result["sharpRatio"] + temp["sharpRatio"]
  
  #VaR calculation
  
  # adj_close_df = pd.DataFrame()
  # for ticker in etfs:
  #   adj_close_df[ticker] = adj_close(ticker, start, end)
  # adj_close_df.dropna(axis=0, inplace=True)

  #calculate log returns
  # log_returns = np.log(adj_close_df/adj_close_df.shift(1))
  # log_returns.dropna()
  # VaR = get_VaR(log_returns, result['weights'], amount)
  # result['VaR'] = VaR
  result['etfs'] = etfs
  print("result ", result)
  # print(result)
  return result