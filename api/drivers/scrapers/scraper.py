from time import sleep

from lxml import html
import requests

from utils.mixins.mode import ModeMixin


SCRAPER_ID = "Sonical Scraper 1.0 (jonathan@ardent.tech)"


class Scraper(ModeMixin, object):

    def get_tree(self, url):
        sleep(1)
        page = requests.get(url, headers={"user-agent": SCRAPER_ID})
        return html.fromstring(page.content)

    def run(self, path):
        raise Exception("Sub-classes of Scraper must implement `run(self, path)`")
