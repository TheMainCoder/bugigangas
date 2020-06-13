#! python3
# getStockPrice.py - Gets stock price from Yahoo Finance
# Usage: getStockPrice.py PETR4.SA
import re
import sys
import requests
from bs4 import BeautifulSoup
if len(sys.argv) > 1:
    pattern = re.compile('(\d+.\d+)</span>') # Pattern found
    page = requests.get('https://finance.yahoo.com/quote/'+sys.argv[1]+'?p='+sys.argv[1]+'&.tsrc=fin-srch')
    soup = BeautifulSoup(page.content, 'html.parser')
    spans = soup.select('#quote-header-info span')
    for span in spans:
        m = pattern.search(str(span))
        if m:
            price = m.group(1)
            print(price)
