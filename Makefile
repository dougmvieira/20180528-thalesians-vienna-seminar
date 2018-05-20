all: quotes.pickle

ES_Sample.zip:
	wget https://s3-us-west-2.amazonaws.com/tick-data-s3/downloads/ES_Sample.zip

ES_Quotes.csv: ES_Sample.zip
	unzip -u ES_Sample.zip ES_Quotes.csv

quotes.pickle: parse_csv.py ES_Quotes.csv
	python3 parse_csv.py
