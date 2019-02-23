import pandas_datareader.data as web
from parameters import tickdata_start, dailydata_end, closing_time


quandl_key = input("Please insert your Quandl API Key: ")

# Continuous front-month E-mini S&P500
daily_prices = web.DataReader('CHRIS/CME_ES1', 'quandl',
                              tickdata_start.date(), dailydata_end.date(),
                              access_key=quandl_key)

daily_prices.index += closing_time
daily_prices.sort_index(inplace=True)

daily_prices.to_pickle('daily_prices.pickle')
