import pandas as pd


tickdata_start = pd.to_datetime('2013-09-01 17:00:00')
tickdata_end = pd.to_datetime('2013-09-20 16:15:00')

dailydata_start = pd.to_datetime('2013-09-23 16:15:00')
dailydata_end = pd.to_datetime('2018-05-18 16:15:00')

closing_time = pd.to_timedelta('16:15:00')
