from decimal import Decimal
import re

from .scraper import Scraper


# @todo scrape driver price, rating and review #
# @todo multithreading
# @todo adjust XPATH patterns to match by text instead of just position indexes


DEV_MODE = "dev"
PRO_MODE = "pro"
URL = "https://www.parts-express.com"
XPATH_PATTERNS = {
    "DC_RESISTANCE": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[2]/span[2]/text()',
    "DRIVER_CATEGORY_XPATH": '//a[@id="lbCategoryName"]/@href',
    "DRIVER_DETAIL_XPATH": '//a[@id="GridViewProdLink"]/@href',
    "ELECTROMAGNETIC_Q": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[7]/span[2]/text()',
    "MANUFACTURER": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[6]/ul/li[1]/span[2]/text()',
    "MAX_POWER": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[4]/span[2]/text()',
    "MECHANICAL_Q": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[5]/span[2]/text()',
    "MODEL": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[6]/ul/li[2]/span[2]/text()',
    "NEXT_PAGE_XPATH": '//a[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxBottomPagingLinks_aNextNav"]/@href',
    "NOMINAL_DIAMETER": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[1]/span[2]/text()',
    "NOMINAL_IMPEDANCE": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[5]/span[2]/text()',
    "RESONANT_FREQUENCY": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[1]/span[2]/text()',
    "REVIEW_COUNT": '//*[@id="TurnToTopSummary"]/div[1]/div/div[2]/a[1]/text()',
    "RMS_POWER": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[2]/span[2]/text()',
    "SENSITIVITY": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[8]/span[2]/text()',
    "VOICE_COIL_INDUCTANCE": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[4]/span[2]/text()',
}


class DriverScraper(Scraper):

    def __init__(self, mode):
        _attrs = self._get_driver_attrs()
        self.driver_attrs = [
            {"key": attr[0], "pattern": attr[1], "sanitizer": attr[2]} for attr in _attrs]

        self.data = {}

    def run(self, path):
        self.data["data_source"] = URL + path
        tree = self._get_tree(self.data["data_source"])

        for attr in self.driver_attrs:
            val = tree.xpath(attr["pattern"])[0]
            if attr["sanitizer"] is not None:
                val = attr["sanitizer"](val)
            self.data[attr["key"]] = val

        return self.data

    def _get_driver_attrs(self):
        return [
            ("dc_resistance", XPATH_PATTERNS["DC_RESISTANCE"], self._to_decimal),
            ("electromagnetic_q", XPATH_PATTERNS["ELECTROMAGNETIC_Q"], None),
            ("manufacturer", XPATH_PATTERNS["MANUFACTURER"], None),
            ("max_power", XPATH_PATTERNS["MAX_POWER"], self._to_int),
            ("mechanical_q", XPATH_PATTERNS["MECHANICAL_Q"], None),
            ("model", XPATH_PATTERNS["MODEL"], None),
            ("nominal_diameter", XPATH_PATTERNS["NOMINAL_DIAMETER"], None),
            ("nominal_impedance", XPATH_PATTERNS["NOMINAL_IMPEDANCE"], self._to_decimal),
            ("resonant_frequency", XPATH_PATTERNS["RESONANT_FREQUENCY"], self._to_decimal),
            ("rms_power", XPATH_PATTERNS["RMS_POWER"], self._to_int),
            ("sensitivity", XPATH_PATTERNS["SENSITIVITY"], self._to_decimal),
            ("voice_coil_inductance", XPATH_PATTERNS["VOICE_COIL_INDUCTANCE"], self._to_decimal)]

    def _to_decimal(self, val):
        return Decimal(val.split(" ")[0])

    def _to_int(self, val):
        return int(val.split(" ")[0])


class DriverListScraper(Scraper):

    def __init__(self, mode):
        self.data = []
        self.should_paginate = False if mode == DEV_MODE else True

    def run(self, path):
        tree = self._get_tree(URL + path)

        for driver in tree.xpath(XPATH_PATTERNS["DRIVER_DETAIL_XPATH"]):
            self.data.append(driver)

        if self.should_paginate:
            try:
                return self.run(tree.xpath(XPATH_PATTERNS["NEXT_PAGE_XPATH"])[0])
            except IndexError:
                return self.data

        return self.data


class CategoryListScraper(Scraper):

    def __init__(self, mode):
        self.data = []
        self.mode = mode

    def run(self, path):
        categories = self._get_tree(URL + path).xpath(XPATH_PATTERNS["DRIVER_CATEGORY_XPATH"])
        self.data = [c for c in categories if not re.search(r'replace|recone', c)]

        if self.mode == DEV_MODE:
            self.data = self.data[:1]

        return self.data


class PartsExpressScraper(Scraper):

    INITIAL_CATEGORY_PATH = "/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13"

    def __init__(self):
        # @todo this should be an arg later
        self.mode = DEV_MODE

    def run(self):
        drivers = []

        for cp in CategoryListScraper(mode=self.mode).run(self.INITIAL_CATEGORY_PATH):
            for dp in DriverListScraper(mode=self.mode).run(cp):
                drivers.append(DriverScraper(mode=self.mode).run(dp))

        return drivers
