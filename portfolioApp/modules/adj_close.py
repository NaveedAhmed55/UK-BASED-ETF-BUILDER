import yfinance as yf

def adj_close(ticker, start, end):
  data = yf.download(ticker, progress=False, start=start, end=end)
  if data.shape[0] == 0:
    data = yf.download(ticker, progress=False)
  return data['Adj Close']