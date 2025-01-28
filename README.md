# Portfolio Optimization Project

## Overview

This project implements a portfolio optimization model aimed at maximizing the Sharpe ratio for a diversified long-only investment portfolio. It calculates optimal asset weights to achieve an efficient balance between expected return and risk by utilising historical price data for selected ETFs.

## Technologies Used

- **Python**: The primary programming language used for data analysis and modeling.
- **Libraries**:
  - pandas: For data manipulation and analysis.
  - yfinance: To retrieve historical market data.
  - numpy: For numerical calculations.
  - fredapi: To access economic data from the Federal Reserve.
  - scipy: For optimization routines.

## Key Concepts

- **Portfolio Theory**: The project applies modern portfolio theory to determine an optimal asset allocation.
- **Sharpe Ratio**: The model maximizes the Sharpe ratio to improve risk-adjusted returns.
- **Log Returns**: It utilizes log returns to represent asset performance accurately.

## Getting Started

### Prerequisites

- Python 3.x
- Libraries: Install the required libraries using pip:

###Setting Up Your Environment
- Clone the Repository (if applicable):

Obtain a FRED API Key:
Sign up for an account at FRED and request your API key.
Update the API Key in the Code:
In the main script, replace the placeholder API key with your actual API key:
fred = Fred(api_key='YOUR_API_KEY')

##Usage
Run the Application:
Execute the script in your terminal or command prompt:
bash

python portfolio_optimizer.py
Input Tickers:
Enter the stock or ETF tickers in the input field, separated by commas (e.g., AAPL, MSFT, GOOG).
Optimize Portfolio:
Click the "Optimize Portfolio" button to initiate the optimization process.
View Results:
The output area will display the optimized asset weights, expected annual return, volatility, and Sharpe ratio.

##Acknowledgments
Yahoo Finance API: For providing historical market data.
FRED API: For offering economic data and indicators.
Tkinter: For creating the graphical user interface.
