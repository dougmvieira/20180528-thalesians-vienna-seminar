import pandas_datareader.data as web


web.DataReader('CHRIS/CME_ES1', # Continuous front-month E-mini S&P500
               'quandl', '2013-09-01', '2018-05-18'
               ).to_pickle('daily_prices.pickle')
