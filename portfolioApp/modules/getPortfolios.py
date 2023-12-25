import random
from scipy.optimize import minimize
from portfolioApp.modules.get_category_freq import get_category_freq
def getPortfolios(number, df):
  NO_PORTFOLIOS = 10
  equities = df[df["category"] == "Equity"]["symbol"]
  commodities = df[df["category"] == "Commodity"]["symbol"]
  bonds = df[df["category"] == "Bonds"]["symbol"]
  real_estate = df[df["category"] == "Real Estate"]["symbol"]
  category_freq = get_category_freq(number)
  data = [equities, commodities, bonds, real_estate]
  if len(df["symbol"]) <= number:
    return [df["symbol"].tolist()]
  portfolios = []
  for i in range(NO_PORTFOLIOS):
    portfolio = []
    for i in range(len(category_freq)):
      portfolio += data[i].sample(category_freq[i]).tolist()
    portfolios.append(portfolio)
  return portfolios