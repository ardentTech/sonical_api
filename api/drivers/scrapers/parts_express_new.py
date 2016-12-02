import re

from lxml import html
import requests

from drivers.factories import DriverFactory


# @todo only run one category at a time? track via class variable?
# @todo add sleeps
# @todo multithreading
# @todo be more explicit naming XPATH patterns
# @todo move XPATH patterns to separate module
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
    RMS_POWER = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[2]/span[2]/text()'
    SENSITIVITY = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[8]/span[2]/text()'
    VOICE_COIL_INDUCTANCE = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[4]/span[2]/text()'
    attribute_patterns = [
        ("dc_resistance", DC_RESISTANCE),
        ("electromagnetic_q", ELECTROMAGNETIC_Q),
        ("manufacturer", MANUFACTURER),
        ("max_power", MAX_POWER),
        ("mechanical_q", MECHANICAL_Q),
        ("model", MODEL),
        ("nominal_diameter", NOMINAL_DIAMETER),
        ("nominal_impedance", NOMINAL_IMPEDANCE),
        ("resonant_frequency", RESONANT_FREQUENCY),
        ("rms_power", RMS_POWER),
        ("sensitivity", SENSITIVITY),
        ("voice_coil_inductance", VOICE_COIL_INDUCTANCE)]

    def run(self, path):
        tree = self._get_tree(path)
        return {ap[0]: tree.xpath(ap[1]) for ap in self.attribute_patterns}


class DriverListScraper(Scraper):

    DRIVER_DETAIL_XPATH = '//a[@id="GridViewProdLink"]/@href'
    NEXT_PAGE_XPATH = '//a[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxBottomPagingLinks_aNextNav"]/@href'

    def __init__(self):
        self.data = []

    def run(self, path):
        tree = self._get_tree(path)

        for driver in tree.xpath(self.DRIVER_DETAIL_XPATH):
            self.data.append(driver)

        # crawl pagination
        try:
            self.run(tree.xpath(self.NEXT_PAGE_XPATH)[0])
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

        for driver in drivers:
            # @todo sanitize data
            # @todo handle FK to manufacturer
            DriverFactory.create(**driver)
