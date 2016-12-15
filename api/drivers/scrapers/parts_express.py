from decimal import Decimal
import re
from time import sleep

from lxml import html
import requests


# @todo scrape driver price, rating and review #
# @todo need some sort of dev mode
# @todo multithreading
# @todo move XPATH patterns to separate module?
# @todo adjust XPATH patterns to match by text instead of just position indexes


class Scraper(object):

    SCRAPER_ID = "Sonical Scraper 1.0 (jonathan@ardent.tech)"
    URL = "https://www.parts-express.com"

    def run(self, path):
        raise Exception("Sub-classes of Scraper must implement `run(self, path)`")

    def _get_tree(self, path):
        headers = {"user-agent": self.SCRAPER_ID}
        page = requests.get(self.URL + path, headers=headers)
        tree = html.fromstring(page.content)
        sleep(1)
        return tree


class DriverScraper(Scraper):

    DC_RESISTANCE = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[2]/span[2]/text()'
    ELECTROMAGNETIC_Q = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[7]/span[2]/text()'
    MANUFACTURER = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[6]/ul/li[1]/span[2]/text()'
    MAX_POWER = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[4]/span[2]/text()'
    MECHANICAL_Q = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[5]/span[2]/text()'
    MODEL = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[6]/ul/li[2]/span[2]/text()'
    NOMINAL_DIAMETER = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[1]/span[2]/text()'
    NOMINAL_IMPEDANCE = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[5]/span[2]/text()'
    RESONANT_FREQUENCY = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[1]/span[2]/text()'
    REVIEW_COUNT = '//*[@id="TurnToTopSummary"]/div[1]/div/div[2]/a[1]/text()'
    RMS_POWER = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[2]/span[2]/text()'
    SENSITIVITY = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[8]/span[2]/text()'
    VOICE_COIL_INDUCTANCE = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[4]/span[2]/text()'
#    RATING = '//*[@id="TurnToTopSummary"]/div[1]/div/div[1]'  # need CSS class

    def __init__(self):
        self.attributes = [
            # (key, xpath_pattern, santizer)
            ("dc_resistance", self.DC_RESISTANCE, self._sanitize_decimal),
            ("electromagnetic_q", self.ELECTROMAGNETIC_Q, None),
            ("manufacturer", self.MANUFACTURER, None),
            ("max_power", self.MAX_POWER, self._sanitize_int),
            ("mechanical_q", self.MECHANICAL_Q, None),
            ("model", self.MODEL, None),
            ("nominal_diameter", self.NOMINAL_DIAMETER, None),
            ("nominal_impedance", self.NOMINAL_IMPEDANCE, self._sanitize_decimal),
            ("resonant_frequency", self.RESONANT_FREQUENCY, self._sanitize_decimal),
            ("rms_power", self.RMS_POWER, self._sanitize_int),
            ("sensitivity", self.SENSITIVITY, self._sanitize_decimal),
            ("voice_coil_inductance", self.VOICE_COIL_INDUCTANCE, self._sanitize_decimal)]

    def run(self, path):
        tree = self._get_tree(path)
        attr = {"data_source": self.URL + path}
        for _attr in self.attributes:
            val = tree.xpath(_attr[1])[0]
            if _attr[2] is not None:
                val = _attr[2](val)
            attr[_attr[0]] = val

        return attr

    def _sanitize_decimal(self, val):
        return Decimal(val.split(" ")[0])

    def _sanitize_int(self, val):
        return int(val.split(" ")[0])


class DriverListScraper(Scraper):

    DRIVER_DETAIL_XPATH = '//a[@id="GridViewProdLink"]/@href'
# @todo figure out how to grab price while looping through drivers on 96
#    DRIVER_PRICE = '//*[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxProductListing_dlProductsGridView_ctl00_divPriceBox"]/div/span[2]/text()'
    NEXT_PAGE_XPATH = '//a[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxBottomPagingLinks_aNextNav"]/@href'

    def __init__(self):
        self.data = []

    def run(self, path):
        tree = self._get_tree(path)

        for driver in tree.xpath(self.DRIVER_DETAIL_XPATH):
            # @todo might want to grab price here
            self.data.append(driver)

        return self.data
        # crawl pagination
        try:
            return self.run(tree.xpath(self.NEXT_PAGE_XPATH)[0])
        except IndexError:
            return self.data


class CategoryListScraper(Scraper):

    DRIVER_CATEGORY_XPATH = '//a[@id="lbCategoryName"]/@href'

    def run(self, path):
        tree = self._get_tree(path)
        categories = tree.xpath(self.DRIVER_CATEGORY_XPATH)
        return [c for c in categories if not re.search(r'replace|recone', c)]


class PartsExpressScraper(Scraper):

    CATEGORY_LIST_PATH = "/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13"

    def __init__(self):
        self.scrapers = {
            "category_list": CategoryListScraper(),
            "driver_list": DriverListScraper(),
            "driver": DriverScraper()}

    def run(self):
        drivers = []
        category_paths = self.scrapers["category_list"].run(self.CATEGORY_LIST_PATH)
        for cp in category_paths:
            driver_paths = self.scrapers["driver_list"].run(cp)
            for dp in driver_paths:
                drivers.append(self.scrapers["driver"].run(dp))

        return drivers
