import yahoo_fin.stock_info as si
import math
def fetch_live_price(ticker):
  # print(ticker)
  try:
    live_price = si.get_live_price(ticker)
  except:
    live_price = math.inf
  return live_price