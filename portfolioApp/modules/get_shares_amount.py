def get_shares_amount(prices, weights, amount):
  total_amount = []
  no_shares = []
  for i in range(len(prices)):
    price = prices[i]
    t_amount = amount * weights[i]
    n_shares = int(round(t_amount/price))
    no_shares.append(n_shares)
    total_amount.append(n_shares * price)
  return no_shares, total_amount