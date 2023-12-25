import pandas as pd
import concurrent.futures
from portfolioApp.modules.fetch_live_price import fetch_live_price

def getDf():
  df = pd.read_csv('static/etfs_list.csv')
  tickers = df['symbol'].tolist()
  
  adj_close = []
  
  # Use a ThreadPoolExecutor for concurrent processing
  with concurrent.futures.ThreadPoolExecutor() as executor:
    # Submit tasks for fetching live prices
    futures = [executor.submit(fetch_live_price, ticker) for ticker in tickers]
    
    # Retrieve results as they become available
    for future in concurrent.futures.as_completed(futures):
      adj_close.append(future.result())

  df["adj_close"] = adj_close
  print("minimum", min(adj_close))
  print("maximum", max(adj_close))
  return df