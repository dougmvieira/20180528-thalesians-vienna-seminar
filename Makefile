all: MicrostructureOfOptionPrices.html

ES_Sample.zip:
	wget https://s3-us-west-2.amazonaws.com/tick-data-s3/downloads/ES_Sample.zip

ES_Quotes.csv: ES_Sample.zip
	unzip -u ES_Sample.zip ES_Quotes.csv

quotes.pickle: parse_csv.py ES_Quotes.csv
	python3 parse_csv.py

daily_prices.pickle: quandl_fetcher.py parameters.py
	python3 quandl_fetcher.py

prices.pickle: price_merger.py parameters.py quotes.pickle daily_prices.pickle
	python3 price_merger.py

simulation.pickle: heston_simulation.py parameters.py
	python3 heston_simulation.py

reveal.js:
	wget https://github.com/hakimel/reveal.js/archive/master.tar.gz
	tar -xzvf master.tar.gz
	mv reveal.js-master reveal.js

MicrostructureOfOptionPrices.html: MicrostructureOfOptionPrices.md reveal.js
	pandoc -s -t revealjs --toc --toc-depth=1 -o MicrostructureOfOptionPrices.html MicrostructureOfOptionPrices.md
