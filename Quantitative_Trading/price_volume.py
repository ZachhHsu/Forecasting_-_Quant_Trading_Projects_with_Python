# BUY signial is generated for a 'rising' price and a 'falling' volume
# SELL signial is for a 'falling' price and a 'rising' volume

import datetime as dt
import pandas as pd
import yfinance as yf

# Figure out the timing of buys/sells and trading profit for a given sma_days
def TradingStrategy(price_data, volume_data, n_day):
    # The Series of price and volume that is N-day ago 
    prior_price = price_data.shift(n_day)
    prior_volume = volume_data.shift(n_day)

    # Combine both price and SMA data and store them in a pandas' dataframe named 'price_sma_data'
    prices_volumes = pd.concat([price_data, volume_data, prior_price, prior_volume], axis=1)
    prices_volumes.columns = ['Price', 'Volume', 'Prior Price', 'Prior Volume']
    
    # Generate buy or sell signals
    buy_or_sell = 0
    buy_count = 0
    sell_count = 0

    for t in prices_volumes.index:
        today_price = prices_volumes.loc[t, 'Price']
        prior_price = prices_volumes.loc[t, 'Prior Price']
        today_volume = prices_volumes.loc[t, 'Volume']
        prior_volume = prices_volumes.loc[t, 'Prior Volume']
  
        # BUY is -1 due to cash outflow and SELL is +1 due to cash inflow     
        if today_price > prior_price and today_volume < prior_volume:
            buy_or_sell = -1
            buy_count = buy_count + 1
        elif today_price < prior_price and today_volume > prior_volume:
            buy_or_sell = 1
            sell_count = sell_count + 1
        else:
            buy_or_sell = 0

        # When it is the final day in the entire sample period
        if t == prices_volumes.index[-1]:
            # Add trades to have equal numbers of buy and sell
            Additional_trade = buy_count - sell_count
            buy_or_sell = buy_or_sell + Additional_trade    
    
        prices_volumes.loc[t, 'Buy or Sell'] = buy_or_sell
        # Calcualte the cash flow for each trade
        cash_flow = today_price * buy_or_sell
        prices_volumes.loc[t, 'Cash Flow'] = cash_flow
    
    # Calculate total P&Ls
    trading_profit = prices_volumes['Cash Flow'].sum(axis=0)
    return prices_volumes, trading_profit

# For a given ticker and date range, loop thru different SMA days to find out the best N-day SMA
my_data = yf.download('GS', '2022-01-01', '2022-03-15')
price_data = my_data['Adj Close']
volume_data = my_data['Volume']

# Find the highest profits and its associated prior N-day
best_profit = 0
best_n_day = 0
best_trades = pd.DataFrame()
for n_day in range(1, 10):
    # Find what the highest profit is, how many prior-days price and volume have differences, and what the individual trades are
    my_trades, my_trading_profit = TradingStrategy(price_data, volume_data, n_day)
    print('N Prior ', n_day, 'Days: Profit =', my_trading_profit)
    if my_trading_profit > best_profit:
        best_profit = my_trading_profit
        best_n_day = n_day
        best_trades = my_trades   

print()
print('Best profit = $' + str(format(best_profit,'5.2f')) + ' for ' + str(best_n_day) + '-day prior price and volume')
print()

# Print all trades of BUY or SELL
for t in best_trades.index:
    buy_or_sell = best_trades.loc[t, 'Buy or Sell']
    price = best_trades.loc[t, 'Price']
    if buy_or_sell < 0:
        print(t.strftime('%Y-%m-%d'), ' BUY ', int(abs(buy_or_sell)), 'shares $', format(price,'5.2f'))
    elif buy_or_sell > 0:
        print(t.strftime('%Y-%m-%d'), ' SELL ', int(abs(buy_or_sell)), 'shares $', format(price,'5.2f'))
