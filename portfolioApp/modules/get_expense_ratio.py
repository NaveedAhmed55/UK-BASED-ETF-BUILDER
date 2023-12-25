import yfinance as yf
import yahoo_fin.stock_info as si
import pandas as pd
from portfolioApp.modules.convert_currency import convert_currency
def get_expense_ratio(etfs_list, df):
  expense_ratios = []
  company_names = []
  previous_close = []
  asset_class = []
  # print("etfs_list ", etfs_list)
  for ticker in etfs_list:
    tk = yf.Ticker(ticker)
    d1 = si.get_analysts_info(ticker)[0]
    d2 = tk.get_info()
    company_names.append(d2['longName'])
    asset_class.append(df.loc[df['symbol']==ticker,'category'].values[0])
    ratio = d1.loc[d1[0]=='Expense Ratio (net)', 1].values[0]
    expense_ratios.append(ratio)
  return (expense_ratios, company_names, asset_class)