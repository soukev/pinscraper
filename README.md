# pinscraper
Pinterest board scraper with simple GUI viewer.

## Requirements
Selenium is used for scraping, which requires geckodriver. [Follow the instructions](https://selenium-python.readthedocs.io/installation.html#drivers) for installing driver.

## Usage
```
pip install -r requirements.txt
```
For board download use pinscrape.py script
```
python pinscrape.py -u <url of board> -s <number of scrolls> -p <number of pics>
```
For viewing run pinscrape_gui.py
```
python pinscrape_gui.py
```

## Requirements
Script and GUI app needs selenium, bs4, requests, sqlite3, PIL, tkinter. Those can be installed from pip.




