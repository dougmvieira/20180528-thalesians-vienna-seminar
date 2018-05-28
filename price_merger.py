import pandas as pd
from parameters import (tickdata_start, tickdata_end,
                        dailydata_start, dailydata_end)


def drop_consecutive(s):
    return s[(s != s.shift()) & ~(s.isnull() & s.isnull().shift())]

quotes = pd.read_pickle('quotes.pickle')
daily_prices = pd.read_pickle('daily_prices.pickle')

mids = drop_consecutive(quotes[['Bid Price', 'Ask Price']].mean(axis=1))

rolling_contract_adjust = (daily_prices.loc['2013-09-13', 'Open'].values[0]
                           - daily_prices.loc['2013-09-12', 'Last'].values[0]
                           - mids.loc['ESZ13'].values[0]
                           + mids.loc['ESU13'].values[-1])

prices = pd.concat([mids.loc['ESU13'],
                    mids.loc['ESZ13'] + rolling_contract_adjust,
                    daily_prices.loc[dailydata_start:, 'Last']])
prices.index.name = 'Time'

prices.to_pickle('prices.pickle')
