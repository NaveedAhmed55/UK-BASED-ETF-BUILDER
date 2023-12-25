import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
def returns(etf_list, ndays):
  end_date = datetime.today()
  start_date = end_date - timedelta(days=ndays)
  total = 0
  for etf in etf_list:
    etf_data = yf.download(etf, start=start_date, end=end_date, progress=False)
    etf_return = (etf_data['Adj Close'][-1] / etf_data['Adj Close'][0]) - 1
    total += etf_return
  return str(np.round(total*100, 2))+"%"