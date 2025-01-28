# Portfolio Optimization Project

## Overview

This project implements a portfolio optimization model to maximize the Sharpe ratio for a diversified investment portfolio. Utilizing historical price data for selected ETFs, it calculates optimal asset weights to achieve an efficient balance between expected return and risk.

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

```bash
pip install pandas yfinance fredapi scipy
