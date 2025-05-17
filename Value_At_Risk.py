import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import norm


# Define weights as a dictionary
weights_dict = {'AAPL': 0.01, 'TSLA': 0.99}


# Create the list of tickers from the dictionary keys (ensures correct order)
tickers = list(weights_dict.keys())


# Convert weights to a NumPy array in the same order as tickers
weights = np.array([weights_dict[ticker] for ticker in tickers])


# Check that weights sum to 1
if not np.isclose(np.sum(weights), 1.0):
   raise ValueError("Weights must sum to 1.")






# Set time from a certain number of years to take data from #


years = 10 # ADJUST TO YOUR DESIRED TIMEFRAME OF YFINANCE DATA #


endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(365*years)


# Create a list of tickers, stocks, bonds and commodities all together #


tickers = ['AAPL', 'TSLA']








# Retrieve the daily adjusted close prices for the tickers, accounts for dividends and stock splits #




adjclose = pd.DataFrame()




# A data frame is a 2D data structure #




for ticker in tickers:
 data = yf.download(ticker, startDate, endDate)
 adjclose[ticker] = data['Close']




# Now we have the close prices in the data frame! #




# Calculate the daily log returns (log returns are additive) #




log_returns = np.log(adjclose/adjclose.shift(1))
log_returns = log_returns.dropna()
print(log_returns)




# The shift 1 accounts for the returns from one day to another #




# Now we have log returns #




# Create a function that will be used to calculate portfolio expected return #




def expected_return(weights, log_returns):
 return np.sum(log_returns.mean()*weights)


# Create a covariance matrix #




cov_matrix = log_returns.cov()
print(cov_matrix)




# Create a function that will be used to calculate standard deviation #




def standard_deviation (weights, cov_matrix):
 variance = weights.T @ cov_matrix @ weights
 return np.sqrt(variance)




# weights.T is the transpose of the weights vector, and "@" is matrix multiplication #




# Create an equally weighted portfolio and find total portfolio expecetd return and SD #




portfolio_value = 100000000


portfolio_expected_return = expected_return(weights, log_returns)
portfolio_std_dev = standard_deviation(weights, cov_matrix)




def random_z_score():
 return np.random.normal(0, 1)




# We can generate a random z score that is normally distributed because log returns are normally distributed $




# Create a function to calculate potential gain or loss over n days #




days = 30




def scenario_gain_loss(portfolio_value, portfolio_std_dev, z_score, days):
 return portfolio_value*portfolio_expected_return*days + portfolio_value*portfolio_std_dev*z_score*np.sqrt(days)




# Run 1000000 simulations #
simulations = 1000000
scenarioReturn = []




for i in range(simulations):
 z_score = random_z_score()
 scenarioReturn.append(scenario_gain_loss(portfolio_value, portfolio_std_dev, z_score, days))




# Specify a confidence interval #




confidence_interval1 = 0.99
confidence_interval2 = 0.95
confidence_interval3 = 0.90




VaR1 = -np.percentile(scenarioReturn, 100 * (1 - confidence_interval1))




VaR2 = -np.percentile(scenarioReturn, 100 * (1 - confidence_interval2))




VaR3 = -np.percentile(scenarioReturn, 100 * (1 - confidence_interval3))




print(f"At a confidence interval of {100*confidence_interval1}%, the Value at Risk is {VaR1}")
print(f"At a confidence interval of {100*confidence_interval2}%, the Value at Risk is {VaR2}")
print(f"At a confidence interval of {100*confidence_interval3}%, the Value at Risk is {VaR3}")




# Find the CVaR #




tail_losses1 = []
for x in scenarioReturn:
 if x < -VaR1:
     tail_losses1.append(x)




cvar1 = -1*np.mean(tail_losses1)




print(f"The Conditional Value at Risk, or tail loss given a {100*confidence_interval1}%, confidence interval is {cvar1}")




tail_losses2 = []
for x in scenarioReturn:
 if x < -VaR2:
     tail_losses2.append(x)




cvar2 = -1 * np.mean(tail_losses2)




print(f"The Conditional Value at Risk, or tail loss given a {100 * confidence_interval2}%, confidence interval is {cvar2}")




tail_losses3 = []
for x in scenarioReturn:
 if x < -VaR3:
     tail_losses3.append(x)




cvar3 = -1 * np.mean(tail_losses3)




print(f"The Conditional Value at Risk, or tail loss given a {100 * confidence_interval3}%, confidence interval is {cvar3}")




plt.hist(scenarioReturn, bins = 100, density = True)
plt.xlabel('Scenario Gain/Loss ($)')
plt.ylabel('Frequency')
plt.title(f'Distribution of Portfolio Gain/Loss Over {days} Days')
plt.axvline(-VaR1, color = 'r', linestyle='dashed', linewidth = 2, label = f'VaR at {100*confidence_interval1}% confidence level')
plt.axvline(-VaR2, color = 'y', linestyle='dashed', linewidth = 2, label = f'VaR at {100*confidence_interval2}% confidence level')
plt.axvline(-VaR3, color = 'b', linestyle='dashed', linewidth = 2, label = f'VaR at {100*confidence_interval3}% confidence level')




plt.legend()
plt.show()
