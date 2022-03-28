# Homework 6: Find SMA Trading Strategy but the buy/sell signial is generated
# if 5-day moving average of volume is higher than 10-day moving average of volume
# When the 5-day VOLUME SMA crosses above the 10-day VOLUME SMA --> BUY
# When the 5-day VOLUME SMA crosses below the 10-day VOLUME SMA --> SELL
# Calculate the total profits using the MA Crossover trading strategy of VOLUME (not price)

import pandas as pd
import numpy as np

# Read the AAPL price and volume in a CSV file
mydata = pd.read_excel('AAPL.xls',sheet_name='AAPL', index_col=0)
price_data = mydata['Price']
volume_data = mydata['Volume']

# You need to calculate SMA of volumes (not price!!!)
# +++ Your Code Below +++ 
sma_5day = volume_data.rolling(window=5).mean()
sma_10day = volume_data.rolling(window=10).mean()
# +++ Your Code Above +++

# combine price and two volume SMAs into one dataframe
sma_data = pd.concat([price_data, volume_data, sma_5day, sma_10day], axis=1)
sma_data.columns = ['Price', 'Volume', 'SMA 5Day', 'SMA 10Day']

# You need to shift data by 1-day to store price & sma of previous-day using shift() function
# +++ Your Code Below +++
last_day_data = sma_data.shift(1)
# +++ Your Code Above +++ 

# generate buy or sell signals
buy_count = 0
sell_count = 0

for t in sma_data.index:
    today_price = sma_data.loc[t, 'Price']
    today_volume = sma_data.loc[t, 'Volume']
    # You need to get the SMA volumes for both the current day and the previous day
    # +++ Your Code Below +++
    today_sma5day = sma_data.loc[t, 'SMA 5Day']
    today_sma10day = sma_data.loc[t, 'SMA 10Day']
    last_sma5day = last_day_data.loc[t, 'SMA 5Day']
    last_sma10day = last_day_data.loc[t, 'SMA 10Day']
    # +++ Your Code Above +++ 

    # You need to generate trading signals (BUY or SELL) here
    # When 5-day Volume SMA crosses above 10-day Volume SMA --> BUY --> buy_or_sell = -1
    # When 5-day Volume SMA crosses below 10-day Volume SMA --> SELL -> buy_or_sell = +1
    # BUY is -1 due to cash outflow and SELL is +1 due to cash inflow
    # Also need to update your total numbers of buys and sells in 'buy_count' and 'sell_count'
    # +++ Your Code Below +++ 
    if today_sma5day > today_sma10day and last_sma5day < last_sma10day:
        buy_or_sell = -1
        buy_count += 1
    elif today_sma5day < today_sma10day and last_sma5day > last_sma10day:
        buy_or_sell = 1
        sell_count += 1
    else:
        buy_or_sell = 0
    # +++ Your Code Above +++ 

    # When it is the final day in the entire sample period
    if t == sma_data.index[-1]:
        # You need to add a new sell on the final day if total number of buys is greater than total number of sells
        # But if it's already sell on that day, double-selling the stock to close your positions
        # +++ Your Code Below +++
        if buy_count > sell_count:
            buy_or_sell = buy_or_sell + 1
        # +++ Your Code Above +++ 

        # You need to add a new buy on the final day if total number of buys is fewer than total number of sells
        # But if it's already buy on that day, double-buying the stock to close your positions
        # +++ Your Code Below +++
        elif buy_count < sell_count:
            buy_or_sell = buy_or_sell - 1
        # +++ Your Code Above +++ 
    
    sma_data.loc[t, 'Buy or Sell'] = buy_or_sell    
    cash_flow = today_price * buy_or_sell 
    sma_data.loc[t, 'Cash Flow'] = cash_flow

# calculate total P&Ls (Profits and Losses)
total_profit = sma_data['Cash Flow'].sum(axis=0)
print('Total P&Ls =', total_profit)
