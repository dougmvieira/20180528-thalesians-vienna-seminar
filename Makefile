all: prices.pickle

ES_Sample.zip:
	wget https://s3-us-west-2.amazonaws.com/tick-data-s3/downloads/ES_Sample.zip

ES_Quotes.csv: ES_Sample.zip
	unzip -u ES_Sample.zip ES_Quotes.csv

quotes.pickle: parse_csv.py ES_Quotes.csv
	python3 parse_csv.py

daily_prices.pickle: quandl_fetcher.py
	python3 quandl_fetcher.py

prices.pickle: price_merger.py quotes.pickle daily_prices.pickle
	python3 price_merger.py
