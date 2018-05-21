import pandas as pd


def drop_consecutive(s):
    return s[(s != s.shift()) & ~(s.isnull() & s.isnull().shift())]

quotes = pd.read_pickle('quotes.pickle')
daily_prices = pd.read_pickle('daily_prices.pickle')

closing_time = pd.to_timedelta('16:15:00')
daily_prices.index += closing_time

mids = drop_consecutive(quotes[['Bid Price', 'Ask Price']].mean(axis=1))

rolling_contract_adjust = (daily_prices.loc['2013-09-13', 'Open'].values[0]
                           - daily_prices.loc['2013-09-12', 'Last'].values[0]
                           - mids.loc['ESZ13'].values[0]
                           + mids.loc['ESU13'].values[-1])

pd.concat([mids.loc['ESU13'],
           mids.loc['ESZ13'] + rolling_contract_adjust,
           daily_prices.loc[:'2013-09-23', 'Last']]
          ).to_pickle('prices.pickle')
