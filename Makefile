all: 20180528-thalesians-vienna-seminar.html

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

20180528/lob.html: lob.py bokeh_template.jinja
	mkdir -p 20180528
	python3 lob.py

20180528/sp500.html 20180528/heston.html 20180528/rounded_heston.html: sp500_plots.py prices.pickle simulation.pickle
	mkdir -p 20180528
	python3 sp500_plots.py

20180528-thalesians-vienna-seminar.html: MicrostructureOfOptionPrices.md References.bib 20180528/lob.html 20180528/sp500.html 20180528/heston.html 20180528/rounded_heston.html
	pandoc -s -c scrollable.css -t revealjs -V theme=white -V revealjs-url=. --mathjax --toc --toc-depth=1 -o 20180528-thalesians-vienna-seminar.html --bibliography References.bib MicrostructureOfOptionPrices.md
