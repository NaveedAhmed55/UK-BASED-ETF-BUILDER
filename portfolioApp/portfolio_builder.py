from portfolioApp.modules.convert_currency import convert_currency
from portfolioApp.modules.getDf import getDf
from portfolioApp.modules.getNumberOfEtf import getNumberOfEtf
from portfolioApp.modules.getPortfolios import getPortfolios
from portfolioApp.modules.sharpRatioAndVaR import sharpRatioAndVaR
from portfolioApp.modules.get_expense_ratio import get_expense_ratio
from portfolioApp.modules.get_shares_amount import get_shares_amount
from portfolioApp.modules.expenseRatioAnnual import expenseRatioAnnual
from portfolioApp.modules.divident import divident
from portfolioApp.modules.returns import returns
from portfolioApp.modules.pie_chart import pie_chart
from portfolioApp.modules.get_category_freq import get_category_freq
import pandas as pd
import numpy as np
df = getDf()
def getOptPortfolio(amount, years, risk_level, category_div):
  # return ({'list': zip(['PHDG', 'FAIL', 'SLVP', 'FTAG', 'VEGI'], ['0.39%', '0.71%', '0.39%', '0.70%', '0.39%'])})
  print("minimum adj value ", min(df["adj_close"]))
  # print(df)
  no_etfs = getNumberOfEtf(amount)
  b_amount = amount
  amount = convert_currency(amount, 'GBP', 'USD')
  
  data = df.loc[df["adj_close"]<=amount]
  r_portfolio = None
  sharpRatioAndVaRs = []
  while True:
    portfolios = getPortfolios(no_etfs, df)
    
    # print("portfolios ", portfolios)
    count = 0
    for portfolio in portfolios:
      # print("portfolio ",portfolio)
      try:
        portfolio = sharpRatioAndVaR(amount, years, portfolio, category_div, get_category_freq(no_etfs))
        print("after sharpRatioAndVaR ")
        prices = [df.loc[df["symbol"]==x, "adj_close"].values[0] for x in portfolio["etfs"]]
        print("after price")
        portfolio["price"] = [convert_currency(x, 'USD', 'GBP') for x in prices]
        print("after convert")
        portfolio["no_shares"], portfolio["total_amount"] = get_shares_amount(portfolio["price"], portfolio["weights"], b_amount)
        print("after get_shares_amount")
        nonZeroETFs = len([x for x in portfolio["no_shares"] if x > 0])
        print("after nonZeroETFs")
        if nonZeroETFs == no_etfs:
          sharpRatioAndVaRs.append(portfolio)
          print("Success on ", count)
        else:
          print("Fail on ", count)
        count = count + 1
      except:
        print("Error on ", count)
        pass
    if len(sharpRatioAndVaRs) > 0:
      break
  # print("sharpRatioAndVaRs ", sharpRatioAndVaRs)
  #sharpRatioAndVaRs.sort(key=lambda portfolio:portfolio['count'], reverse=True)
  
  risk_amount = risk_level * amount
  
  # print("risk_amount ", risk_amount)
  #backup_sr = sharpRatioAndVaRs
  
  print("sharpRatioAndVaRs ", sharpRatioAndVaRs)
  sharpRatioAndVaRs.sort(key=lambda portfolio:portfolio['sharpRatio'], reverse=True)
  print("optimum portfolio ",sharpRatioAndVaRs[0])

  #sharpRatioAndVaRs = [x for x in sharpRatioAndVaRs if x["VaR"] <= risk_amount]
  # print("backup_sr ", backup_sr)
  # print("sharpRatioAndVaRs ", sharpRatioAndVaRs)
  
  r_portfolio = pd.DataFrame(sharpRatioAndVaRs[0])
  r_portfolio["exp_ratio"], r_portfolio["company"], r_portfolio["asset_class"] = get_expense_ratio(r_portfolio["etfs"], df)
  total_spent = sum(r_portfolio["total_amount"])
  divident_amount = convert_currency(divident(r_portfolio["etfs"], r_portfolio["no_shares"]), 'USD', 'GBP')
  expense_ratio_annual = expenseRatioAnnual(r_portfolio["exp_ratio"], r_portfolio["total_amount"])
  # print("before round", obj["price"])
  r_portfolio["price"] = np.round(r_portfolio["price"], 2)
  r_portfolio["total_amount"] = np.round(r_portfolio["total_amount"], 2)
  temp = ["£"] * len(r_portfolio["price"])
  # print("after round", obj["price"])
  pie_df = r_portfolio[["asset_class", "total_amount"]]
  r_portfolio["price"] = r_portfolio["price"].astype(str) + pd.Series(temp)
  r_portfolio["total_amount"] = r_portfolio["total_amount"].astype(str) + pd.Series(temp)
  print("data r_portfolio ", r_portfolio)
  # print("temp", temp)
  return {"list": zip(r_portfolio["etfs"], r_portfolio["company"], r_portfolio["asset_class"], r_portfolio["exp_ratio"],r_portfolio["price"], r_portfolio["no_shares"], r_portfolio["total_amount"]),
          "one_week_return": returns(r_portfolio["etfs"], 7),
          "one_month_return":returns(r_portfolio["etfs"], 28),
          "one_year_return":returns(r_portfolio["etfs"], 365),
          "five_year_return":returns(r_portfolio["etfs"], 5*365),
          "divident_amount":str(np.round(divident_amount, 2))+"£",
          "total_spent": str(np.round(total_spent, 2))+"£",
          "divident_yeild": str(np.round(divident_amount*100/total_spent, 2))+"%",
          "expense_ratio_annual_amount":str(np.round(expense_ratio_annual, 2))+"£",
          "expense_ratio_annual_per":str(np.round(expense_ratio_annual*100/total_spent, 2))+"%",
          "image_uri": pie_chart(pie_df, total_spent)
          }
