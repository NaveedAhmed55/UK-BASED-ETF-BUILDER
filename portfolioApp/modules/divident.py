import yfinance as yf
def divident(etf_list, no_stocks):
  divident_amount = 0
  for x,n in zip(etf_list, no_stocks):
    etf_ticker = yf.Ticker(x)
    dividend_history = etf_ticker.dividends
    divident_amount += n* dividend_history.resample('Y').sum()[-1]
  return divident_amount