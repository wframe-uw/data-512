import os
import unittest
from scraping.scraper import Scraper
from scraping.clients import Requester

TEST_TICKER = 'MSFT'
VALID_PROFILE_URL_TEXT_FILE_NAME = 'valid_profile_url_text.html'
VALID_KEY_STATISTICS_URL_TEXT_FILE_NAME = 'valid_key_statistics_url_text.html'
TEST_URL = 'https://some.url'

class TestScraper(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestScraper, self).__init__(*args, **kwargs)
        self.data_dir = os.path.join("scraping", "tests", "data")
        self.data_dir = self.data_dir if os.path.isdir(self.data_dir) else os.path.join("data")
    @staticmethod
    def get_test_requester(file_to_read_text_from):
        requester = Requester()
        with open(file_to_read_text_from, 'r') as file:
            text = file.read()
            requester.get_page_text = lambda x: text
            return requester
    @staticmethod
    def get_test_scraper(requester=Requester()):
        return Scraper(TEST_TICKER, requester)

    def test_scraper_succesfully_scrapes_valid_key_statistics_url(self):
        test_data = os.path.join(self.data_dir, VALID_KEY_STATISTICS_URL_TEXT_FILE_NAME)
        test_requester = TestScraper.get_test_requester(test_data)
        test_scraper = TestScraper.get_test_scraper(test_requester)
        test_scraper.add_key_stats_to_dict()
        self.assertTrue(test_scraper.financials_dict['grossProfits'] == '96.94B')

    def test_scraper_succesfully_scrapes_valid_profile_url(self):
        test_data = os.path.join(self.data_dir, VALID_PROFILE_URL_TEXT_FILE_NAME)
        test_requester = TestScraper.get_test_requester(test_data)
        test_scraper = TestScraper.get_test_scraper(test_requester)
        test_scraper.add_profile_to_dict()
        self.assertTrue(test_scraper.profile_dict['sector'] == 'Technology')