import requests
class Requester:
    def get_page_text(self, url):
        return requests.get(url).text