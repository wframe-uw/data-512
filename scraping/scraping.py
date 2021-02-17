import pandas as pd
from bs4 import BeautifulSoup
import re
import json
import requests

url_stats = "https://finance.yahoo.com/quote/{}/key-statistics?p={}"
url_profile = "https://finance.yahoo.com/quote/{}/profile?p={}"
url_financials = "https://finance.yahoo.com/quote/{}/financials?p={}"
stock = 'AAPL'
url = url_financials.format(stock, stock)

page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
pattern = re.compile(r'\s--\sData\s--\s')
script_data = soup.find('script', text=pattern).contents[0]

# print(script_data)
start_pos = script_data.find("context") - 2
end_pos = -12
json_data = json.loads(script_data[start_pos : end_pos])
profile_data = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']
summary_data = profile_data['summaryDetail']


summary_stats = {}

for key, val in summary_data.items():
    try:
        summary_stats[key] = val['fmt']
    except (KeyError, TypeError):
        continue

print(summary_stats)


