def expenseRatioAnnual(exp_ratio, prices):
  expense_amount = 0
  for x,p in zip(exp_ratio, prices):
    expense_amount += (float(x[:-1])/100) * p
  return expense_amount