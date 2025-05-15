import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


# Define stocks and bonds to include in the mutual fund portfolio
stocks = ['AAPL',  'MSFT', 'AMZN', 'GOOGL', 'NVDA',
         'TSLA', 'WMT', 'META', 'UNH', 'JNJ',
          'JPM', 'V', 'PG', 'XOM', 'LLY',
         'AVGO', 'MA', 'PEP', 'DIS', 'KO',
         'COST', 'HD', 'CSCO', 'PFE', 'BA',
         'AMD', 'PANW', 'SHOP', 'ZM', 'CAR',
         'ROKU', 'DKNG', 'DOCU', 'ALB', 'MDB',
         'ETSY', 'U', 'NET', 'SNOW', 'PLUG',
         'BABA', 'TCEHY', 'BIDU', '005930.KQ', 'TSM',
         'INFY', 'RELIANCE.NS', 'MELI', 'PBR', 'VALE',
         'NPSNY', '2222.SR', 'SIEGY', 'SAP', 'ASML',
         'NSRGY', 'UL', 'TM', '8058.T', 'SONY'
         ]  # Stocks only #


bonds = ['EMB', 'VWOB', 'EBND', 'LEMB', 'PCY',
         'IDR', 'CL', 'PH', 'INR', 'TR',
         'VCIT', 'SPAB', 'SCHZ', 'CRED', 'VCLT',
         'BND', 'IGLB', 'LQD', 'IGF', 'BNDX',
         '^IRX', '^FVX', '^TNX', 'SPYB', '^TYX',
         'IEF', 'TLH', 'FLOT', 'FNMA', 'TLT']  # Bonds only #


commodities = ['GLD', 'SLV', 'DBC', 'USO', 'MOO',
         'UNG', 'COPX', 'WEAT', 'PALL', 'IAU'
              ] # Commodities only (other equities such as real estate may be included based on your own judgment $


# Download historical data from Yahoo Finance
assets = stocks + bonds + commodities
years = 10




endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(365*years)
data = yf.download(assets, start=startDate, end=endDate)["Close"]


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
   "Market Crash": {"stocks": -0.30, "bonds": -0.10, "commodities": 0},
   "Interest Rate Spike": {"stocks": -0.05, "bonds": -0.05, "commodities": 0},
   "Recession Scenario": {"stocks": -0.10, "bonds": -0.05, "commodities": 0.05},
   "Inflation Shock": {"stocks": -0.08, "bonds": -0.06, "commodities": 0.10}  # Assume commodities gain
}


# Apply Stress Tests
stress_results = {}


for scenario, shocks in stress_tests.items():
   # Apply shocks
   stock_impact = shocks["stocks"] * sum(weights[:len(stocks)])
   bond_impact = shocks["bonds"] * sum(weights[len(stocks):len(stocks) + len(bonds)])
   commodity_impact = shocks["commodities"] * sum(weights[len(stocks) + len(bonds):])


   stressed_return = stock_impact + bond_impact + commodity_impact
   stress_results[scenario] = stressed_return


# Display Results
print("\nStress Test Results (Even Weights):")
for scenario, result in stress_results.items():
   print(f"{scenario}: {result * 100:.2f}% expected portfolio return")


# Visualize the stress test results, but not really needed #
plt.figure(figsize=(10, 5))
plt.plot(stress_results.keys(), stress_results.values())
plt.axhline(y=0, color="black", linestyle="--")
plt.ylabel("Portfolio Return Under Stress (%)")
plt.title("Stress Testing Portfolio (Even Weights)")
plt.show()
