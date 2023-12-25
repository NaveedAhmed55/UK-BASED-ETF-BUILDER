import math
def getNumberOfEtf(amount):
  num_portfolios = {
    (1, 5000):5,
    (5001, 20000):10,
    (20001, math.inf): 15
  }
  no_etfs = 0
  for k in num_portfolios:
    if amount>=k[0] and amount<=k[1]:
      no_etfs = num_portfolios[k]
  return no_etfs