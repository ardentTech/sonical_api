from time import sleep

from lxml import html
import requests


SCRAPER_ID = "Sonical Scraper 1.0 (jonathan@ardent.tech)"


class Scraper(object):

    def run(self, path):
        raise Exception("Sub-classes of Scraper must implement `run(self, path)`")

    def _get_tree(self, url):
        headers = {"user-agent": SCRAPER_ID}
        page = requests.get(url, headers=headers)
        tree = html.fromstring(page.content)
        sleep(1)
        return tree
