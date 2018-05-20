from pandas import read_csv
from datetime import datetime as dt


def tick_data_datetime_parser(date, time):
    return dt.strptime(date + time, '%m/%d/%Y%H:%M:%S.%f')

quotes = read_csv('ES_Quotes.csv', parse_dates={'Timestamp': ['Date', 'Time']},
                  index_col=('Symbol', 'Timestamp'),
                  date_parser=tick_data_datetime_parser)

quotes.to_pickle('quotes.pickle')
