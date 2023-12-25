from scipy.optimize import minimize
import numpy as np
from portfolioApp.modules.fin_stat import sharpe_ratio, standard_deviation, expected_return, neg_sharpe_ratio
import pandas as pd
def optimized_portfolio(tickers, log_returns, cov_matrix, risk_free_rate, total_weight, min_weight):
  constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - total_weight}
  bounds = [(min_weight, 1) for _ in range(len(tickers))]
  initial_weights = np.array([total_weight/len(tickers)]*len(tickers))
  optimized_results = minimize(neg_sharpe_ratio, initial_weights, args=(log_returns, cov_matrix, risk_free_rate), method='SLSQP', constraints=constraints, bounds=bounds)
  optimal_weights = optimized_results.x
  result = {}
  if len(tickers)==1:
    optimal_weights[0] = total_weight
  result["weights"] = optimal_weights
  # result["return"] = expected_return(optimal_weights, log_returns)
  # result["volatility"] = standard_deviation(optimal_weights, cov_matrix)
  result["sharpRatio"] = sharpe_ratio(optimal_weights, log_returns, cov_matrix, risk_free_rate)
  return result