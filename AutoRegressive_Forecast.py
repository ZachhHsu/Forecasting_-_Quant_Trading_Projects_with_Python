# Homework 8. Predict stock prices in the next FOUR days (from Feb 1, 2022) using AR(2), AR(5) and AR(8)
# Also need to plot all stock price predictions in one chart.

import numpy as np
import yfinance as yf
import statsmodels.tsa.ar_model as sm
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

mydata = yf.download('TSLA','2022-01-01', '2022-02-01')
price_data = mydata['Adj Close']
print('Last Prince on', price_data.index[-1], '=', price_data[-1])
future_day = price_data.index[-1]+ np.timedelta64(1,'D')

# +++ Your Code Below +++ 
# First, use the past daily price to estimate (fit) the model
my_model_fit = sm.AutoReg(price_data, lags=2).fit()
# Next, predict the price for the subsequent 4 days
ar2_forecasts = my_model_fit.predict(len(price_data), len(price_data)+3)
# Finally, append 'ar2_forecasts' to the existing daily prices series: 'price_data'
p_ar2 = np.append(price_data, ar2_forecasts)
print('AR(2) predicts from', future_day, '=', p_ar2[-4:])
# +++ Your Code Above +++

# Autoregressive model: AR(5) predicts prices for the next 4 days
# +++ Your Code Below +++ 
my_model_fit = sm.AutoReg(price_data, lags=5).fit()
ar5_forecasts = my_model_fit.predict(len(price_data), len(price_data)+3)
p_ar5 = np.append(price_data, ar5_forecasts)
print('AR(5) predicts from', future_day, '=', p_ar5[-4:])
# +++ Your Code Above +++

# Autoregressive model: AR(8) predicts prices for the next 4 days
# +++ Your Code Below +++ 
my_model_fit = sm.AutoReg(price_data, lags=8).fit()
ar8_forecasts = my_model_fit.predict(len(price_data), len(price_data)+3)
p_ar8 = np.append(price_data, ar8_forecasts)
print('AR(8) predicts from', future_day, '=', p_ar8[-4:])
# +++ Your Code Above +++

t_values = price_data.index.values
last_day = t_values[-1]

# Generate 4 future dates and append them to the end of the existing dates
# +++ Your Code Below +++ 
day_plus_1 = last_day + np.timedelta64(1, 'D')
day_plus_2 = last_day + np.timedelta64(2, 'D')
day_plus_3 = last_day + np.timedelta64(3, 'D')
day_plus_4 = last_day + np.timedelta64(4, 'D')
t_values_new = np.append(t_values, [day_plus_1, day_plus_2, day_plus_3, day_plus_4])
# +++ Your Code Above +++

# Download the prices of What actully happened in the subsequent 4 days
p_actual = yf.download('TSLA','2022-01-01', '2022-02-05')['Adj Close'].to_numpy()
print('Actual prices ', p_actual[-4:])

# Can you plot the prices using AR(2), AR(5) and AR(8)?
# +++ Your Code Below +++ 
plt.plot(t_values_new, p_ar2, color='green', label='AR(2)')
plt.plot(t_values_new, p_ar5, color='blue', label='AR(5)')
plt.plot(t_values_new, p_ar8, color='yellow', label='AR(8)')
plt.plot(t_values_new, p_actual, color='red', marker='o', label='Actual')
# +++ Your Code Above +++

plt.tick_params(axis='x', rotation=20)
plt.legend(loc='upper left')
plt.show()
