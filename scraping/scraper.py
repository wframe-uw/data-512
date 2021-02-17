from bs4 import BeautifulSoup
import re
import json
import requests


class scraper():

    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.url_stats = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(self.ticker, self.ticker)
        self.url_stats = "https://finance.yahoo.com/quote/{}/profile?p={}".format(self.ticker, self.ticker)
        self.url_financials = "https://finance.yahoo.com/quote/{}/financials?p={}".format(self.ticker, self.ticker)

    def get_data(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')
        pattern = re.compile(r'\s--\sData\s--\s')
        script_data = soup.find('script', text=pattern).contents[0]
        start_pos = script_data.find("context") - 2
        end_pos = -12
        json_data = json.loads(script_data[start_pos: end_pos])
        data = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']
        return data
