from decimal import Decimal
import re

from django.conf import settings

from .scraper import Scraper


# @todo scrape driver rating and review # (these are AJAX)
# @todo multithreading


class BasePartsExpressScraper(Scraper):

    URL = "https://www.parts-express.com"

    def url_from_path(self, path):
        return self.URL + path


class DriverScraper(BasePartsExpressScraper):

    TARGETS = [
        ('//div[@id="MiddleColumn1"]', [
            # (key, xpath pattern, desired type)
            ("price", 'div[@class="PriceContBox"]/div[1]/div[1]/span[1]/span[2]/text()', "decimal"),
        ]),
        ('//div[@class="ProducDetailsNote"]', [
            # (key, table row column one text, to type)
            ("dc_resistance", "DC Resistance (Re)", "decimal"),
            ("electromagnetic_q", "Electromagnetic Q (Qes)", None),
            ("manufacturer", "Brand", None),
            ("max_power", "Power Handling (max)", "int"),
            ("mechanical_q", "Mechanical Q (Qms)", None),
            ("model", "Model", None),
            ("nominal_diameter", "Nominal Diameter", None),
            ("nominal_impedance", "Impedance", "decimal"),
            ("resonant_frequency", "Resonant Frequency (Fs)", "decimal"),
            ("rms_power", "Power Handling (RMS)", "int"),
            ("sensitivity", "Sensitivity", "decimal"),
            ("voice_coil_inductance", "Voice Coil Inductance (Le)", "decimal"),
        ])
    ]

    def __init__(self, mode):
        self.data = {}

    def run(self, path):
        tree = self._get_tree(self.url_from_path(path))

        for idx, section in enumerate(self.TARGETS):
            root = tree.xpath(section[0])[0]
            pattern = '{0}'
            if idx == 1:
                pattern = 'span[text()="{0}"]/following-sibling::span[1]/text()'

            for items in section[1]:
                val = root.xpath("//" + pattern.format(items[1]))[0]
                if items[2]:
                    val = getattr(self, "_to_" + items[2])(val)
                self.data[items[0]] = val

        return self.data

    def _to_decimal(self, val):
        return Decimal(val.split(" ")[0])

    def _to_int(self, val):
        return int(val.split(" ")[0])

    def _to_rating_int(self, val):
        pass


class DriverListScraper(BasePartsExpressScraper):

    XPATH = {
        "DRIVER_DETAIL": '//a[@id="GridViewProdLink"]/@href',
        "NEXT_PAGE": '//a[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxBottomPagingLinks_aNextNav"]/@href',
    }

    def __init__(self, mode):
        self.data = []
        self.should_paginate = False if mode == self.DEV_MODE else True

    def run(self, path):
        tree = self._get_tree(self.url_from_path(path))

        for driver in tree.xpath(self.XPATH["DRIVER_DETAIL"]):
            self.data.append(driver)

        if self.should_paginate:
            try:
                return self.run(tree.xpath(self.XPATH["NEXT_PAGE"])[0])
            except IndexError:
                return self.data

        return self.data


class CategoryListScraper(BasePartsExpressScraper):

    XPATH = {
        "DRIVER_CATEGORY": '//a[@id="lbCategoryName"]/@href'
    }

    def __init__(self, mode):
        self.data = []
        self.mode = mode

    def run(self, path):
        categories = self._get_tree(
            self.url_from_path(path)).xpath(
                self.XPATH["DRIVER_CATEGORY"])
        self.data = [c for c in categories if not re.search(r'replace|recone', c)]

        if self.mode == self.DEV_MODE:
            self.data = self.data[:1]

        return self.data


class PartsExpressScraper(BasePartsExpressScraper):

    INITIAL_CATEGORY_PATH = "/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13"

    def __init__(self):
        self.data = []
        self.mode = self.DEV_MODE if settings.DEBUG is True else self.PRO_MODE

    def run(self):
        for cp in CategoryListScraper(mode=self.mode).run(self.INITIAL_CATEGORY_PATH):
            for dp in DriverListScraper(mode=self.mode).run(cp):
                self.data.append(DriverScraper(mode=self.mode).run(dp))

        return self.data
