from time import sleep

from lxml import html
import requests

from products.models import Dealer
from utils.mixins.mode import ModeMixin


class Scraper(ModeMixin):

    # @todo put this in settings
    PAUSE_SECONDS = 1
    SCRAPER_ID = "Sonical Scraper 1.0 (jonathan@ardent.tech)"

    def __init__(self, base_url=None):
        self.result = ScraperResult()
        self.base_url = base_url

    def add_error(self, e):
        self.result.errors.append(e)

    def add_pass(self, p):
        self.result.passes.append(p)

    def add_skip(self, s):
        self.result.skips.append(s)

    def build_url(self, path):
        return self.base_url + path

    def get_html(self, url):
        sleep(self.PAUSE_SECONDS)
        page = requests.get(url, headers={"user-agent": self.SCRAPER_ID})
        return html.fromstring(page.content)

    def run(self):
        raise Exception("Sub-classes of Scraper must implement a `run()` method")


class DealerScraper(Scraper):

    def __init__(self):
        super(DealerScraper, self).__init__()
        # @todo could this ever return more than one?
        self.dealer = Dealer.objects.get(name=self.LABEL)

    def get_url(self):
        return self.dealer.website


class ScraperResult(object):

    def __init__(self):
        self.errors = []
        self.passes = []
        self.skips = []

    def attempts(self):
        return len(self.errors) + len(self.passes) + len(self.skips)
