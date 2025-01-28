import pandas as pd
import yfinance as yf
import datetime as dt
import numpy as np
from fredapi import Fred
from scipy.optimize import minimize

tickers = ['SPY', 'BND', 'GLD', 'QQQ', 'VTI']

fred = Fred(api_key='93caef823fe2dd6e2e1858fdd49cf038')
ten_year_rate = fred.get_series('GS10') / 100
rf = ten_year_rate.mean()

end_date = dt.datetime.today()
start_date = end_date - dt.timedelta(days = 5 * 365)

close_df = pd.DataFrame()

for ticker in tickers:
    data = yf.download(ticker, start = start_date, end = end_date)
    close_df[ticker] = data['Close']
    
log_return = np.log(close_df/close_df.shift(1)).dropna()
cov_matrix = log_return.cov()*252

def portfolio_deviation(weights, cov_matrix):
    return np.sqrt(weights.T @ cov_matrix @ weights)

def portfolio_return(weights, log_return):
    return np.sum(log_return.mean() * weights) * 252

def neg_portfolio_sharpe_ratio(weights, log_return, rf, cov_matrix):
    return -(portfolio_return(weights, log_return) - rf) / portfolio_deviation(weights, cov_matrix)

constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bounds = tuple((0, 1) for x in range(len(tickers)))

initial_weights = np.array([1/len(tickers)]*len(tickers))

optimize_result = minimize(neg_portfolio_sharpe_ratio, initial_weights, args=(log_return, rf, cov_matrix), method='SLSQP', bounds=bounds, constraints = constraints)
optimize_weights = optimize_result.x

print("Optimized Portfolio Weights:")
for ticker, weight in zip(tickers, optimize_weights):
    print(f"{ticker}: {weight:.2%}")

expected_return = portfolio_return(optimize_weights, log_return)
expected_volatility = portfolio_deviation(optimize_weights, cov_matrix)
sharpe_ratio = (expected_return - rf) / expected_volatility

print(f"\nExpected Annual Return: {expected_return:.2%}")
print(f"Expected Annual Volatility: {expected_volatility:.2%}")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
