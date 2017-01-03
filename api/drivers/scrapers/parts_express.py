from decimal import Decimal
import re

from .scraper import Scraper


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

    def run(self, path):
        data = {}
        tree = self.get_tree(self.url_from_path(path))

        for idx, section in enumerate(self.TARGETS):
            root = tree.xpath(section[0])[0]
            pattern = '{0}'
            if idx == 1:
                pattern = 'span[text()="{0}"]/following-sibling::span[1]/text()'

            for items in section[1]:
                try:
                    val = root.xpath("//" + pattern.format(items[1]))[0]
                    if items[2]:
                        val = getattr(self, "_to_" + items[2])(val)
                    data[items[0]] = val
                except:
                    pass

        print("{0}".format(data))
        return data

    def _to_decimal(self, val):
        return Decimal(val.split(" ")[0])

    def _to_int(self, val):
        return int(val.split(" ")[0])


class DriverListScraper(BasePartsExpressScraper):

    TARGETS = {
        "DRIVER_DETAIL": '//a[@id="GridViewProdLink"]/@href',
        "NEXT_PAGE": '//a[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxBottomPagingLinks_aNextNav"]/@href',
    }

    def __init__(self):
        super(DriverListScraper, self).__init__()
        self.data = []

    def run(self, path):
        tree = self.get_tree(self.url_from_path(path))

        for driver in tree.xpath(self.TARGETS["DRIVER_DETAIL"]):
            self.data.append(driver)

        if self.pro_mode():
            try:
                return self.run(tree.xpath(self.TARGETS["NEXT_PAGE"])[0])
            except IndexError:
                return self.data

        return self.data


class CategoryListScraper(BasePartsExpressScraper):

    TARGETS = {
        "DRIVER_CATEGORY": '//a[@id="lbCategoryName"]/@href'
    }

    def run(self, path):
        categories = self.get_tree(
            self.url_from_path(path)).xpath(
                self.TARGETS["DRIVER_CATEGORY"])
        data = [c for c in categories if not re.search(r'replace|recone', c)]

        if self.dev_mode():
            data = data[:1]

        return data


class PartsExpressScraper(BasePartsExpressScraper):

    INITIAL_CATEGORY_PATH = "/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13"

    def run(self):
        data = []

        for cp in CategoryListScraper().run(self.INITIAL_CATEGORY_PATH):
            for dp in DriverListScraper().run(cp):
                data.append(DriverScraper().run(dp))

        return data
