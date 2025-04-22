import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Define stocks and bonds to include in the mutual fund portfolio
stocks = ["SPY", "AAPL", "MSFT"]  # S&P 500 ETF, Apple, Microsoft (Equities)
bonds = ["TLT", "LQD"]  # TLT: 20+ Year Treasury Bond ETF, LQD: Investment-Grade Corporate Bonds ETF
commodities = ["GLD"]


# Download historical data from Yahoo Finance
assets = stocks + bonds + commodities
data = yf.download(assets, start="2020-01-01", end="2024-01-01")["Close"]


# Compute daily returns
returns = data.pct_change().dropna()


print(returns)


# Evenly distribute portfolio weights
num_assets = len(assets)
weights = np.array([1 / num_assets] * num_assets)  # Even weights


# Calculate portfolio returns
portfolio_returns = returns @ weights


# Define Stress Test Scenarios
stress_tests = {
   "Market Crash": {"stocks": -0.30, "bonds": -0.10},
   "Interest Rate Spike": {"stocks": -0.05, "bonds": -0.05},
   "Recession Scenario": {"stocks": -0.10, "bonds": -0.05},
   "Inflation Shock": {"stocks": -0.08, "bonds": -0.06, "commodities": 0.10}  # Assume commodities gain
}


# Apply Stress Tests
stress_results = {}


for scenario, shocks in stress_tests.items():
   # Apply shocks
   stock_impact = sum(weights[i] * shocks["stocks"] for i in range(len(stocks)))
   bond_impact = sum(weights[i + len(stocks)] * shocks["bonds"] for i in range(len(bonds)))


   stressed_return = stock_impact + bond_impact
   stress_results[scenario] = stressed_return


# Display Results
print("\nStress Test Results (Even Weights):")
for scenario, result in stress_results.items():
   print(f"{scenario}: {result * 100:.2f}% expected portfolio return")


# Visualize the stress test results
plt.figure(figsize=(10, 5))
plt.plot(stress_results.keys(), stress_results.values())
plt.axhline(y=0, color="black", linestyle="--")
plt.ylabel("Portfolio Return Under Stress (%)")
plt.title("Stress Testing Portfolio (Even Weights)")
plt.show()


plt.bar(stress_results.keys(), stress_results.values())
plt.show()
