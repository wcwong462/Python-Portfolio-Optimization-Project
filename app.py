import pandas as pd
import yfinance as yf
import datetime as dt
import numpy as np
from fredapi import Fred
from scipy.optimize import minimize
import tkinter as tk
from tkinter import messagebox, scrolledtext

def fetch_data(tickers, start_date, end_date):
    close_df = pd.DataFrame()
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            if not data.empty:
                close_df[ticker] = data['Close']
            else:
                print(f"No data found for {ticker}. It may be delisted or unavailable.")
        except Exception as e:
            print(f"Error downloading {ticker}: {e}")
    return close_df

def portfolio_optimization(tickers):
    fred = Fred(api_key='93caef823fe2dd6e2e1858fdd49cf038')
    ten_year_rate = fred.get_series('GS10') / 100
    rf = ten_year_rate.mean()

    end_date = dt.datetime.today()
    start_date = end_date - dt.timedelta(days=5 * 365)

    close_df = fetch_data(tickers, start_date, end_date)

    if close_df.empty:
        return "No valid data available for the provided tickers."

    log_return = np.log(close_df / close_df.shift(1)).dropna()
    cov_matrix = log_return.cov() * 252

    def portfolio_deviation(weights, cov_matrix):
        return np.sqrt(weights.T @ cov_matrix @ weights)

    def portfolio_return(weights, log_return):
        return np.sum(log_return.mean() * weights) * 252

    def neg_portfolio_sharpe_ratio(weights, log_return, rf, cov_matrix):
        return -(portfolio_return(weights, log_return) - rf) / portfolio_deviation(weights, cov_matrix)

    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(len(tickers)))
    initial_weights = np.array([1 / len(tickers)] * len(tickers))

    optimize_result = minimize(neg_portfolio_sharpe_ratio, initial_weights, args=(log_return, rf, cov_matrix), method='SLSQP', bounds=bounds, constraints=constraints)

    if optimize_result.success:
        optimize_weights = optimize_result.x
        expected_return = portfolio_return(optimize_weights, log_return)
        expected_volatility = portfolio_deviation(optimize_weights, cov_matrix)
        sharpe_ratio = (expected_return - rf) / expected_volatility
        
        result = "Optimized Portfolio Weights:\n"
        for ticker, weight in zip(tickers, optimize_weights):
            result += f"{ticker}: {weight:.2%}\n"
        result += f"\nExpected Annual Return: {expected_return:.2%}\n"
        result += f"Expected Annual Volatility: {expected_volatility:.2%}\n"
        result += f"Sharpe Ratio: {sharpe_ratio:.2f}"
        
        return result
    else:
        return "Optimization failed."

def on_optimize_button_click():
    user_input = entry_tickers.get()
    if not user_input:
        messagebox.showwarning("Input Error", "Please enter at least one ticker.")
        return
    
    tickers = [ticker.strip() for ticker in user_input.split(',')]
    result = portfolio_optimization(tickers)
    output_text.delete(1.0, tk.END)  # Clear previous output
    output_text.insert(tk.END, result)

# Create the main application window
app = tk.Tk()
app.title("Portfolio Optimization")
app.geometry("400x400")

# Create and place the widgets
label = tk.Label(app, text="Enter ETF/Stock Tickers (comma-separated):")
label.pack(pady=10)

entry_tickers = tk.Entry(app, width=50)
entry_tickers.pack(pady=10)

optimize_button = tk.Button(app, text="Optimize Portfolio", command=on_optimize_button_click)
optimize_button.pack(pady=20)

output_text = scrolledtext.ScrolledText(app, width=48, height=10)
output_text.pack(pady=10)

# Start the GUI event loop
app.mainloop()
