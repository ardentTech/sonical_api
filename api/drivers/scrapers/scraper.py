from time import sleep

from django.conf import settings

from lxml import html
import requests


SCRAPER_ID = "Sonical Scraper 1.0 (jonathan@ardent.tech)"


class Scraper(object):

    DEV_MODE = "dev"
    PRO_MODE = "pro"

    def __init__(self):
        self.mode = self.DEV_MODE if settings.DEBUG is True else self.PRO_MODE

    def dev_mode(self):
        return self.mode == self.DEV_MODE

    def get_tree(self, url):
        sleep(1)
        page = requests.get(url, headers={"user-agent": SCRAPER_ID})
        return html.fromstring(page.content)

    def pro_mode(self):
        return self.mode == self.PRO_MODE

    def run(self, path):
        raise Exception("Sub-classes of Scraper must implement `run(self, path)`")
