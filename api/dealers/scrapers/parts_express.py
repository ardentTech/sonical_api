import re
from time import sleep

from lxml import html
import requests


class Scraper(object):

    SCRAPER_ID = "Sonical Scraper 1.0 (jonathan@ardent.tech)"

    def get_html(self, url):
        sleep(1)  # avoid barraging server
        page = requests.get(url, headers={"user-agent": self.SCRAPER_ID})
        return html.fromstring(page.content)

    def run(self):
        raise Exception("Scrapers must implement a `run` method.")


class DealerScraper(Scraper):
    """
    Responsible managing data, coordinating path scrapers and creating a
    DealerScraperReport.
    """

    def __init__(self, db_record):
        self.db_record = db_record
        self.dealer = self.db_record.dealer


class PathScraper(Scraper):
    """
    Responsible for scraping a path and returning a dict.
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.data = {}

    def add_data(self, key, value):
        self.data[key] = value

    def build_url(self, path):
        return self.base_url + path

    def get_result(self):
        return self.data


class CategoryScraper(PathScraper):

    DRIVER_CATEGORY = '//a[@id="lbCategoryName"]/@href'

    def run(self, path):
        categories = self.get_html(
            self.build_url(path)).xpath(self.DRIVER_CATEGORY)
        data = [c for c in categories if not re.search(r"replace|recone", c)]
        self.add_data("categories", data)


class DriverScraper(PathScraper):
    pass


class DriverListingScraper(PathScraper):
    pass


class PartsExpressScraper(DealerScraper):

    SEED = "/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13"

    def run(self):
        category_scraper = CategoryScraper(self.dealer.website)
        category_scraper.run(self.SEED)
        print("{0}".format(category_scraper.get_result()))
