import re

from lxml import html
import requests

from drivers.factories import DriverFactory
from drivers.models import Driver
from manufacturing.models import Manufacturer


DRIVER_CATEGORIES_PATH = '/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13'
DRIVER_CATEGORY_XPATH = '//a[@id="lbCategoryName"]/@href'
DRIVER_DETAIL_XPATH = '//a[@id="GridViewProdLink"]/@href'
HOST = "www.parts-express.com"
NEXT_PAGE_XPATH = '//a[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxBottomPagingLinks_aNextNav"]/@href'
PROTOCOL = "https://"


# @todo add ability to only scrape one category at a time?


class PartsExpress(object):

    def __init__(self):
        self.data_store = {}

    # @todo handle each category on a different thread
    def run(self):
        categories = self._get_categories()
        for category in categories:
            data_store = self.data_store.setdefault(category[0], [])
            self._scrape_and_advance(category[1], data_store)
            self._create_drivers(data_store)

    def _build_url(self, path):
        return PROTOCOL + HOST + path

    # @todo fetch all manufacturers on init
    def _create_driver(self, attrs):
        manufacturer, created = Manufacturer.objects.get_or_create(
            name=attrs["manufacturer"])
        DriverFactory.create(manufacturer=manufacturer, model=attrs["model"])

    def _create_drivers(self, store):
        for path in store:
            url = self._build_url(path)
            driver = Driver.objects.filter(data_source=url)
            if not driver:
                self._create_driver(self._get_driver_attrs(url))

    def _get_categories(self):
        page = requests.get(self._build_url(DRIVER_CATEGORIES_PATH))
        tree = html.fromstring(page.content)
        paths = tree.xpath(DRIVER_CATEGORY_XPATH)
        return [
            (p.split("/")[2], p) for p in paths if not re.search(r'replace|recone', p)]

    def _get_driver_attrs(self, url):
        attrs = {}

        page = requests.get(url)
        tree = html.fromstring(page.content)

        attrs["manufacturer"] = tree.xpath('//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[6]/ul/li[1]/span[2]/text()')[0]
        attrs["model"] = tree.xpath('//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[6]/ul/li[2]/span[2]/text()')[0]

        return attrs

    # @todo rename this
    def _scrape_and_advance(self, path, store):
        page = requests.get(self._build_url(path))
        tree = html.fromstring(page.content)
        store.append(tree.xpath(DRIVER_DETAIL_XPATH)[0])

        try:
            next_path = tree.xpath(NEXT_PAGE_XPATH)[0]
            self._scrape_and_advance(next_path, store)
        except IndexError:  # no next_path was found
            return
        except Exception as e:
            print("Unexpected Exception: {0}".format(e))
