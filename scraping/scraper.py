from bs4 import BeautifulSoup
import re
import json
from scraping.clients import Requester
from scraping.constants import *

class Scraper:
    def __init__(self, ticker, requester=Requester()):
        self.ticker = ticker.upper()
        self.requester = requester
        self.url_stats = URL_KEY_STATISTICS.format(self.ticker, self.ticker)
        self.url_profile = URL_PROFILE.format(self.ticker, self.ticker)
        # self.url_financials = URL_FINANCIALS.format(self.ticker, self.ticker)
        self.financials_dict = {}
        self.profile_dict = {}
        self.sec_filing_list = []

    def parse_url(self, url):
        text = self.requester.get_page_text(url)
        soup = BeautifulSoup(text, 'lxml')
        pattern = re.compile(r'\s--\sData\s--\s')
        script_data = soup.find('script', text=pattern).contents[0]
        start_pos = script_data.find("context") - 2
        end_pos = -12
        json_loads = json.loads(script_data[start_pos: end_pos])
        json_data = json_loads['context']['dispatcher']['stores']['QuoteSummaryStore']
        return json_data

    def add_to_data_dict(self, dict):
        for key, val in dict.items():
            try:
                self.financials_dict[key] = val['fmt']
            except (KeyError, TypeError):
                continue

    def add_key_stats_to_dict(self):
        stats_data = self.parse_url(self.url_stats)
        tables_to_scrape = ['financialData', 'summaryDetail', 'defaultKeyStatistics', 'price', 'calendarEvents']
        for table in tables_to_scrape:
            self.add_to_data_dict(stats_data[table])

    def add_profile_to_dict(self):
        profile_data = self.parse_url(self.url_profile)
        self.scrape_company_description(profile_data)
        self.scrape_sec_filling(profile_data)

    def scrape_company_description(self, profile_data):
        asset_profile = profile_data['assetProfile']
        profile_fields_to_include = ['sector', 'industry', "longBusinessSummary"]
        for field in profile_fields_to_include:
            self.profile_dict[field] = asset_profile.get(field)

    def scrape_sec_filling(self, profile_data):
        try:
            sec_filings = profile_data['secFilings']['filings']
            n = min(3, len(sec_filings))
            sec_fields_to_include = ['date', 'type', 'title', 'edgarUrl']
            if sec_filings:
                for i in range(n):
                    temp_filing_dict = {}
                    for field in sec_fields_to_include:
                        temp_filing_dict[field] = sec_filings[i].get(field)
                    self.sec_filing_list.append(temp_filing_dict)
        except (KeyError, TypeError):
            pass

    def scrape_all_data(self):
        self.add_key_stats_to_dict()
        self.add_profile_to_dict()
        return {'profile': self.profile_dict, 'financials': self.financials_dict, 'sec_filings': self.sec_filing_list}


if __name__ == "__main__":
    s = Scraper('ECL')
    data = s.scrape_all_data()
    print(data["profile"])
    print(data["financials"])
    print(len(data["financials"]))
    print(data['sec_filings'])